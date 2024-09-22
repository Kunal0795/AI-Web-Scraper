from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import requests

# Template for extracting specific information
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# API endpoint for gemma2:2b
url = "http://localhost:11434/api/chat"

# if you are using any other model than change the "Model name" with that 
def gemma2(prompt):
    data = {
        "model": "gemma2:2b",  # Model name
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }
    headers = {
        'Content-Type': 'application/json'
    }

    # sending a post request to model
    response = requests.post(url, headers=headers, json=data)
    return response.json().get('message', {}).get('content', '')

def parse_with_ollama(dom_chunks, parse_description):
    prompt_template = ChatPromptTemplate.from_template(template)

    # define a list to store parsed results
    parsed_results = []

    # loop each DOM chunk and parse it
    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = prompt_template.format(dom_content=chunk, parse_description=parse_description)

        # send promt to gemma2 and get it stored in responde
        response = gemma2(prompt)
        
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        
        parsed_results.append(response)

    # join all the parsed results and return it
    return "\n".join(parsed_results)

