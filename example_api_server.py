#!/usr/bin/env python3
"""
Example API server for testing the MCP server's getpatientlist tool.
This is a simple Flask server that provides a /patients endpoint.

Run this server to test your MCP server before connecting to your real API.

Usage:
    pip install flask
    python example_api_server.py

Then update config.py to use: "base_url": "http://localhost:5001"
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample patient data
SAMPLE_PATIENTS = [
    {"id": "P001", "name": "John Smith", "age": 45, "department": "cardiology", "status": "active", "admission_date": "2024-01-15"},
    {"id": "P002", "name": "Mary Johnson", "age": 32, "department": "neurology", "status": "admitted", "admission_date": "2024-01-20"},
    {"id": "P003", "name": "Robert Brown", "age": 67, "department": "orthopedics", "status": "discharged", "admission_date": "2024-01-10"},
    {"id": "P004", "name": "Sarah Davis", "age": 28, "department": "general", "status": "outpatient", "admission_date": "2024-01-22"},
    {"id": "P005", "name": "Michael Wilson", "age": 55, "department": "emergency", "status": "active", "admission_date": "2024-01-23"},
    {"id": "P006", "name": "Emily Taylor", "age": 41, "department": "cardiology", "status": "admitted", "admission_date": "2024-01-21"},
    {"id": "P007", "name": "David Anderson", "age": 39, "department": "neurology", "status": "active", "admission_date": "2024-01-19"},
    {"id": "P008", "name": "Lisa Martinez", "age": 52, "department": "orthopedics", "status": "outpatient", "admission_date": "2024-01-18"},
    {"id": "P009", "name": "James Garcia", "age": 33, "department": "general", "status": "discharged", "admission_date": "2024-01-12"},
    {"id": "P010", "name": "Jennifer Lee", "age": 47, "department": "emergency", "status": "admitted", "admission_date": "2024-01-24"},
    {"id": "P011", "name": "Christopher White", "age": 29, "department": "cardiology", "status": "outpatient", "admission_date": "2024-01-25"},
    {"id": "P012", "name": "Amanda Clark", "age": 38, "department": "neurology", "status": "discharged", "admission_date": "2024-01-16"},
]

@app.route('/api/Patient', methods=['GET'])
def get_patients():
    """
    Get patients with optional filtering.

    Query parameters:
    - name: Filter by patient name (partial matches supported)
    - limit: Maximum number of patients to return
    """
    try:
        # Get query parameters
        name = request.args.get('name')
        limit = request.args.get('limit', type=int, default=10)

        # Start with all patients
        filtered_patients = SAMPLE_PATIENTS.copy()

        # Apply name filter (partial match, case insensitive)
        if name:
            filtered_patients = [p for p in filtered_patients if name.lower() in p['name'].lower()]
        
        # Apply limit
        if limit > 0:
            filtered_patients = filtered_patients[:limit]
        
        # Return response
        response = {
            "patients": filtered_patients,
            "total": len(filtered_patients),
            "filters": {
                "name": name,
                "limit": limit
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get a specific patient by ID."""
    try:
        patient = next((p for p in SAMPLE_PATIENTS if p['id'] == patient_id), None)
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"error": "Patient not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "message": "Example API server is running"}), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information."""
    return jsonify({
        "message": "Example Patient API Server",
        "endpoints": {
            "/api/Patient": "GET - List patients with optional filters (name, limit)",
            "/patients/<id>": "GET - Get specific patient by ID",
            "/health": "GET - Health check"
        },
        "example_requests": {
            "all_patients": "http://localhost:5000/api/Patient",
            "patients_by_name": "http://localhost:5000/api/Patient?name=John",
            "patients_with_limit": "http://localhost:5000/api/Patient?name=Smith&limit=5",
            "specific_patient": "http://localhost:5000/patients/P001"
        }
    }), 200

if __name__ == '__main__':
    print("Starting Example Patient API Server...")
    print("Available endpoints:")
    print("  GET /patients - List patients with optional filters")
    print("  GET /patients/<id> - Get specific patient")
    print("  GET /health - Health check")
    print("  GET / - API information")
    print("\nExample URLs:")
    print("  http://localhost:5001/patients")
    print("  http://localhost:5001/patients?name=John")
    print("  http://localhost:5001/patients?name=Smith&limit=5")
    print("\nTo use with MCP server, update config.py:")
    print('  "base_url": "http://localhost:5001"')
    print("\nPress Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
