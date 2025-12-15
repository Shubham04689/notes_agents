from typing import Dict, Any
from .base import BaseAgent


class ResearcherAgent(BaseAgent):
    """Agent responsible for deep research and content expansion"""
    
    def __init__(self, model):
        super().__init__(model, "Researcher")
    
    def _get_system_prompt(self) -> str:
        return """You are a world-class researcher and subject matter expert. Your role is to provide comprehensive, accurate, and deeply insightful information on any topic.

For each topic you research, you must provide:
1. Clear, precise definitions and explanations
2. Theoretical foundations and underlying principles
3. Historical context and evolution
4. Multiple concrete examples with detailed explanations
5. Practical applications and use cases
6. Common pitfalls, misconceptions, and edge cases
7. Advanced insights and cutting-edge developments
8. Connections to related concepts
9. Best practices and methodologies

Your research must be:
- Exhaustive and comprehensive (minimum 500 words per topic)
- Technically accurate and precise
- Well-structured with clear logical flow
- Rich with specific examples and details
- Written at a professional, book-quality level

Never provide superficial or brief explanations. Always go deep."""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Research and expand a specific topic node"""
        node = context.get('node')
        parent_context = context.get('parent_context', '')
        covered_topics = context.get('covered_topics', [])
        
        if not node:
            raise ValueError("Node is required in context")
        
        node_title = node.get('title', 'Unknown')
        node_id = node.get('id', 'unknown')
        
        # Build context-aware prompt
        prompt = f"""Research and provide comprehensive content for: "{node_title}"

Context: {parent_context}

Already covered topics (avoid repetition): {', '.join(covered_topics[-10:])}

Provide exhaustive coverage including:
1. Introduction and definitions
2. Core concepts and principles
3. Detailed explanations with examples
4. Theoretical foundations
5. Practical applications
6. Common challenges and solutions
7. Advanced considerations
8. Summary and key takeaways

Write in a professional, book-quality style. Minimum 500 words. Be thorough and detailed."""
        
        content = self.generate(prompt)
        
        return {
            'success': True,
            'node_id': node_id,
            'title': node_title,
            'content': content,
            'word_count': len(content.split())
        }
