from typing import Dict, Any, Optional
from ..agents import (
    PlannerAgent, ResearcherAgent, AuthorAgent,
    CoverageTrackerAgent, ReviewerAgent, CompletionJudgeAgent
)
from ..models.base import BaseModelAdapter
from .storage import StorageManager
from .state import StateManager


class Orchestrator:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self, model: BaseModelAdapter, storage: StorageManager, state: StateManager, config: Dict[str, Any]):
        self.model = model
        self.storage = storage
        self.state = state
        self.config = config
        
        # Initialize agents
        self.planner = PlannerAgent(model)
        self.researcher = ResearcherAgent(model)
        self.author = AuthorAgent(model)
        self.tracker = CoverageTrackerAgent(model)
        self.reviewer = ReviewerAgent(model)
        self.judge = CompletionJudgeAgent(model)
        
        self.max_iterations = config.get('generation', {}).get('max_iterations', 100)
        self.min_section_length = config.get('generation', {}).get('min_section_length', 500)
        self.iteration_count = 0
    
    def generate_notes(self, topic: str, resume: bool = False) -> Dict[str, Any]:
        """Main generation loop"""
        
        # Step 1: Planning phase
        if not resume or not self.state.has_active_session():
            print(f"\n[Planner] Creating comprehensive outline for: {topic}")
            outline_result = self.planner.execute({'topic': topic})
            
            if not outline_result['success']:
                error_msg = outline_result.get('error', 'Unknown error creating outline')
                print(f"[Error] {error_msg}")
                if 'raw_response' in outline_result:
                    print(f"[Debug] Raw response: {outline_result['raw_response'][:500]}...")
                return {'success': False, 'error': error_msg}
            
            outline = outline_result['outline']
            fallback_used = outline_result.get('fallback_used', False)
            if fallback_used:
                print(f"[Planner] Used fallback outline with {outline_result['total_nodes']} nodes")
            else:
                print(f"[Planner] Created outline with {outline_result['total_nodes']} nodes")
            
            # Initialize state
            self.state.initialize_session(topic, self.model.model_name, outline)
            
            # Initialize tracker
            self.tracker.execute({'action': 'initialize', 'outline': outline})
        else:
            print(f"\n[Orchestrator] Resuming session for: {self.state.state['topic']}")
            outline = self.state.state['outline']
            
            # Restore tracker state
            self.tracker.covered_nodes = set(self.state.state.get('covered_nodes', []))
            self.tracker.pending_nodes = self.state.state.get('pending_nodes', [])
            self.tracker.covered_topics = self.state.state.get('covered_topics', [])
        
        # Step 2: Iterative generation loop
        self.iteration_count = 0
        
        while self.iteration_count < self.max_iterations:
            self.iteration_count += 1
            
            # Get next node
            next_result = self.tracker.execute({'action': 'get_next'})
            
            if not next_result['has_next']:
                print("\n[Orchestrator] All nodes processed")
                break
            
            node = next_result['node']
            print(f"\n[Iteration {self.iteration_count}] Processing: {node['title']} ({node['type']})")
            
            # Research phase
            print(f"[Researcher] Researching...")
            research_result = self.researcher.execute({
                'node': node,
                'parent_context': f"Topic: {topic}",
                'covered_topics': self.tracker.covered_topics
            })
            
            if not research_result['success']:
                print(f"[Error] Research failed for {node['title']}")
                continue
            
            raw_content = research_result['content']
            print(f"[Researcher] Generated {research_result['word_count']} words")
            
            # Review phase
            print(f"[Reviewer] Reviewing quality...")
            review_result = self.reviewer.execute({
                'content': raw_content,
                'title': node['title'],
                'min_length': self.min_section_length
            })
            
            review = review_result['review']
            print(f"[Reviewer] Quality score: {review['quality_score']}/100")
            
            # If not approved, expand
            if not review['approved'] or review.get('requires_expansion'):
                print(f"[Reviewer] Content needs expansion. Regenerating...")
                # Request deeper research
                research_result = self.researcher.execute({
                    'node': node,
                    'parent_context': f"Topic: {topic}\nPrevious attempt was too shallow. Provide much more depth.",
                    'covered_topics': self.tracker.covered_topics
                })
                raw_content = research_result['content']
            
            # Author phase
            print(f"[Author] Polishing content...")
            author_result = self.author.execute({
                'content': raw_content,
                'title': node['title'],
                'level': node['type']
            })
            
            final_content = author_result['polished_content']
            word_count = author_result['word_count']
            print(f"[Author] Final content: {word_count} words")
            
            # Save to storage
            filepath = self.storage.save_content(
                node['id'],
                node['title'],
                final_content,
                node['type']
            )
            print(f"[Storage] Saved to: {filepath}")
            
            # Update tracking
            self.tracker.execute({
                'action': 'mark_complete',
                'node_id': node['id'],
                'title': node['title']
            })
            
            self.state.mark_node_complete(node['id'], node['title'], word_count)
            
            # Show progress
            status = self.tracker.execute({'action': 'get_status'})['success'] and \
                     self.tracker.execute({'action': 'get_status'})
            if status:
                print(f"[Progress] {status['covered_count']}/{status['total_nodes']} nodes " +
                      f"({status['progress_percent']}%) - {self.state.state['total_word_count']} total words")
        
        # Step 3: Completion judgment
        print("\n[Completion Judge] Evaluating completeness...")
        coverage_status = self.state.get_status()
        
        judgment_result = self.judge.execute({
            'outline': outline,
            'coverage_status': coverage_status,
            'total_word_count': self.state.state['total_word_count']
        })
        
        judgment = judgment_result['judgment']
        print(f"[Completion Judge] Complete: {judgment['is_complete']}")
        print(f"[Completion Judge] Ready for PDF: {judgment['ready_for_pdf']}")
        print(f"[Completion Judge] Reasoning: {judgment['reasoning']}")
        
        if judgment['ready_for_pdf']:
            self.state.mark_complete()
            print("\n[Orchestrator] Generation complete! Ready for PDF compilation.")
            return {
                'success': True,
                'complete': True,
                'ready_for_pdf': True,
                'total_word_count': self.state.state['total_word_count'],
                'judgment': judgment
            }
        else:
            print("\n[Orchestrator] Generation incomplete. Remaining gaps:")
            for gap in judgment.get('remaining_gaps', []):
                print(f"  - {gap}")
            
            return {
                'success': True,
                'complete': False,
                'ready_for_pdf': False,
                'judgment': judgment
            }
