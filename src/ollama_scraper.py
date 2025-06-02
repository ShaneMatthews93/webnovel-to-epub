import requests

def ask_llama(prompt, model='llama3'):
    
    response = requests.post(
        "http://10.0.0.100:11434/api/generate",
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
    
def extract_with_ai(html, model='llama3'):
    prompt = f"""
    You are an intelligent HTML parser. Your task is to extract the *title* and *main content* from a novel chapter's HTML page. Ignore navigation bars, ads, comments, or unrelated content.
    You should extract the full chapter and not just an excerpt.
    Return the result in **exactly** this JSON format:
    {{
        'title': '...',
        'content': '...'
    }}
    
    HTML:
    {html}
    
    """
    result = ask_llama(prompt=prompt, model=model)
    
    if result:
        print(result)
        return result
    else:
        print("Failed Ask Ollama Operation")
        return None
    