import json
import os
from pathlib import Path
from typing import Dict, Optional


class ConfigManager:
    def __init__(self):
        self.claude_dir = Path(".claude")
        self.settings_file = "settings.local.json"
        self.settings_path = self.claude_dir / self.settings_file
    
    def ensure_claude_directory(self):
        """Ensure .claude directory exists"""
        self.claude_dir.mkdir(exist_ok=True)
    
    def save_settings(self, settings: Dict[str, str]):
        """Save settings to .claude/settings.local.json"""
        self.ensure_claude_directory()
        
        # Load existing settings if file exists
        existing_settings = self.load_settings() or {}
        
        # Update with new settings
        existing_settings.update(settings)
        
        # Write to file
        with open(self.settings_path, 'w') as f:
            json.dump(existing_settings, f, indent=2)
    
    def load_settings(self) -> Optional[Dict[str, str]]:
        """Load settings from .claude/settings.local.json"""
        if not self.settings_path.exists():
            return None
        
        try:
            with open(self.settings_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def reset_settings(self):
        """Remove the settings file"""
        if self.settings_path.exists():
            self.settings_path.unlink()