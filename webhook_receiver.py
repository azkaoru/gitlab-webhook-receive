#!/usr/bin/env python3
"""
GitLab Webhook Receiver
Receives GitLab webhooks and outputs issue number and description to stdout
Also sends issue data to configured webhook URL
"""

from flask import Flask, request, jsonify
import json
import sys
import os
import requests

app = Flask(__name__)


def send_webhook_data(issue_number, description, title, action):
    """Send issue data to configured webhook URL"""
    webhook_url = os.environ.get('WEBHOOK_URL')
    
    if not webhook_url:
        print("Warning: WEBHOOK_URL environment variable not set, skipping webhook send", file=sys.stderr)
        return False
    
    # Prepare webhook payload
    webhook_payload = {
        'issue_number': issue_number,
        'description': description,
        'title': title,
        'action': action
    }
    
    try:
        # Send POST request to webhook URL
        response = requests.post(
            webhook_url,
            json=webhook_payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"Successfully sent webhook data to {webhook_url}", file=sys.stderr)
            return True
        else:
            print(f"Webhook send failed with status {response.status_code}: {response.text}", file=sys.stderr)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook: {str(e)}", file=sys.stderr)
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
                
                # Output to stdout as requested
                print(f"Issue Number: {issue_number}")
                print(f"Description: {description}")
                print(f"Title: {title}")
                print(f"Action: {action}")
                print("-" * 50)
                
                # Send webhook data to configured URL
                send_webhook_data(issue_number, description, title, action)
                
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
    
    webhook_url = os.environ.get('WEBHOOK_URL')
    if webhook_url:
        print(f"Will forward issue data to: {webhook_url}", file=sys.stderr)
    else:
        print("Warning: WEBHOOK_URL not set - webhook forwarding disabled", file=sys.stderr)
        
    app.run(host='0.0.0.0', port=5000, debug=False)