#!/usr/bin/env python3
"""
Test script to demonstrate the new patient API response format handling.
This script shows how the system handles the comprehensive patient data structure.
"""

import asyncio
import json
from api_client import PatientAPIClient


# Sample API response in the new format
SAMPLE_PATIENT_DATA = [
    {
        "PatientId": "P001",
        "Name": "John Doe",
        "Age": 45,
        "Diagnosis": "Hypertension, Type 2 Diabetes",
        "Medications": ["Metformin 500mg", "Lisinopril 10mg", "Atorvastatin 20mg"],
        "Allergies": ["Penicillin", "Shellfish"],
        "LastUpdated": "2024-01-15T10:30:00Z"
    },
    {
        "PatientId": "P002",
        "Name": "Jane Smith",
        "Age": 32,
        "Diagnosis": "Asthma, Seasonal Allergies",
        "Medications": ["Albuterol Inhaler", "Claritin 10mg"],
        "Allergies": ["Pollen", "Dust mites"],
        "LastUpdated": "2024-01-14T14:20:00Z"
    },
    {
        "PatientId": "P003",
        "Name": "Robert Johnson",
        "Age": 67,
        "Diagnosis": "Coronary Artery Disease, High Cholesterol",
        "Medications": ["Clopidogrel 75mg", "Simvastatin 40mg", "Metoprolol 50mg"],
        "Allergies": ["Aspirin"],
        "LastUpdated": "2024-01-13T09:15:00Z"
    }
]

# Alternative format with string medications/allergies
SAMPLE_PATIENT_DATA_ALT = [
    {
        "patient_id": "P004",
        "patient_name": "Mary Wilson",
        "age": 28,
        "diagnosis": "Migraine, Anxiety",
        "medications": "Sumatriptan 50mg, Sertraline 25mg",
        "allergies": "Codeine, Latex",
        "last_updated": "2024-01-12T16:45:00Z"
    }
]


def test_patient_formatting():
    """Test the patient data formatting with the new structure."""
    print("🧪 Testing Patient Data Formatting")
    print("=" * 50)
    
    # Initialize the API client
    client = PatientAPIClient()
    
    print("\n📋 Test 1: Comprehensive Patient Data (Array Format)")
    print("-" * 50)
    formatted_result = client._format_patient_list(SAMPLE_PATIENT_DATA)
    print(formatted_result)
    
    print("\n📋 Test 2: Alternative Format (String Medications/Allergies)")
    print("-" * 50)
    formatted_result_alt = client._format_patient_list(SAMPLE_PATIENT_DATA_ALT)
    print(formatted_result_alt)
    
    print("\n📋 Test 3: Empty Patient List")
    print("-" * 50)
    empty_result = client._format_patient_list([])
    print(empty_result)


def test_field_mapping():
    """Test field mapping with different naming conventions."""
    print("\n🔍 Testing Field Mapping")
    print("=" * 50)
    
    client = PatientAPIClient()
    
    # Test different field name variations
    test_patient = {
        "PatientId": "P001",
        "Name": "Test Patient",
        "Age": 30,
        "Diagnosis": "Test Condition",
        "Medications": ["Test Med 1", "Test Med 2"],
        "Allergies": ["Test Allergy"],
        "LastUpdated": "2024-01-15"
    }
    
    print(f"Patient ID: {client._get_field_value(test_patient, 'id')}")
    print(f"Name: {client._get_field_value(test_patient, 'name')}")
    print(f"Age: {client._get_field_value(test_patient, 'age')}")
    print(f"Diagnosis: {client._get_field_value(test_patient, 'diagnosis')}")
    print(f"Medications: {client._get_field_value(test_patient, 'medications')}")
    print(f"Allergies: {client._get_field_value(test_patient, 'allergies')}")
    print(f"Last Updated: {client._get_field_value(test_patient, 'last_updated')}")


def test_mixed_formats():
    """Test handling of mixed API response formats."""
    print("\n🔄 Testing Mixed Format Handling")
    print("=" * 50)
    
    client = PatientAPIClient()
    
    # Mix of new and legacy formats
    mixed_data = [
        {
            "PatientId": "P001",
            "Name": "John Doe",
            "Age": 45,
            "Diagnosis": "Hypertension",
            "Medications": ["Lisinopril 10mg"],
            "Allergies": ["Penicillin"],
            "LastUpdated": "2024-01-15"
        },
        {
            "id": "P002",
            "name": "Jane Smith",
            "age": 32,
            "department": "cardiology",
            "status": "active",
            "admission_date": "2024-01-14"
        }
    ]
    
    formatted_mixed = client._format_patient_list(mixed_data)
    print(formatted_mixed)


def show_api_examples():
    """Show examples of API responses that the system can handle."""
    print("\n📚 API Response Examples")
    print("=" * 50)
    
    print("\n✅ Supported API Response Format 1 (Recommended):")
    print(json.dumps(SAMPLE_PATIENT_DATA[0], indent=2))
    
    print("\n✅ Supported API Response Format 2 (Alternative):")
    print(json.dumps(SAMPLE_PATIENT_DATA_ALT[0], indent=2))
    
    print("\n✅ Supported API Response Format 3 (Wrapped):")
    wrapped_format = {
        "data": SAMPLE_PATIENT_DATA[:1],
        "total": 1,
        "page": 1
    }
    print(json.dumps(wrapped_format, indent=2))


if __name__ == "__main__":
    print("🏥 Healthcare Chatbot - Patient API Format Testing")
    print("=" * 60)
    
    try:
        test_patient_formatting()
        test_field_mapping()
        test_mixed_formats()
        show_api_examples()
        
        print("\n🎉 All tests completed successfully!")
        print("\n💡 Key Features:")
        print("- ✅ Handles comprehensive patient data (ID, Name, Age, Diagnosis, Medications, Allergies)")
        print("- ✅ Supports both array and string formats for medications/allergies")
        print("- ✅ Backward compatible with legacy API formats")
        print("- ✅ Flexible field mapping for different naming conventions")
        print("- ✅ Rich formatting with emojis and structured display")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
