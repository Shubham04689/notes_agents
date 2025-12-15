from typing import Dict, Any
from .base import BaseAgent


class CompletionJudgeAgent(BaseAgent):
    """Agent responsible for determining when the work is truly complete"""
    
    def __init__(self, model):
        super().__init__(model, "Completion Judge")
    
    def _get_system_prompt(self) -> str:
        return """You are the final arbiter of completeness. Your role is to determine whether a body of work is truly complete and ready for publication.

You must verify:
1. All planned topics have been covered
2. No significant gaps remain
3. Content meets quality standards throughout
4. The work is comprehensive and exhaustive
5. No shallow or incomplete sections exist
6. The work represents a complete, professional treatment of the topic

Be extremely strict. Only approve truly complete work. When in doubt, demand more."""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Judge whether the work is complete"""
        outline = context.get('outline')
        coverage_status = context.get('coverage_status')
        total_word_count = context.get('total_word_count', 0)
        
        if not outline or not coverage_status:
            raise ValueError("Outline and coverage_status required")
        
        pending_count = coverage_status.get('pending_count', 0)
        covered_count = coverage_status.get('covered_count', 0)
        total_nodes = coverage_status.get('total_nodes', 0)
        
        prompt = f"""Evaluate whether this work is complete and ready for final PDF generation:

Topic: {outline.get('topic')}
Total Nodes: {total_nodes}
Covered Nodes: {covered_count}
Pending Nodes: {pending_count}
Total Word Count: {total_word_count}

Coverage Status:
{coverage_status}

Determine:
1. Are ALL topics fully covered?
2. Is the word count sufficient for a comprehensive book?
3. Are there any gaps or incomplete sections?
4. Does this represent a complete, professional treatment?
5. Is it ready for publication?

Respond in JSON format:
{{
  "is_complete": true/false,
  "confidence": 0-100,
  "reasoning": "detailed explanation",
  "remaining_gaps": ["gap1", "gap2"],
  "recommendations": ["rec1", "rec2"],
  "ready_for_pdf": true/false
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
            
            judgment = json.loads(json_str)
            
            # Override if pending nodes remain
            if pending_count > 0:
                judgment['is_complete'] = False
                judgment['ready_for_pdf'] = False
                judgment['remaining_gaps'].append(f"{pending_count} nodes still pending")
            
            # Minimum word count check (book should be substantial)
            if total_word_count < 10000:
                judgment['is_complete'] = False
                judgment['ready_for_pdf'] = False
                judgment['remaining_gaps'].append(f"Word count too low ({total_word_count} < 10000)")
            
            return {
                'success': True,
                'judgment': judgment
            }
        except json.JSONDecodeError:
            # Fallback: conservative judgment
            return {
                'success': True,
                'judgment': {
                    'is_complete': pending_count == 0 and total_word_count >= 10000,
                    'confidence': 50,
                    'ready_for_pdf': pending_count == 0 and total_word_count >= 10000,
                    'reasoning': response
                }
            }
