from pathlib import Path


def ensure_gitignore():
    """Ensure .claude/settings.local.json is in .gitignore"""
    gitignore_path = Path(".gitignore")
    claude_settings_pattern = ".claude/settings.local.json"
    
    # Read existing .gitignore content
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            content = f.read()
            lines = content.strip().split('\n') if content.strip() else []
    else:
        lines = []
    
    # Check if pattern already exists
    if claude_settings_pattern not in lines:
        # Add the pattern
        lines.append(claude_settings_pattern)
        
        # Write back to .gitignore
        with open(gitignore_path, 'w') as f:
            f.write('\n'.join(lines) + '\n')