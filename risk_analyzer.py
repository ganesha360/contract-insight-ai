import google.generativeai as genai
import json
import streamlit as st

# Configure your API Key securely using Streamlit Secrets
# Create .streamlit/secrets.toml and add: GEMINI_API_KEY = "your_key"
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    # Fallback for local testing if secrets are not set
    genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")

model = genai.GenerativeModel('gemini-pro')

def analyze_clause(clause, language="English"):
    """
    Analyzes a contract clause using AI with a focus on Indian legal standards.
    Supports both English and Hindi text.
    """
    
    # Enhanced prompt for higher accuracy and legal grounding
    prompt = f"""
    Act as a senior legal counsel specializing in Indian Law (e.g., Indian Contract Act, 1872). 
    Analyze the following contract clause accurately.
    
    The analysis must be provided in {language}, but if the input is in Hindi, 
    the explanation should include Hindi legal terms for better understanding.
    
    Provide:
    1. risk: Categorize as 'High', 'Medium', or 'Low'.
    2. explanation: A detailed legal reasoning of why this is a risk.
    3. suggestion: Specific actionable advice to mitigate the risk or renegotiate.
    
    Clause: {clause}
    
    Return the response ONLY in this exact JSON format:
    {{
        "risk": "High/Medium/Low",
        "explanation": "Detailed reasoning here",
        "suggestion": "Actionable fix here"
    }}
    """
    
    try:
        # Request content from Gemini
        response = model.generate_content(prompt)
        
        # Clean the response text to ensure valid JSON parsing
        # AI sometimes wraps JSON in markdown blocks (```json ... ```)
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        
        # Parse and return the JSON data
        analysis_result = json.loads(clean_text)
        return analysis_result

    except Exception as e:
        # Robust Fallback: If AI fails or API limit is reached, return a safe default
        return {
            "risk": "Medium",
            "explanation": "AI Analysis encountered an error. Please review this clause manually for termination or liability traps.",
            "suggestion": "Consult with a legal professional to ensure this clause complies with standard local regulations."
        }