from django import template
import re

register = template.Library()

@register.filter
def youtube_id(url):
    """
    Extracts the YouTube video ID from a URL.
    """
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return ""
