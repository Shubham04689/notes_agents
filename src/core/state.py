import json
import os
from typing import Dict, Any, Optional
from datetime import datetime


class StateManager:
    """Manages persistent state across sessions"""
    
    def __init__(self, state_file: str):
        self.state_file = state_file
        self.state: Dict[str, Any] = {}
        self._load_state()
    
    def _load_state(self):
        """Load state from disk"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    self.state = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load state: {e}")
                self.state = {}
        else:
            self.state = {}
    
    def save_state(self):
        """Save state to disk"""
        try:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"Failed to save state: {e}")
    
    def initialize_session(self, topic: str, model_name: str, outline: Dict[str, Any]):
        """Initialize a new session"""
        self.state = {
            'topic': topic,
            'model_name': model_name,
            'outline': outline,
            'covered_nodes': [],
            'pending_nodes': self._flatten_outline(outline),
            'covered_topics': [],
            'total_word_count': 0,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'status': 'in_progress'
        }
        self.save_state()
    
    def _flatten_outline(self, outline: Dict[str, Any]) -> list:
        """Flatten outline into list of nodes"""
        nodes = []
        for chapter in outline.get('chapters', []):
            nodes.append({
                'id': chapter['id'],
                'title': chapter['title'],
                'type': 'chapter'
            })
            for section in chapter.get('sections', []):
                nodes.append({
                    'id': section['id'],
                    'title': section['title'],
                    'type': 'section'
                })
                for subsection in section.get('subsections', []):
                    nodes.append({
                        'id': subsection['id'],
                        'title': subsection['title'],
                        'type': 'subsection'
                    })
        return nodes
    
    def mark_node_complete(self, node_id: str, title: str, word_count: int):
        """Mark a node as complete"""
        self.state['covered_nodes'].append(node_id)
        self.state['covered_topics'].append(title)
        self.state['pending_nodes'] = [
            n for n in self.state['pending_nodes'] if n['id'] != node_id
        ]
        self.state['total_word_count'] += word_count
        self.state['updated_at'] = datetime.now().isoformat()
        self.save_state()
    
    def get_next_node(self) -> Optional[Dict[str, Any]]:
        """Get next pending node"""
        if self.state.get('pending_nodes'):
            return self.state['pending_nodes'][0]
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        total = len(self.state.get('covered_nodes', [])) + len(self.state.get('pending_nodes', []))
        covered = len(self.state.get('covered_nodes', []))
        progress = (covered / total * 100) if total > 0 else 0
        
        return {
            'topic': self.state.get('topic'),
            'total_nodes': total,
            'covered_count': covered,
            'pending_count': len(self.state.get('pending_nodes', [])),
            'progress_percent': round(progress, 2),
            'total_word_count': self.state.get('total_word_count', 0),
            'status': self.state.get('status', 'unknown')
        }
    
    def mark_complete(self):
        """Mark session as complete"""
        self.state['status'] = 'complete'
        self.state['completed_at'] = datetime.now().isoformat()
        self.save_state()
    
    def clear_state(self):
        """Clear current state"""
        self.state = {}
        self.save_state()
    
    def has_active_session(self) -> bool:
        """Check if there's an active session"""
        return bool(self.state and self.state.get('status') == 'in_progress')
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get session information"""
        return {
            'topic': self.state.get('topic'),
            'model': self.state.get('model_name'),
            'created_at': self.state.get('created_at'),
            'status': self.state.get('status')
        }
