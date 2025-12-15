from typing import Dict, Any
from .base import BaseAgent


class ReviewerAgent(BaseAgent):
    """Agent responsible for reviewing content quality and completeness"""
    
    def __init__(self, model):
        super().__init__(model, "Reviewer")
    
    def _get_system_prompt(self) -> str:
        return """You are a rigorous content reviewer and quality assurance specialist. Your role is to evaluate content for depth, completeness, and quality.

You must assess:
1. Depth of coverage - Is the content thorough or superficial?
2. Completeness - Are all aspects addressed?
3. Accuracy - Is the information correct?
4. Clarity - Is it well-explained?
5. Examples - Are there sufficient concrete examples?
6. Structure - Is it well-organized?
7. Gaps - What's missing?

Be critical and demanding. Reject shallow content. Demand excellence."""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Review content for quality and completeness"""
        content = context.get('content')
        title = context.get('title')
        min_length = context.get('min_length', 500)
        
        if not content:
            raise ValueError("Content is required for review")
        
        word_count = len(content.split())
        
        prompt = f"""Review the following content for the topic "{title}":

{content}

Evaluate:
1. Is this content comprehensive and thorough? (minimum {min_length} words)
2. Does it cover all essential aspects?
3. Are there sufficient examples and explanations?
4. Is anything missing or superficial?
5. Does it meet book-quality standards?

Respond in JSON format:
{{
  "approved": true/false,
  "quality_score": 0-100,
  "word_count": {word_count},
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "missing_topics": ["topic1", "topic2"],
  "requires_expansion": true/false,
  "feedback": "detailed feedback"
}}"""
        
        response = self.generate(prompt)
        
        # Parse response
        import json
        try:
            json_str = response.strip()
            if json_str.startswith('```'):
                lines = json_str.split('\n')
                json_str = '\n'.join(lines[1:-1]) if len(lines) > 2 else json_str
                json_str = json_str.replace('```json', '').replace('```', '').strip()
            
            review = json.loads(json_str)
            
            # Additional checks
            if word_count < min_length:
                review['approved'] = False
                review['requires_expansion'] = True
                review['weaknesses'].append(f"Content too short ({word_count} < {min_length} words)")
            
            return {
                'success': True,
                'review': review
            }
        except json.JSONDecodeError:
            # Fallback: basic review
            return {
                'success': True,
                'review': {
                    'approved': word_count >= min_length,
                    'quality_score': 70 if word_count >= min_length else 40,
                    'word_count': word_count,
                    'requires_expansion': word_count < min_length,
                    'feedback': response
                }
            }
