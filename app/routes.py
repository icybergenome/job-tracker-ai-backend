from flask import request, jsonify
from app import app, queue
from app.tasks import process_job

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
                result_ttl=86400,  # Keep the result for 24 hours
                ttl=3600  # Discard the job if it stays in the queue for more than 1 hour
            )
        
        return jsonify({"message": "Jobs are being processed in the background!"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500