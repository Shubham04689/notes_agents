from typing import Dict, Any, List, Set
from .base import BaseAgent


class CoverageTrackerAgent(BaseAgent):
    """Agent responsible for tracking what has been covered and what remains"""
    
    def __init__(self, model):
        super().__init__(model, "Coverage Tracker")
        self.covered_nodes: Set[str] = set()
        self.pending_nodes: List[Dict[str, Any]] = []
        self.covered_topics: List[str] = []
    
    def _get_system_prompt(self) -> str:
        return """You are a meticulous tracking and organization specialist. Your role is to maintain perfect records of what has been covered and what remains to be addressed.

You must:
1. Track every completed topic precisely
2. Identify all remaining topics
3. Detect any gaps or omissions
4. Prevent duplication
5. Ensure comprehensive coverage
6. Maintain clear status of progress"""
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Update coverage tracking"""
        action = context.get('action')
        
        if action == 'initialize':
            return self._initialize_tracking(context)
        elif action == 'mark_complete':
            return self._mark_complete(context)
        elif action == 'get_next':
            return self._get_next_node(context)
        elif action == 'get_status':
            return self._get_status(context)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _initialize_tracking(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize tracking from outline"""
        outline = context.get('outline')
        if not outline:
            raise ValueError("Outline required for initialization")
        
        self.covered_nodes.clear()
        self.pending_nodes.clear()
        self.covered_topics.clear()
        
        # Flatten outline into pending nodes
        for chapter in outline.get('chapters', []):
            self.pending_nodes.append({
                'id': chapter['id'],
                'title': chapter['title'],
                'type': 'chapter',
                'parent': None
            })
            
            for section in chapter.get('sections', []):
                self.pending_nodes.append({
                    'id': section['id'],
                    'title': section['title'],
                    'type': 'section',
                    'parent': chapter['id']
                })
                
                for subsection in section.get('subsections', []):
                    self.pending_nodes.append({
                        'id': subsection['id'],
                        'title': subsection['title'],
                        'type': 'subsection',
                        'parent': section['id']
                    })
        
        return {
            'success': True,
            'total_nodes': len(self.pending_nodes),
            'pending_count': len(self.pending_nodes)
        }
    
    def _mark_complete(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Mark a node as complete"""
        node_id = context.get('node_id')
        title = context.get('title')
        
        if not node_id:
            raise ValueError("node_id required")
        
        self.covered_nodes.add(node_id)
        if title:
            self.covered_topics.append(title)
        
        # Remove from pending
        self.pending_nodes = [n for n in self.pending_nodes if n['id'] != node_id]
        
        return {
            'success': True,
            'covered_count': len(self.covered_nodes),
            'pending_count': len(self.pending_nodes)
        }
    
    def _get_next_node(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get the next node to process"""
        if not self.pending_nodes:
            return {
                'success': True,
                'has_next': False,
                'node': None
            }
        
        # Return first pending node
        next_node = self.pending_nodes[0]
        
        return {
            'success': True,
            'has_next': True,
            'node': next_node
        }
    
    def _get_status(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get current tracking status"""
        total = len(self.covered_nodes) + len(self.pending_nodes)
        progress = len(self.covered_nodes) / total if total > 0 else 0
        
        return {
            'success': True,
            'total_nodes': total,
            'covered_count': len(self.covered_nodes),
            'pending_count': len(self.pending_nodes),
            'progress_percent': round(progress * 100, 2),
            'covered_topics': self.covered_topics[-10:],  # Last 10
            'next_pending': self.pending_nodes[:5] if self.pending_nodes else []
        }
