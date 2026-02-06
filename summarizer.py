def generate_summary(full_text):
    prompt = f"""
    Summarize this contract in 5 bullet points. 
    Focus on:
    - Parties involved
    - Key obligations
    - Payment terms
    - Termination rights
    - Major risks
    
    Contract Text: {full_text[:10000]} # Limit text for API
    """
    response = model.generate_content(prompt)
    return response.text