import os
import json
from typing import Dict, Any
from datetime import datetime


class StorageManager:
    """Manages file storage for generated content"""
    
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.content_dir = os.path.join(base_dir, 'content')
        self.metadata_file = os.path.join(base_dir, 'metadata.json')
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure storage directories exist"""
        os.makedirs(self.content_dir, exist_ok=True)
    
    def save_content(self, node_id: str, title: str, content: str, node_type: str) -> str:
        """Save content to disk and return file path"""
        # Sanitize filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')
        
        filename = f"{node_id}_{safe_title}.txt"
        filepath = os.path.join(self.content_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"Type: {node_type}\n")
                f.write(f"ID: {node_id}\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n")
                f.write(f"\n{'='*80}\n\n")
                f.write(content)
            
            return filepath
        except Exception as e:
            raise RuntimeError(f"Failed to save content: {e}")
    
    def load_content(self, node_id: str) -> str:
        """Load content from disk"""
        # Find file by node_id prefix
        for filename in os.listdir(self.content_dir):
            if filename.startswith(node_id):
                filepath = os.path.join(self.content_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
        raise FileNotFoundError(f"Content for node {node_id} not found")
    
    def get_all_content_files(self) -> list:
        """Get all content files in order"""
        files = []
        for filename in sorted(os.listdir(self.content_dir)):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.content_dir, filename)
                files.append(filepath)
        return files
    
    def save_metadata(self, metadata: Dict[str, Any]):
        """Save metadata"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"Failed to save metadata: {e}")
    
    def load_metadata(self) -> Dict[str, Any]:
        """Load metadata"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def clear_storage(self):
        """Clear all stored content"""
        import shutil
        if os.path.exists(self.base_dir):
            shutil.rmtree(self.base_dir)
        self._ensure_directories()
