"""
Helper utilities for Federal Academic Search MCP Server
"""
import re
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse


def normalize_doi(doi: str) -> str:
    """
    Normalize DOI to standard format.
    
    Args:
        doi: DOI string
        
    Returns:
        Normalized DOI
    """
    if not doi:
        return doi
        
    # Remove leading/trailing whitespace
    doi = doi.strip()
    
    # If it's a full URL, extract the DOI part
    if doi.startswith('http'):
        parsed = urlparse(doi)
        if 'doi.org' in parsed.netloc:
            # Extract DOI from path
            doi = parsed.path.lstrip('/')
        elif parsed.fragment:
            # DOI might be in fragment
            doi = parsed.fragment
        elif parsed.query:
            # DOI might be in query parameter
            if 'doi=' in parsed.query:
                doi = parsed.query.split('doi=')[1].split('&')[0]
    
    # Remove 'doi:' prefix if present
    if doi.lower().startswith('doi:'):
        doi = doi[4:]
        
    return doi


def extract_paper_id_from_url(url: str) -> str:
    """
    Extract paper ID from various URL formats.
    
    Args:
        url: URL string
        
    Returns:
        Extracted paper ID
    """
    if not url:
        return url
        
    # Remove leading/trailing whitespace
    url = url.strip()
    
    # Handle OpenAlex URLs
    if 'openalex.org' in url:
        return url.split('/')[-1]
    
    # Handle Semantic Scholar URLs
    if 'semanticscholar.org' in url:
        return url.split('/')[-1]
    
    # Handle arXiv URLs
    if 'arxiv.org' in url:
        return url.split('/')[-1]
    
    # Return as-is if no pattern matches
    return url


def sanitize_query(query: str) -> str:
    """
    Sanitize search query string.
    
    Args:
        query: Search query
        
    Returns:
        Sanitized query
    """
    if not query:
        return query
        
    # Remove excessive whitespace
    query = re.sub(r'\s+', ' ', query.strip())
    
    # Remove problematic characters that might break APIs
    query = re.sub(r'[^\w\s\-_"\'\(\)\[\]\{\}\.\,\:\;\!\?\+\=\*\#\@\$\%\^\&\<\>\/\\]', '', query)
    
    # Limit length to prevent overly long queries
    if len(query) > 500:
        query = query[:500]
        
    return query


def merge_paper_data(base_data: Dict[str, Any], 
                    additional_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge paper data from different sources, preferring non-null values.
    
    Args:
        base_data: Base paper data
        additional_data: Additional paper data to merge
        
    Returns:
        Merged paper data
    """
    if not additional_data:
        return base_data or {}
        
    if not base_data:
        return additional_data or {}
        
    merged = base_data.copy()
    
    for key, value in additional_data.items():
        # Only update if the additional value is not None/empty and base value is None/empty
        if value is not None and value != '':
            if merged.get(key) is None or merged.get(key) == '':
                merged[key] = value
                
    return merged


def format_authors(authors: List[str]) -> str:
    """
    Format list of authors into a readable string.
    
    Args:
        authors: List of author names
        
    Returns:
        Formatted author string
    """
    if not authors:
        return ""
        
    if len(authors) == 1:
        return authors[0]
    elif len(authors) == 2:
        return f"{authors[0]} and {authors[1]}"
    else:
        return f"{authors[0]} et al."


def estimate_reading_time(word_count: int) -> str:
    """
    Estimate reading time based on word count.
    
    Args:
        word_count: Number of words
        
    Returns:
        Reading time estimate
    """
    if not word_count:
        return "Unknown"
        
    # Average reading speed: 200 words per minute
    minutes = word_count // 200
    
    if minutes < 1:
        return "Less than 1 minute"
    elif minutes == 1:
        return "1 minute"
    else:
        return f"{minutes} minutes"


def is_valid_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
        
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
        
    return text[:max_length].rstrip() + "..."


# Export all functions
__all__ = [
    'normalize_doi',
    'extract_paper_id_from_url',
    'sanitize_query',
    'merge_paper_data',
    'format_authors',
    'estimate_reading_time',
    'is_valid_email',
    'truncate_text'
]