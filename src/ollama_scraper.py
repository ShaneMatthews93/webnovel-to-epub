import requests

def ask_llama(prompt, model='tinyllama'):
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False  # Set to True for streaming output
        }
    )
    
    if response.status_code == 200:
        return response.json()['response']
    else:
        print("Error: ", response.text)
        return None
    
def extract_with_ai(html, model='tinyllama'):
    prompt = f"""
    You are an intelligent HTML parser. Your task is to extract the *title* and *main content* from a novel chapter's HTML page. Ignore navigation bars, ads, comments, or unrelated content.

    Return the result in **exactly** this JSON format:
    {{
        'title': '...',
        'content': '...'
    }}
    
    HTML:
    {html}
    
    """
    response = ask_llama(prompt=prompt, model='tinyllama')
    
    try:
        result = response.json().get('response', "").strip()
        print(result)
    except Exception as e:
        print("Failed Ask Ollama Operation")
        return None
    
    