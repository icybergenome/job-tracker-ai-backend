import datetime
import os
from dotenv import load_dotenv
from pprint import pprint
import ollama
import json
# import gspread
# import google.auth
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
from flask import Flask, request, jsonify

from pydantic import BaseModel


load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Your details
my_details = {
    "Name": "Bilal Saeed",
    "Technical Niche": "Full stack web and mobile development",
    "Languages": ["Typescript", "JavaScript", "Python", "Rails"],
    "Frameworks and libraries": ["NextJS", "ReactJS", "ExpressJS", "Flask", "Ruby on Rails"],
    "Cloud": ["Firebase", "SupaBase", "AWS(EC2, lightsail, s3, step functions, cdk, cognito, Lambda, Cloudfront, Amplify)", "Hetzner", "Google Cloud Platform"]
}

MODEL_NAME = os.getenv("MODEL_NAME")
# Google Sheets setup
SHEET_ID = os.getenv("SHEET_ID")
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class JobEvaluation(BaseModel):
    relevancy: str
    summary: str
    keyPoints: list

class Proposal(BaseModel):
    proposal: str

# Function to evaluate job relevancy and extract key points
def evaluate_job(job, my_details):
    prompt = f"""
    Evaluate the following job based on my skills and abilities:
    My Details: {json.dumps(my_details, indent=2)}
    Job Details: {json.dumps(job, indent=2)}

    Output must be in json format and must have following info:
    1. Relevancy of the job (High, Medium, Low)
    2. Summary 
    3. Key Points of the job
    Example:
    {{
        "relevancy": "High",
        "summary": "This job is really interesting and relevant. Client is looking for a Full stack developer .....",
        "keyPoints": {"Keypoint1", "Keypoint2", "Keypoint3"}
    }}
    """
    
    response = ollama.generate(model=MODEL_NAME, prompt=prompt, format=JobEvaluation.model_json_schema())
    evaluation = response['response']
    
    return evaluation

# Function to generate an ideal proposal
def generate_proposal(job, my_details):
    prompt = f"""
    Generate an ideal proposal for the following job based on my skills and abilities:
    My Details: {json.dumps(my_details, indent=2)}
    Job Details: {json.dumps(job, indent=2)}

    Proposal should be in json format and must be covering following details:
    1. Talk about project details
    2. Ask relevant questions
    3. Propose technologies relevant to the job and my skills

    Example:
    {{
        "proposal": "Hi Eric! I see you are looking for a Fullstack developer. Let's have a chat about the project details..."
    }}
    """
    
    response = ollama.generate(model=MODEL_NAME, prompt=prompt, format=Proposal.model_json_schema())
    proposal = response['response']
    
    return proposal

# Function to save data to Google Sheets
def save_to_google_sheets(job, evaluation, proposal):
    try:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('credentials_oauth.json'):
            creds = Credentials.from_authorized_user_file('credentials_oauth.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials_oauth.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('credentials_oauth.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)

        row = [
            job.get("jobUrl", ""),
            job.get("jobTitle", ""),
            job.get("postedOn", ""),
            job.get("jobType", ""),
            job.get("contractorTier", ""),
            job.get("duration", ""),
            job.get("jobDescription", ""),
            ", ".join(job.get("skills", [])),
            job.get("paymentVerified", ""),
            str(job.get("clientRating", "")),
            job.get("clientSpendings", ""),
            job.get("clientCountry", ""),
            job.get("proposals", ""),
            # json.dumps(evaluation),
            # json.dumps(proposal)
            evaluation.get("relevancy", "") if evaluation and "relevancy" in evaluation else "",
            evaluation.get("summary", "") if evaluation and "summary" in evaluation else "",
            ", ".join(evaluation.get("keyPoints", [])) if evaluation and "keyPoints" in evaluation else "",
            proposal.get("proposal", "") if "proposal" in proposal else "",
            # current date and time
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        print("Saving data to Google Sheets...")
        pprint(row)
        body = {"values": [row]}
        # append the row to the sheet
        result = service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range="DevJobs!A:R",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        # sheet = service.spreadsheets()
        # sheet.values().append(
        #     spreadsheetId=SHEET_ID,
        #     range="Sheet1!A1:O1",
        #     valueInputOption="USER_ENTERED",
        #     insertDataOption="INSERT_ROWS",
        #     body={"values": [row]}
        # )
        print("Data saved to Google Sheets successfully!", result)
    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")

# API endpoint to process jobs
@app.route('/evaluate-jobs', methods=['POST'])
def evaluate_jobs():
    try:
        jobs_data = request.json  # Get job data from the request body
        pprint(jobs_data)
        relevant_jobs = []
        
        for job in jobs_data:
            evaluation = evaluate_job(job, my_details)
            print(f"Evaluation for Job: {job['jobTitle']}")
            pprint(evaluation)

            # extract json output from evaluation
            evaluation_output = json.loads(evaluation)
            print("Evaluation Output:")
            pprint(evaluation_output)
            # empty proposal variable to be populated in the next step
            proposal_output = ""
            
            if "High" in evaluation_output['relevancy']:
                proposal = generate_proposal(job, my_details)
                print(f"\nProposal for Job: {job['jobTitle']}")
                pprint(proposal)

                proposal_output = json.loads(proposal)
                
                relevant_jobs.append({
                    "job": job,
                    "evaluation": evaluation_output,
                    "proposal": proposal
                })
            
            # Save job, evaluation, and proposal to Google Sheets
            save_to_google_sheets(job, evaluation_output, proposal_output)
        
        return jsonify({"message": "Jobs processed successfully!", "relevant_jobs": relevant_jobs}), 200
    except Exception as e:
        print(f"Error processing jobs: {e}")
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5001)