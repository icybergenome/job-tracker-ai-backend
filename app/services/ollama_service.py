from ollama import Client
import json
from app import app
from pydantic import BaseModel

class JobEvaluation(BaseModel):
    relevancy: str
    summary: str
    keyPoints: list
 
class Proposal(BaseModel):
    proposal: str

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
    print("Making request to Ollama... for job evaluation", job['jobTitle'])
    response = ollama_client.generate(model=app.config['MODEL_NAME'], prompt=prompt, format=JobEvaluation.model_json_schema())
    tokens_per_s = response['eval_count']/response['eval_duration'] * 10^9
    print(f"Response from Ollama generated {response['eval_count']} tokens in {response['eval_duration']} seconds. {tokens_per_s} tokens per second")
    
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
    print("Making request to Ollama... for job proposal", job['jobTitle'])
    response = ollama_client.generate(model=app.config['MODEL_NAME'], prompt=prompt, format=Proposal.model_json_schema())
    tokens_per_s = response['eval_count']/response['eval_duration'] * 10^9
    print(f"Response from Ollama generated {response['eval_count']} tokens in {response['eval_duration']} seconds. {tokens_per_s} tokens per second")
    return response['response']