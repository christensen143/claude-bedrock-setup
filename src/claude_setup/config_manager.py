from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional


class ConfigManager:
    def __init__(self) -> None:
        self.claude_dir = Path(".claude")
        self.settings_file = "settings.local.json"
        self.settings_path = self.claude_dir / self.settings_file

    def ensure_claude_directory(self) -> None:
        """Ensure .claude directory exists"""
        self.claude_dir.mkdir(exist_ok=True)

    def save_settings(self, settings: Dict[str, str]) -> None:
        """Save settings to .claude/settings.local.json"""
        self.ensure_claude_directory()

        # Create the env wrapper structure
        env_wrapper = {"env": settings}

        # Write to file
        with open(self.settings_path, "w") as f:
            json.dump(env_wrapper, f, indent=2)

    def load_settings(self) -> Optional[Dict[str, str]]:
        """Load settings from .claude/settings.local.json"""
        if not self.settings_path.exists():
            return None

        try:
            with open(self.settings_path, "r") as f:
                content = json.load(f)
                # Handle new format with env wrapper
                if isinstance(content, dict) and "env" in content:
                    return content["env"]  # type: ignore[no-any-return]
                # Handle legacy format (direct settings)
                return content  # type: ignore[no-any-return]
        except (json.JSONDecodeError, IOError):
            return None

    def reset_settings(self) -> None:
        """Remove the settings file"""
        if self.settings_path.exists():
            self.settings_path.unlink()
