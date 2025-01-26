from flask import Flask, render_template, jsonify, request
import subprocess
import os
import json
import platform

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Route for serving the home page
@app.route('/')
def index():
    os_type = platform.system()
    return render_template('index.html', os_type=os_type)

# Route to trigger audit based on OS type
@app.route('/api/audit', methods=['POST'])
def run_audit():
    os_type = request.json.get('os_type')
    
    # Check OS type and run the corresponding PowerShell script for Windows 11
    if os_type == "windows":
        script_path = os.path.join('scripts', 'windows_11_audit.ps1')
        result = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], capture_output=True, text=True)
        
        # Parse the JSON output from the PowerShell script
        try:
            audit_results = json.loads(result.stdout)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse audit results"}), 500
        
        # Save results to a JSON file
        os.makedirs('results', exist_ok=True)  # Ensure the results directory exists
        with open('results/audit_results.json', 'w') as f:
            json.dump(audit_results, f, indent=4)
        
        return jsonify({"message": "Audit completed successfully"}), 200
    else:
        return jsonify({"error": "Unsupported OS type"}), 400

# Route to get audit results
@app.route('/api/results', methods=['GET'])
def get_results():
    try:
        with open('results/audit_results.json', 'r') as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({"error": "No results found"}), 404

if __name__ == '__main__':
    app.run(debug=True)