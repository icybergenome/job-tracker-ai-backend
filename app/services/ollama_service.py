from ollama import Client
import json
from app import app
from pydantic import BaseModel

class BasicJobEvaluation(BaseModel):
    relevancy: str

class DetailJobEvaluation(BaseModel):
    summary: str
    keyPoints: list
 
class Proposal(BaseModel):
    proposal: str

ollama_client = Client(host=app.config['OLLAMA_URL'])

def basic_evaluate_job(job, profile_details):
    prompt = f"""
    Evaluate the following job based on Profiles skills and abilities:
        - Profiles: {json.dumps(profile_details, indent=2)}
        - Details of potential Job: {json.dumps(job, indent=2)}

    Output must be in json format and must have following info:
    1. Relevancy of the job (High, Medium, Low, Irrelevant)
    While evaluating the job, consider following factors:
    - Provided 2 profiles one for developer and other for designer. Use the profile relevancy to decide the relevancy of the job
    - Match Technologies mention in profiles and technologies require in this job:
        - If some major skills are missing from profiles then job is irrelevant. Lets say a job is not relevant if it requires PHP expertise but profiles does not have PHP expertise then job is irrelevant
        - Similarly we provide the custom development solutions so jobs like Wordpress, Shopify, Magento, Prestashop are not relevant
    From the job details above pay special attention to following field:
        - jobType: This field shows the budget and type of job(i.e. fixed or hourly) If budget matches the effort required in the job then job is relevant
        - clientRating: clients with higher rating are more relevant
        - clientSpendings: higher spendings are more relevant
        - clientCountry:
            - clients from richer countries are more relevant and easy to work with i.e. Clients from India, Pakistan and similar countries are not relevant
    Example:
    {{
        "relevancy": "High"
    }}
    """
    print("Making request to Ollama... for job evaluation", job['jobTitle'])
    response = ollama_client.generate(model=app.config['EVALUATION_MODEL_NAME'], prompt=prompt, format=BasicJobEvaluation.model_json_schema())
    tokens_per_s = response['eval_count']/response['eval_duration'] * 10**9
    print(f"Response from Ollama generated {response['eval_count']} tokens using {tokens_per_s} tokens per second")
    
    return response['response']

def detail_evaluate_job(job, profile_details):
    prompt = f"""
    Evaluate the following job based on Profiles skills and abilities:
        - Profiles: {json.dumps(profile_details, indent=2)}
        - Details of potential Job:
            ```
            Title: {job['jobTitle']}
            Description: {job['jobDescription']}
            Client Rating: {job.get('clientRating', '')}
            Client Spending: {job.get('clientSpendings', '')}
            Client Country: {job.get('clientCountry', '')}
            Job Type and Budget: {job.get('jobType', '')}
            ```

    Output must be in json format and must have following info:
    1. Brief Summary about the job
    2. Important key points about the job such as based on my skills and abilities should I apply for this job or not
    While evaluating the job, consider following factors:
    - Provided 2 profiles one for developer and other for designer. Use the profile relevancy to decide the relevancy of the job
    - Match Technologies mention in profiles and technologies require in this job:
        - If some major skills are missing from profiles then job is irrelevant. Lets say a job is not relevant if it requires PHP expertise but profiles does not have PHP expertise then job is irrelevant
        - Similarly we provide the custom development solutions so jobs like Wordpress, Shopify, Magento, Prestashop are not relevant
    From the job details above pay special attention to following field:
    - Job Type and Budget: This field shows the budget and type of job(i.e. fixed or hourly). If budget matches the effort required in the job then job is relevant
    - Client Rating: clients with higher rating are more relevant
    - Client Spending: higher spendings are more relevant
    - Client Country:
        - clients from richer countries are more relevant and easy to work with i.e. Clients from India, Pakistan and similar countries are not relevant
    Example:
    {{
        "summary": "This job is really interesting and relevant. Client is looking for a Full stack developer .....",
        "keyPoints": Array of Objects with keys such as: point and reason
    }}
    """
    print("Making request to Ollama... for job evaluation", job['jobTitle'])
    response = ollama_client.generate(model=app.config['EVALUATION_MODEL_NAME'], prompt=prompt, format=DetailJobEvaluation.model_json_schema())
    tokens_per_s = response['eval_count']/response['eval_duration'] * 10**9
    print(f"Response from Ollama generated {response['eval_count']} tokens using {tokens_per_s} tokens per second")
    return response['response']

def generate_proposal(job, profile_details, related_past_projects):
    prompt = f"""
    I want to apply for following job post as a Freelancer:
        ```
        Title: {job['jobTitle']}
        Description: {job['jobDescription']}
        ```
    
    Help me write a Job proposal based on my skills which are as follow:
        Profiles of person to apply: {json.dumps(profile_details, indent=2)}
        My Related Past Projects: {json.dumps(related_past_projects, indent=2)}

    Proposal should be covering following details:
        - Proposal should be professional with perfect structure
        - In a proposal talk about project details
        - Ask relevant questions where needed
        - Propose technologies relevant to the job and my skills
        - Give reference of related past projects if necessary 
    """
    print("Making request to Ollama... for job proposal", job['jobTitle'])
    response = ollama_client.generate(model=app.config['PROPOSAL_MODEL_NAME'], prompt=prompt, format=Proposal.model_json_schema())
    tokens_per_s = response['eval_count']/response['eval_duration'] * 10**9
    print(f"Response from Ollama generated {response['eval_count']} tokens using {tokens_per_s} tokens per second")
    return response['response']