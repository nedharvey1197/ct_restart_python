# Current Flow
class DataFlow:
    # Primary Flow
    company_to_trials = {
        "source": "companies",
        "target": "clinical_trials",
        "link_field": "company_id",
        "reference_type": "one_to_many"
    }
    
    # Analytics Flow
    trials_to_analytics = {
        "source": "clinical_trials",
        "target": "trial_analytics",
        "link_field": "company_id",
        "aggregation_type": "group_by_company"
    }

    # Future KG Integration Points
    kg_integration = {
        "baseline_layer": {
            "study_entities": ["Study", "Protocol", "StudyArm"],
            "clinical_entities": ["Condition", "Intervention", "Biomarker"]
        },
        "core_support_layer": {
            "trial_state": ["TrialStatus", "Milestone", "RiskIndicator"],
            "contextual_intelligence": ["Protocol", "SafetySignal"]
        }
    }