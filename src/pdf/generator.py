import os
from typing import Dict, Any, List
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor


class PDFGenerator:
    """Generates professional PDF documents from content"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pdf_config = config.get('pdf', {})
        self.styles = self._create_styles()
    
    def _create_styles(self):
        """Create custom paragraph styles"""
        styles = getSampleStyleSheet()
        
        # Title style
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=self.pdf_config.get('title_font_size', 24),
            textColor='#1a1a1a',
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Chapter style
        styles.add(ParagraphStyle(
            name='Chapter',
            parent=styles['Heading1'],
            fontSize=self.pdf_config.get('chapter_font_size', 18),
            textColor='#2c3e50',
            spaceAfter=20,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Section style
        styles.add(ParagraphStyle(
            name='Section',
            parent=styles['Heading2'],
            fontSize=self.pdf_config.get('section_font_size', 14),
            textColor='#34495e',
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection style
        styles.add(ParagraphStyle(
            name='Subsection',
            parent=styles['Heading3'],
            fontSize=12,
            textColor='#555555',
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        # Body style
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['BodyText'],
            fontSize=self.pdf_config.get('body_font_size', 11),
            leading=self.pdf_config.get('body_font_size', 11) * self.pdf_config.get('line_spacing', 1.5),
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # Code block style
        styles.add(ParagraphStyle(
            name='CodeBlock',
            parent=styles['Code'],
            fontSize=9,
            fontName='Courier',
            textColor=HexColor('#2c3e50'),
            backColor=HexColor('#f5f5f5'),
            leftIndent=20,
            rightIndent=20,
            spaceBefore=8,
            spaceAfter=8
        ))
        
        # SubHeading style (for markdown headers in content)
        styles.add(ParagraphStyle(
            name='SubHeading',
            parent=styles['Heading3'],
            fontSize=11,
            textColor='#666666',
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))
        
        # BulletPoint style
        styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=styles['BodyText'],
            fontSize=self.pdf_config.get('body_font_size', 11),
            leftIndent=20,
            spaceAfter=6
        ))
        
        # TOC styles
        styles.add(ParagraphStyle(
            name='TOCHeading',
            parent=styles['Heading1'],
            fontSize=18,
            textColor='#2c3e50',
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='TOCEntry1',
            parent=styles['Normal'],
            fontSize=12,
            leftIndent=0,
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='TOCEntry2',
            parent=styles['Normal'],
            fontSize=11,
            leftIndent=20,
            spaceAfter=6
        ))
        
        styles.add(ParagraphStyle(
            name='TOCEntry3',
            parent=styles['Normal'],
            fontSize=10,
            leftIndent=40,
            spaceAfter=4
        ))
        
        return styles
    
    def generate(self, topic: str, content_files: List[str], output_path: str, metadata: Dict[str, Any]) -> str:
        """Generate PDF from content files"""
        
        print(f"\n[PDF Generator] Creating PDF: {output_path}")
        
        # First pass: collect TOC entries
        toc_entries = self._collect_toc_entries(content_files)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=self.pdf_config.get('margin', 72),
            leftMargin=self.pdf_config.get('margin', 72),
            topMargin=self.pdf_config.get('margin', 72),
            bottomMargin=self.pdf_config.get('margin', 72)
        )
        
        story = []
        
        # Title page
        story.extend(self._create_title_page(topic, metadata))
        story.append(PageBreak())
        
        # Table of contents
        story.extend(self._create_table_of_contents(toc_entries))
        story.append(PageBreak())
        
        # Process content files
        current_chapter = None
        
        for filepath in content_files:
            content_data = self._parse_content_file(filepath)
            
            if content_data['type'] == 'chapter':
                if current_chapter is not None:
                    story.append(PageBreak())
                current_chapter = content_data['title']
                story.append(Paragraph(content_data['title'], self.styles['Chapter']))
                story.append(Spacer(1, 0.2*inch))
            
            elif content_data['type'] == 'section':
                story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph(content_data['title'], self.styles['Section']))
                story.append(Spacer(1, 0.1*inch))
            
            elif content_data['type'] == 'subsection':
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph(content_data['title'], self.styles['Subsection']))
                story.append(Spacer(1, 0.05*inch))
            
            # Add content paragraphs
            for paragraph in content_data['paragraphs']:
                if paragraph.strip():
                    # Process paragraph with proper formatting
                    self._add_formatted_content(story, paragraph)
        
        # Build PDF
        try:
            doc.build(story)
            print(f"[PDF Generator] Successfully created: {output_path}")
            return output_path
        except Exception as e:
            raise RuntimeError(f"Failed to generate PDF: {e}")
    
    def _create_title_page(self, topic: str, metadata: Dict[str, Any]) -> List:
        """Create title page elements"""
        elements = []
        
        # Add spacing
        elements.append(Spacer(1, 2*inch))
        
        # Title
        elements.append(Paragraph(topic, self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle = "Comprehensive Notes Generated by AI"
        elements.append(Paragraph(subtitle, self.styles['CustomBody']))
        elements.append(Spacer(1, 1*inch))
        
        # Metadata
        date_str = datetime.now().strftime("%B %d, %Y")
        elements.append(Paragraph(f"Generated: {date_str}", self.styles['CustomBody']))
        
        if metadata.get('model'):
            elements.append(Paragraph(f"Model: {metadata['model']}", self.styles['CustomBody']))
        
        if metadata.get('total_word_count'):
            elements.append(Paragraph(f"Total Words: {metadata['total_word_count']:,}", self.styles['CustomBody']))
        
        return elements
    
    def _collect_toc_entries(self, content_files: List[str]) -> List[Dict[str, Any]]:
        """Collect table of contents entries from content files"""
        toc_entries = []
        
        for filepath in content_files:
            content_data = self._parse_content_file(filepath)
            
            # Determine level based on type
            level = 1
            if content_data['type'] == 'chapter':
                level = 1
            elif content_data['type'] == 'section':
                level = 2
            elif content_data['type'] == 'subsection':
                level = 3
            
            toc_entries.append({
                'title': content_data['title'],
                'level': level,
                'type': content_data['type']
            })
        
        return toc_entries
    
    def _create_table_of_contents(self, toc_entries: List[Dict[str, Any]]) -> List:
        """Create table of contents elements"""
        elements = []
        
        # TOC Title
        elements.append(Paragraph("Table of Contents", self.styles['TOCHeading']))
        elements.append(Spacer(1, 0.3*inch))
        
        # TOC Entries
        for entry in toc_entries:
            title = entry['title']
            level = entry['level']
            
            # Choose style based on level
            if level == 1:
                style = self.styles['TOCEntry1']
                prefix = ""
            elif level == 2:
                style = self.styles['TOCEntry2']
                prefix = "  "
            else:
                style = self.styles['TOCEntry3']
                prefix = "    "
            
            # Create TOC entry with dots
            toc_text = f"{prefix}{title}"
            elements.append(Paragraph(toc_text, style))
        
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _parse_content_file(self, filepath: str) -> Dict[str, Any]:
        """Parse a content file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Extract metadata from header
        title = ""
        node_type = "section"
        content_start = 0
        
        for i, line in enumerate(lines):
            if line.startswith('# '):
                title = line[2:].strip()
            elif line.startswith('Type: '):
                node_type = line[6:].strip()
            elif line.startswith('='*20):
                content_start = i + 1
                break
        
        # Extract content
        content = ''.join(lines[content_start:]).strip()
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        return {
            'title': title,
            'type': node_type,
            'paragraphs': paragraphs
        }
    
    def _add_formatted_content(self, story: List, text: str):
        """Add formatted content to story with proper handling of markdown"""
        import re
        
        # Check if it's a code block (starts with ``` or has multiple lines of code)
        if text.startswith('```') or (text.count('\n') > 2 and '    ' in text):
            # Extract code
            code = text.replace('```python', '').replace('```', '').strip()
            # Add as preformatted text
            story.append(Preformatted(code, self.styles['CodeBlock']))
            story.append(Spacer(1, 0.1*inch))
            return
        
        # Check if it's a markdown header (## or ###)
        if text.startswith('##'):
            level = text.count('#', 0, 4)
            header_text = text.lstrip('#').strip()
            if level == 2:
                story.append(Paragraph(header_text, self.styles['Section']))
            elif level == 3:
                story.append(Paragraph(header_text, self.styles['Subsection']))
            else:
                story.append(Paragraph(header_text, self.styles['SubHeading']))
            story.append(Spacer(1, 0.05*inch))
            return
        
        # Check if it's a bullet list
        if text.startswith('- ') or text.startswith('* '):
            # Split into individual bullets
            bullets = [line.strip() for line in text.split('\n') if line.strip().startswith(('- ', '* '))]
            for bullet in bullets:
                bullet_text = bullet.lstrip('- *').strip()
                formatted = self._format_inline_markdown(bullet_text)
                story.append(Paragraph(f"• {formatted}", self.styles['BulletPoint']))
            story.append(Spacer(1, 0.05*inch))
            return
        
        # Regular paragraph
        formatted = self._format_inline_markdown(text)
        story.append(Paragraph(formatted, self.styles['CustomBody']))
        story.append(Spacer(1, 0.1*inch))
    
    def _format_inline_markdown(self, text: str) -> str:
        """Format inline markdown (bold, italic, code) safely"""
        import re
        
        # Escape XML special characters first
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        # Handle inline code `code` -> <font name="Courier" color="#2c3e50">code</font>
        text = re.sub(
            r'`([^`]+?)`',
            r'<font name="Courier" color="#2c3e50" backColor="#f5f5f5">\1</font>',
            text
        )
        
        # Handle bold **text** -> <b>text</b>
        text = re.sub(r'\*\*([^*]+?)\*\*', r'<b>\1</b>', text)
        
        # Handle italic *text* -> <i>text</i> (but not ** which is bold)
        text = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<i>\1</i>', text)
        
        return text
