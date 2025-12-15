import json
import re
from typing import Dict, Any, List
from .base import BaseAgent


class PlannerAgent(BaseAgent):
    """Agent responsible for creating comprehensive topic outlines"""
    
    def __init__(self, model):
        super().__init__(model, "Planner")
    
    def _get_system_prompt(self) -> str:
        return """You are an expert academic planner and curriculum designer. Your role is to create comprehensive, hierarchical outlines for any topic.

Your outlines must:
1. Cover ALL aspects of the topic exhaustively
2. Be structured in a clear hierarchy: Topic → Chapters → Sections → Subsections
3. Include theoretical foundations, practical applications, history, examples, and advanced concepts
4. Be organized logically, building from fundamentals to advanced topics
5. Identify knowledge gaps that need deep exploration
6. Be suitable for a book-length treatment (not a brief overview)

CRITICAL: You MUST respond with ONLY valid JSON. No explanations, no markdown, no extra text.

Use this EXACT format:
{
  "topic": "Main Topic",
  "chapters": [
    {
      "id": "ch1",
      "title": "Chapter Title",
      "sections": [
        {
          "id": "ch1_s1",
          "title": "Section Title",
          "subsections": [
            {
              "id": "ch1_s1_ss1",
              "title": "Subsection Title",
              "key_points": ["point1", "point2"]
            }
          ]
        }
      ]
    }
  ]
}"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive outline for the topic"""
        topic = context.get('topic')
        if not topic:
            raise ValueError("Topic is required in context")
        
        prompt = f"""Create a comprehensive, book-level outline for the topic: "{topic}"

This outline will be used to generate a complete, professional book. Include:
- Foundational concepts and definitions
- Historical context and evolution
- Theoretical frameworks
- Practical applications and examples
- Common pitfalls and misconceptions
- Advanced topics and cutting-edge developments
- Real-world case studies
- Best practices and methodologies

Ensure the outline is exhaustive and covers every important aspect. Think like you're planning a 300+ page book.

RESPOND WITH ONLY JSON - NO OTHER TEXT."""
        
        # Try multiple times with different approaches
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = self.generate(prompt)
                outline = self._extract_and_parse_json(response)
                
                if outline:
                    return {
                        'success': True,
                        'outline': outline,
                        'total_nodes': self._count_nodes(outline)
                    }
                    
            except Exception as e:
                print(f"[Planner] Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_attempts - 1:
                    # Last attempt - try fallback
                    return self._create_fallback_outline(topic)
        
        return self._create_fallback_outline(topic)
    
    def _extract_and_parse_json(self, response: str) -> Dict[str, Any]:
        """Extract and parse JSON from model response with multiple strategies"""
        
        # Strategy 1: Direct JSON parsing
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Remove markdown code blocks
        try:
            json_str = response.strip()
            if '```' in json_str:
                # Extract content between code blocks
                pattern = r'```(?:json)?\s*(.*?)\s*```'
                match = re.search(pattern, json_str, re.DOTALL)
                if match:
                    json_str = match.group(1).strip()
                else:
                    # Remove all ``` markers
                    json_str = json_str.replace('```json', '').replace('```', '').strip()
            
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # Strategy 3: Find JSON object boundaries
        try:
            # Look for { ... } pattern
            start = response.find('{')
            if start != -1:
                # Find matching closing brace
                brace_count = 0
                end = start
                for i, char in enumerate(response[start:], start):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end = i + 1
                            break
                
                if end > start:
                    json_str = response[start:end]
                    return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # Strategy 4: Clean and retry
        try:
            # Remove common prefixes/suffixes
            cleaned = response.strip()
            prefixes_to_remove = [
                "Here's the JSON outline:",
                "Here is the JSON outline:",
                "The outline is:",
                "JSON outline:",
                "Outline:",
            ]
            
            for prefix in prefixes_to_remove:
                if cleaned.lower().startswith(prefix.lower()):
                    cleaned = cleaned[len(prefix):].strip()
            
            # Remove trailing explanations
            if '\n\n' in cleaned:
                parts = cleaned.split('\n\n')
                for part in parts:
                    if part.strip().startswith('{'):
                        cleaned = part.strip()
                        break
            
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass
        
        return None
    
    def _create_fallback_outline(self, topic: str) -> Dict[str, Any]:
        """Create a basic fallback outline when JSON parsing fails"""
        print(f"[Planner] Creating fallback outline for: {topic}")
        
        # Create a basic but comprehensive outline
        outline = {
            "topic": topic,
            "chapters": [
                {
                    "id": "ch1",
                    "title": "Introduction and Fundamentals",
                    "sections": [
                        {
                            "id": "ch1_s1",
                            "title": "Overview and Definitions",
                            "subsections": [
                                {
                                    "id": "ch1_s1_ss1",
                                    "title": "Basic Concepts",
                                    "key_points": ["Core definitions", "Key terminology"]
                                },
                                {
                                    "id": "ch1_s1_ss2",
                                    "title": "Historical Context",
                                    "key_points": ["Evolution", "Timeline"]
                                }
                            ]
                        },
                        {
                            "id": "ch1_s2",
                            "title": "Theoretical Foundation",
                            "subsections": [
                                {
                                    "id": "ch1_s2_ss1",
                                    "title": "Core Principles",
                                    "key_points": ["Fundamental laws", "Basic rules"]
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": "ch2",
                    "title": "Core Concepts and Methods",
                    "sections": [
                        {
                            "id": "ch2_s1",
                            "title": "Primary Methods",
                            "subsections": [
                                {
                                    "id": "ch2_s1_ss1",
                                    "title": "Basic Techniques",
                                    "key_points": ["Standard approaches", "Common methods"]
                                }
                            ]
                        },
                        {
                            "id": "ch2_s2",
                            "title": "Advanced Techniques",
                            "subsections": [
                                {
                                    "id": "ch2_s2_ss1",
                                    "title": "Complex Methods",
                                    "key_points": ["Advanced strategies", "Specialized techniques"]
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": "ch3",
                    "title": "Practical Applications",
                    "sections": [
                        {
                            "id": "ch3_s1",
                            "title": "Real-world Examples",
                            "subsections": [
                                {
                                    "id": "ch3_s1_ss1",
                                    "title": "Case Studies",
                                    "key_points": ["Practical examples", "Success stories"]
                                }
                            ]
                        },
                        {
                            "id": "ch3_s2",
                            "title": "Best Practices",
                            "subsections": [
                                {
                                    "id": "ch3_s2_ss1",
                                    "title": "Guidelines and Standards",
                                    "key_points": ["Industry standards", "Recommended practices"]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        return {
            'success': True,
            'outline': outline,
            'total_nodes': self._count_nodes(outline),
            'fallback_used': True
        }
    
    def _count_nodes(self, outline: Dict[str, Any]) -> int:
        """Count total number of nodes in the outline"""
        count = 0
        for chapter in outline.get('chapters', []):
            count += 1
            for section in chapter.get('sections', []):
                count += 1
                count += len(section.get('subsections', []))
        return count
