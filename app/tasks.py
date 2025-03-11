from pprint import pprint
from app.services.ollama_service import basic_evaluate_job, detail_evaluate_job, generate_proposal
from app.services.google_sheets import save_to_google_sheets, read_from_row_address, save_proposal_in_proposal_sheet
from app.services.notifications import send_slack_notification
import json

def process_job(job, profile_details, sheet_name):
    basic_evaluation = basic_evaluate_job(job, profile_details)
    print(f"Basic Evaluation for Job: {job['jobTitle']}, Done ✅", basic_evaluation)
    evaluation_output = json.loads(basic_evaluation)

    if "High" in evaluation_output['relevancy']:
        detail_evaluation = detail_evaluate_job(job, profile_details)
        print(f"Detail Evaluation for Job: {job['jobTitle']}, Done ✅")
        detail_evaluation_output = json.loads(detail_evaluation)
        evaluation_output = {**evaluation_output, **detail_evaluation_output}	
        print(f"Final Evaluation for Job: {job['jobTitle']}, Done ✅", evaluation_output)   
    else:
        evaluation_output['summary'] = ""
        evaluation_output['keyPoints'] = []
        
    proposal_output = ""
        
    # if "High" in evaluation_output['relevancy']:
    #     proposal = generate_proposal(job, profile_details)
    #     proposal_output = json.loads(proposal)
    
    # Save job, evaluation, and proposal to Google Sheets
    range_info = save_to_google_sheets(job, evaluation_output, proposal_output, sheet_name)
    send_slack_notification(job["jobTitle"], job["jobUrl"], job["jobDescription"], evaluation_output, range_info)

def generate_job_proposal(jobAddress, profile_details, related_past_projects):
    print("Getting Data for ", jobAddress)
    pprint(profile_details)
    rows = read_from_row_address(jobAddress)
    row_data = rows[0]
    job = {
        "jobUrl": row_data[0],
        "jobTitle": row_data[1],
        "postedOn": row_data[2],
        "jobType": row_data[3],
        "contractorTier": row_data[4],
        "duration": row_data[5],
        "jobDescription": row_data[6],
        "skills": row_data[7].split(", "),
        "paymentVerified": row_data[8],
        "clientRating": float(row_data[9]) if row_data[9] else None,
        "clientSpendings": row_data[10],
        "clientCountry": row_data[11]
    }
    proposal = generate_proposal(job, profile_details, related_past_projects)
    proposal_output = json.loads(proposal)
    save_proposal_in_proposal_sheet(jobAddress, proposal_output)