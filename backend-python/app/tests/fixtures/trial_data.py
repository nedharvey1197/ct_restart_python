from datetime import datetime

SAMPLE_TRIAL = {
    "nctId": "NCT00000000",
    "protocolSection": {
        "identificationModule": {
            "nctId": "NCT00000000",
            "briefTitle": "Test Trial",
            "officialTitle": "Official Test Trial Title",
            "organization": {"name": "Test Org"}
        },
        "statusModule": {
            "overallStatus": "Completed",
            "startDateStruct": {"date": "2023-01-01"},
            "completionDateStruct": {"date": "2023-12-31"}
        },
        "designModule": {
            "phases": ["Phase 1"],
            "enrollmentInfo": {"count": 100}
        },
        "conditionsModule": {
            "conditions": ["Cancer"]
        }
    },
    "hasResults": False
}

SAMPLE_COMPANY = {
    "name": "Test Company",
    "website": "https://test.com",
    "clinicalTrials": [SAMPLE_TRIAL],
    "lastAnalyzed": datetime.utcnow().isoformat()
} 