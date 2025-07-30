"""
Configuration file for the MCP server.
Update these settings to match your API endpoint.
"""

# API Configuration
API_CONFIG = {
    # Replace with your actual API endpoint URL
    "base_url": "http://localhost:5010/api",
    
    # API endpoints
    "endpoints": {
        "patients": "/Patient",  # GET endpoint for patient list
    },
    
    # Authentication (if required)
    "auth": {
        "type": "None",  # Options: "bearer", "api_key", "basic", None
        "token": "YOUR_API_TOKEN_HERE",  # Replace with your actual token
        "header_name": "Authorization",  # Header name for API key auth
    },
    
    # Request settings
    "timeout": 30,  # Request timeout in seconds
    "max_retries": 3,  # Number of retry attempts
    
    # Default parameters
    "defaults": {
        "limit": 10,  # Default number of patients to return
    }
}

# Field mapping for different API response formats
# Map your API's field names to standard field names
FIELD_MAPPING = {
    "id": ["id", "patient_id", "patientId", "PatientId", "ID"],
    "name": ["name", "patient_name", "fullName", "full_name", "Name"],
    "age": ["age", "patient_age", "Age"],
    "diagnosis": ["diagnosis", "Diagnosis", "condition", "medical_condition"],
    "medications": ["medications", "Medications", "meds", "drugs", "prescriptions"],
    "allergies": ["allergies", "Allergies", "allergy_list", "medical_allergies"],
    "last_updated": ["last_updated", "LastUpdated", "lastUpdated", "updated_at", "modified_date"],
    "department": ["department", "dept", "department_name"],
    "status": ["status", "patient_status", "state"],
    "admission_date": ["admission_date", "admissionDate", "admitted", "date_admitted"]
}

# API query parameter mapping
# Map tool parameters to your API's query parameter names
QUERY_PARAM_MAPPING = {
    "patient_name": "name"  # Change this to match your API's parameter name for patient name filtering
}

# Example API response formats that the server can handle:
"""
Format 1 - Comprehensive Patient Data (Recommended):
[
    {
        "PatientId": "P001",
        "Name": "John Doe",
        "Age": 45,
        "Diagnosis": "Hypertension, Type 2 Diabetes",
        "Medications": ["Metformin 500mg", "Lisinopril 10mg", "Atorvastatin 20mg"],
        "Allergies": ["Penicillin", "Shellfish"],
        "LastUpdated": "2024-01-15T10:30:00Z"
    }
]

Format 2 - Wrapped in data object:
{
    "data": [
        {
            "PatientId": "P001",
            "Name": "John Doe",
            "Age": 45,
            "Diagnosis": "Hypertension, Type 2 Diabetes",
            "Medications": ["Metformin 500mg", "Lisinopril 10mg"],
            "Allergies": ["Penicillin"],
            "LastUpdated": "2024-01-15T10:30:00Z"
        }
    ]
}

Format 3 - Legacy format (still supported):
{
    "patients": [
        {
            "id": "P001",
            "name": "John Smith",
            "age": 45,
            "department": "cardiology",
            "status": "active",
            "admission_date": "2024-01-15"
        }
    ],
    "total": 1,
    "page": 1
}

Format 4 - Mixed format with medical data:
[
    {
        "patient_id": "P001",
        "patient_name": "John Doe",
        "age": 45,
        "diagnosis": "Hypertension, Type 2 Diabetes",
        "medications": "Metformin 500mg, Lisinopril 10mg",
        "allergies": "Penicillin, Shellfish",
        "last_updated": "2024-01-15"
    }
]
"""
