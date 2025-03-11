import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
from app import app

def get_auth():
    try:
        creds = None
        if os.path.exists('credentials_oauth.json'):
            creds = Credentials.from_authorized_user_file('credentials_oauth.json', app.config['SCOPES'])
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials_oauth.json', app.config['SCOPES'])
                creds = flow.run_local_server(port=0)
            with open('credentials_oauth.json', 'w') as token:
                token.write(creds.to_json())
        return creds
    except Exception as e:
        print(f"Auth Error: {e}")

def save_to_google_sheets(job, evaluation, proposal, sheet_name):
    try:
        creds = get_auth()

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
            evaluation.get("relevancy", "") if evaluation and "relevancy" in evaluation else "",
            evaluation.get("summary", "") if evaluation and "summary" in evaluation else "",
            ", ".join([f"{keyPoint.get('point', '')} - {keyPoint.get('reason', '')}" for keyPoint in evaluation.get("keyPoints", [])]) if evaluation and "keyPoints" in evaluation else "",
            proposal.get("proposal", "") if "proposal" in proposal else "",
            datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        ]
        body = {"values": [row]}
        result = service.spreadsheets().values().append(
            spreadsheetId=app.config['SHEET_ID'],
            range=sheet_name+"!A:R",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        print("Data saved to Google Sheets successfully!", result)
        return result['updates']['updatedRange']
    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")

def read_from_row_address(row_address):
    try:
        creds = get_auth()
        service = build('sheets', 'v4', credentials=creds)
        result = service.spreadsheets().values().get(
            spreadsheetId=app.config['SHEET_ID'],
            range=row_address
        ).execute()
        return result.get('values', [])
    except Exception as e:
      print(f"Error retrieving row data: {e}")
      
def save_proposal_in_proposal_sheet(jobAddress, proposal):
    try:
        creds = get_auth()
        service = build('sheets', 'v4', credentials=creds)
        sheet_name = "Proposals"
        values = [
            [jobAddress, proposal.get("proposal", "")]
        ]
        body = {"values": values}
        result = service.spreadsheets().values().append(
            spreadsheetId=app.config['SHEET_ID'],
            range=sheet_name+"!A:B",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        print("Proposal saved to Proposals Sheet successfully!", result)
        return result['updates']['updatedRange']
    except Exception as e:
        print(f"Error saving proposal to Proposals Sheet: {e}")

