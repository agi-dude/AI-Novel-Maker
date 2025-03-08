import re

def remove_think_tags(text: str) -> str:
    """Remove thinking tags from text"""
    pattern = r"[\s\S]*?<\/think>\s*"
    return re.sub(pattern, "", text)
