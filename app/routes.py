from flask import request, jsonify
from app import app, queue
from app.tasks import process_job, generate_job_proposal

@app.route('/evaluate-jobs', methods=['POST'])
def evaluate_jobs():
    try:
        payload = request.json
        profile_details = payload.get('profileDetails', {})
        jobs_data = payload.get('jobs', [])
        sheet_name = payload.get('sheetName', "DevJobs")
        
        # Enqueue each job for background processing
        for job in jobs_data:
            queue.enqueue_call(
                func=process_job,
                args=(job, profile_details, sheet_name),
                timeout=900,  # Timeout in seconds
                result_ttl=86400  # Keep the result for 24 hours
            )
        
        return jsonify({"message": "Jobs are being processed in the background!"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/generate-proposal', methods=['POST'])
def generate_proposal():
    try:
        payload = request.json
        jobAddress = payload.get('jobAddress', {})
        profile_details = payload.get('profileDetails', {})
        related_past_projects = payload.get('relatedProject', {})

        queue.enqueue_call(
            func=generate_job_proposal,
            args=(jobAddress, profile_details, related_past_projects),
            timeout=900,  # Timeout in seconds
            result_ttl=86400  # Keep the result for 24 hours
        )        

        return jsonify({"message": "Proposal is being generated in the background!"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500