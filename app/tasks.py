from app.services.ollama_service import evaluate_job, generate_proposal
from app.services.google_sheets import save_to_google_sheets
from app.services.notifications import send_slack_notification
import json

def process_job(job, profile_details, sheet_name):
    try:
      evaluation = evaluate_job(job, profile_details)
      print(f"Evaluation for Job: {job['jobTitle']}")
      evaluation_output = json.loads(evaluation)
      proposal_output = ""
      
      if "High" in evaluation_output['relevancy']:
          proposal = generate_proposal(job, profile_details)
          proposal_output = json.loads(proposal)
      
      # Save job, evaluation, and proposal to Google Sheets
      save_to_google_sheets(job, evaluation_output, proposal_output, sheet_name)
      send_slack_notification(job["jobTitle"], job["jobUrl"], job["jobDescription"], evaluation_output)
    except JobTimeoutException:
       print("Job processing timed out.")