#!/usr/bin/env python3
"""
API client for healthcare patient data.
This module handles all API calls to the patient management system.
"""

import httpx
from typing import List, Dict, Any, Optional
from config import API_CONFIG, FIELD_MAPPING, QUERY_PARAM_MAPPING


class PatientAPIClient:
    """Client for interacting with the patient management API."""
    
    def __init__(self):
        """Initialize the API client with configuration."""
        self.base_url = API_CONFIG["base_url"]
        self.timeout = API_CONFIG.get("timeout", 30)
        self.auth_config = API_CONFIG.get("auth", {})
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers including authentication."""
        headers = {
            "Content-Type": "application/json",
        }
        
        # Add authentication if configured
        if self.auth_config.get("type") == "bearer" and self.auth_config.get("token"):
            headers["Authorization"] = f"Bearer {self.auth_config['token']}"
        elif self.auth_config.get("type") == "api_key" and self.auth_config.get("token"):
            header_name = self.auth_config.get("header_name", "X-API-Key")
            headers[header_name] = self.auth_config["token"]
        
        return headers
    
    def _get_field_value(self, patient_data: Dict[str, Any], field_name: str) -> Any:
        """Get field value using field mapping configuration."""
        possible_names = FIELD_MAPPING.get(field_name, [field_name])
        for name in possible_names:
            if name in patient_data and patient_data[name] is not None:
                value = patient_data[name]
                # Return the actual value (could be string, list, etc.)
                return value
        return "N/A" if field_name != "name" else "Unknown"
    
    def _format_patient_list(self, patients: List[Dict[str, Any]]) -> str:
        """Format patient list into a readable string with comprehensive patient information."""
        if not patients:
            return "No patients found matching the specified criteria."

        response_lines = [f"Found {len(patients)} patient(s):\n"]

        for i, patient in enumerate(patients, 1):
            # Basic information
            patient_id = self._get_field_value(patient, "id")
            name = self._get_field_value(patient, "name")
            age = self._get_field_value(patient, "age")

            # Medical information
            diagnosis = self._get_field_value(patient, "diagnosis")
            medications = self._get_field_value(patient, "medications")
            allergies = self._get_field_value(patient, "allergies")
            last_updated = self._get_field_value(patient, "last_updated")

            # Legacy fields (for backward compatibility)
            dept = self._get_field_value(patient, "department")
            status = self._get_field_value(patient, "status")
            admission_date = self._get_field_value(patient, "admission_date")

            # Format patient entry
            response_lines.append(f"📋 Patient #{i}")
            response_lines.append(f"   👤 Name: {name}")
            response_lines.append(f"   🆔 ID: {patient_id}")
            response_lines.append(f"   🎂 Age: {age}")

            if diagnosis != "N/A":
                response_lines.append(f"   🏥 Diagnosis: {diagnosis}")

            if medications != "N/A":
                # Handle medications array
                if isinstance(medications, list):
                    meds_str = ", ".join(medications)
                else:
                    meds_str = str(medications)
                response_lines.append(f"   💊 Medications: {meds_str}")

            if allergies != "N/A":
                # Handle allergies array
                if isinstance(allergies, list):
                    allergies_str = ", ".join(allergies)
                else:
                    allergies_str = str(allergies)
                response_lines.append(f"   ⚠️  Allergies: {allergies_str}")

            if last_updated != "N/A":
                response_lines.append(f"   📅 Last Updated: {last_updated}")

            # Legacy fields (if available)
            if dept != "N/A":
                response_lines.append(f"   🏢 Department: {dept.title()}")
            if status != "N/A":
                response_lines.append(f"   📊 Status: {status.title()}")
            if admission_date != "N/A":
                response_lines.append(f"   📆 Admitted: {admission_date}")

            response_lines.append("")  # Empty line between patients

        return "\n".join(response_lines)
    
    async def get_patient_list(self, patient_name: Optional[str] = None, limit: int = 10) -> str:
        """
        Get list of patients from the API.
        
        Args:
            patient_name: Filter by patient name (optional, partial matches supported)
            limit: Maximum number of patients to return (1-100, default: 10)
            
        Returns:
            Formatted string with patient information
            
        Raises:
            Exception: If API call fails or returns invalid data
        """
        try:
            # Build endpoint URL
            endpoint = f"{self.base_url}{API_CONFIG['endpoints']['patients']}"
            
            # Prepare query parameters
            params = {}
            if patient_name:
                # Use the configured parameter name for patient name filtering
                param_name = QUERY_PARAM_MAPPING.get("patient_name", "name")
                params[param_name] = patient_name
            params["limit"] = min(max(limit, 1), 100)  # Ensure limit is between 1 and 100
            
            # Make HTTP request
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(endpoint, params=params, headers=self._get_headers())
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Handle different API response formats
                    if isinstance(data, list):
                        patients = data
                    elif isinstance(data, dict) and "patients" in data:
                        patients = data["patients"]
                    elif isinstance(data, dict) and "data" in data:
                        patients = data["data"]
                    else:
                        patients = [data] if data else []
                    
                    return self._format_patient_list(patients)
                
                else:
                    error_text = f"API request failed with status {response.status_code}"
                    try:
                        error_data = response.text
                        error_text += f": {error_data}"
                    except:
                        pass
                    
                    return f"Error: {error_text}"
        
        except httpx.RequestError as e:
            return f"Network error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"


# Create a singleton instance for use across the application
patient_api_client = PatientAPIClient()
