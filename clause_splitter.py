import re

def split_clauses(text):
    # Regex explanations:
    # \n\d+\.       -> Matches English numbering (e.g., "1.")
    # \n[१-९]+\.    -> Matches Hindi numbering (e.g., "१.")
    # \n[A-Z\u0900-\u097F]+: -> Matches Headers in English or Hindi ending with ':'
    # \([a-z]\)     -> Matches sub-clauses like "(a)", "(b)"
    
    pattern = r'\n\d+\.|\n[१-९]+\.|\n[A-Z\u0900-\u097F ]+:|\n\([a-z]\)'
    
    clauses = re.split(pattern, text)
    
    # Filter out empty strings or very short fragments (less than 10 chars)
    # This removes noise like page numbers or header fragments
    return [c.strip() for c in clauses if len(c.strip()) > 10]