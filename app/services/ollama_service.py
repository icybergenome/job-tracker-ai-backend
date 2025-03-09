from ollama import Client
import json
from app import app

ollama_client = Client(host=app.config['OLLAMA_URL'])

def evaluate_job(job, profile_details):
    prompt = f"""
    Evaluate the following job based on my skills and abilities:
    My Details: {json.dumps(profile_details, indent=2)}
    Job Details: {json.dumps(job, indent=2)}

    Output must be in json format and must have following info:
    1. Relevancy of the job (High, Medium, Low, Irrelevant)
    2. Brief Summary about the job
    3. Important key points about the job such as based on my skills and abilities should I apply for this job or not
    Example:
    {{
        "relevancy": "High",
        "summary": "This job is really interesting and relevant. Client is looking for a Full stack developer .....",
        "keyPoints": Array of Objects with keys such as: point and reason
    }}
    """
    
    response = ollama_client.generate(model=app.config['MODEL_NAME'], prompt=prompt)
    return response['response']

def generate_proposal(job, profile_details):
    prompt = f"""
    Generate a detailed proposal for the following job based on my skills and abilities:
    My Details: {json.dumps(profile_details, indent=2)}
    Job to apply for: {json.dumps(job, indent=2)}

    Proposal should be in json format and must be covering following details:
    1. Talk about project details
    2. Ask relevant questions
    3. Propose technologies relevant to the job and my skills
    """
    
    response = ollama_client.generate(model=app.config['MODEL_NAME'], prompt=prompt)
    return response['response']