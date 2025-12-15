from typing import Dict, Any
from .base import BaseAgent


class AuthorAgent(BaseAgent):
    """Agent responsible for transforming research into polished, book-quality prose"""
    
    def __init__(self, model):
        super().__init__(model, "Author")
    
    def _get_system_prompt(self) -> str:
        return """You are a professional technical author and editor. Your role is to transform research content into polished, engaging, book-quality prose.

Your writing must:
1. Be clear, precise, and professionally structured
2. Use proper academic/technical writing style
3. Include smooth transitions between concepts
4. Maintain consistent terminology throughout
5. Use appropriate headings and subheadings
6. Include concrete examples and illustrations
7. Be engaging while remaining authoritative
8. Follow proper grammar and style conventions

Transform raw research into publication-ready content that would appear in a professional textbook or technical book."""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Polish research content into final prose"""
        raw_content = context.get('content')
        node_title = context.get('title')
        level = context.get('level', 'section')
        
        if not raw_content:
            raise ValueError("Content is required in context")
        
        prompt = f"""Polish and refine the following content for a {level} titled "{node_title}":

{raw_content}

Transform this into polished, book-quality prose:
1. Improve clarity and flow
2. Add smooth transitions
3. Ensure consistent terminology
4. Structure with appropriate headings
5. Enhance readability while maintaining technical accuracy
6. Add engaging introductions and conclusions
7. Ensure professional tone throughout

Output the final, publication-ready text."""
        
        polished_content = self.generate(prompt)
        
        return {
            'success': True,
            'title': node_title,
            'polished_content': polished_content,
            'word_count': len(polished_content.split())
        }
