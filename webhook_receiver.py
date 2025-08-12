#!/usr/bin/env python3
"""
GitLab Webhook Receiver
Receives GitLab webhooks and outputs issue number and description to stdout
Also triggers GitLab CI pipelines with issue data
"""

from flask import Flask, request, jsonify
import json
import sys
import os
import requests

app = Flask(__name__)


def send_webhook_data(issue_number, description, title, action, assignee_username):
    """Trigger GitLab pipeline with issue data"""
    project_id = os.environ.get('PROJECT_ID')
    token = os.environ.get('TOKEN') 
    ref = os.environ.get('REF')
    gitlab_url = os.environ.get('GITLAB_URL')
    
    if not all([project_id, token, ref, gitlab_url]):
        missing_vars = []
        if not project_id: missing_vars.append('PROJECT_ID')
        if not token: missing_vars.append('TOKEN')
        if not ref: missing_vars.append('REF')
        if not gitlab_url: missing_vars.append('GITLAB_URL')
        print(f"Warning: Required environment variables not set: {', '.join(missing_vars)}, skipping pipeline trigger", file=sys.stderr)
        return False
    
    # Validate PROJECT_ID format (should be numeric)
    if not project_id.isdigit():
        print(f"Error: PROJECT_ID must be numeric, got: {project_id}", file=sys.stderr)
        return False
    
    # Remove trailing slash from gitlab_url if present
    gitlab_url = gitlab_url.rstrip('/')
    
    # Construct GitLab pipeline trigger URL
    trigger_url = f"{gitlab_url}/api/v4/projects/{project_id}/trigger/pipeline"
    print(f"Debug: Triggering pipeline at URL: {trigger_url}", file=sys.stderr)
    
    # Prepare form data with issue information as pipeline variables
    form_data = {
        'token': token,
        'ref': ref,
        'variables[ISSUE_NUMBER]': str(issue_number),
        'variables[ISSUE_DESCRIPTION]': description,
        'variables[ISSUE_TITLE]': title,
        'variables[ISSUE_ACTION]': action,
        'variables[ASSIGNEE_USERNAME]': assignee_username
    }
    
    try:
        # Send POST request to GitLab pipeline trigger API
        response = requests.post(
            trigger_url,
            data=form_data,
            timeout=10,
            verify=False
        )
        
        if response.status_code == 201:
            print(f"Successfully triggered GitLab pipeline for project {project_id}", file=sys.stderr)
            return True
        elif response.status_code == 404:
            print(f"Pipeline trigger failed with status 404: Project not found or access denied", file=sys.stderr)
            print(f"  Check that PROJECT_ID ({project_id}) is correct and you have access to the project", file=sys.stderr)
            print(f"  Verify GITLAB_URL ({gitlab_url}) is correct and reachable", file=sys.stderr)
            print(f"  Response: {response.text}", file=sys.stderr)
            return False
        elif response.status_code == 401:
            print(f"Pipeline trigger failed with status 401: Authentication failed", file=sys.stderr)
            print(f"  Check that TOKEN is valid and has pipeline trigger permissions", file=sys.stderr)
            print(f"  Response: {response.text}", file=sys.stderr)
            return False
        elif response.status_code == 403:
            print(f"Pipeline trigger failed with status 403: Access forbidden", file=sys.stderr)
            print(f"  Check that TOKEN has permission to trigger pipelines on project {project_id}", file=sys.stderr)
            print(f"  Response: {response.text}", file=sys.stderr)
            return False
        else:
            print(f"Pipeline trigger failed with status {response.status_code}: {response.text}", file=sys.stderr)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Error triggering pipeline: {str(e)}", file=sys.stderr)
        return False


@app.route('/webhook', methods=['POST'])
def gitlab_webhook():
    """Handle GitLab webhook requests"""
    try:
        # Get the webhook payload
        payload = request.get_json()
        
        if not payload:
            print("Error: No JSON payload received", file=sys.stderr)
            return jsonify({'error': 'No JSON payload'}), 400
        
        # Check if this is an issue event
        object_kind = payload.get('object_kind', '')
        
        if object_kind == 'issue':
            # Extract issue information
            issue_data = payload.get('object_attributes', {})
            
            if issue_data:
                issue_number = issue_data.get('iid', 'N/A')  # Internal ID
                description = issue_data.get('description', 'No description')
                title = issue_data.get('title', 'No title')
                action = issue_data.get('action', 'unknown')
                
                # Extract assignee information
                assignee_username = 'No assignee'
                
                # Check for assignees array (newer GitLab versions)
                assignees = payload.get('assignees', [])
                if assignees and len(assignees) > 0:
                    # Use the first assignee if multiple assignees exist
                    assignee_username = assignees[0].get('username', 'No assignee')
                else:
                    # Check for single assignee field (older GitLab versions)
                    assignee = payload.get('assignee')
                    if assignee:
                        assignee_username = assignee.get('username', 'No assignee')
                
                # Output to stdout as requested
                print(f"Issue Number: {issue_number}")
                print(f"Description: {description}")
                print(f"Title: {title}")
                print(f"Action: {action}")
                print(f"Assignee Username: {assignee_username}")
                print("-" * 50)
                
                # Trigger GitLab pipeline with issue data
                send_webhook_data(issue_number, description, title, action, assignee_username)
                
                return jsonify({'status': 'success', 'message': 'Issue processed'}), 200
            else:
                print("Error: No issue data found in payload", file=sys.stderr)
                return jsonify({'error': 'No issue data found'}), 400
        else:
            # Not an issue event, but still acknowledge receipt
            print(f"Received webhook of type: {object_kind}", file=sys.stderr)
            return jsonify({'status': 'acknowledged', 'type': object_kind}), 200
            
    except Exception as e:
        print(f"Error processing webhook: {str(e)}", file=sys.stderr)
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    # Run the Flask app
    print("Starting GitLab webhook receiver...", file=sys.stderr)
    print("Listening for webhooks at /webhook", file=sys.stderr)
    
    project_id = os.environ.get('PROJECT_ID')
    token = os.environ.get('TOKEN')
    ref = os.environ.get('REF')
    gitlab_url = os.environ.get('GITLAB_URL')
    
    if all([project_id, token, ref, gitlab_url]):
        print(f"Will trigger GitLab pipelines for project {project_id} on ref {ref} at {gitlab_url}", file=sys.stderr)
    else:
        print("Warning: PROJECT_ID, TOKEN, REF, or GITLAB_URL not set - pipeline triggering disabled", file=sys.stderr)
        
    app.run(host='0.0.0.0', port=5000, debug=False)