//CT Module list for study data
// Required data modules from ClinicalTrials.gov
private final Set<String> REQUIRED_MODULES = Set.of(
    "IdentificationModule", 
    "StatusModule", 
    "SponsorCollaboratorsModule",
    "OversightModule", 
    "DescriptionModule", 
    "ConditionsModule", 
    "DesignModule", 
    "ArmsInterventionsModule", 
    "OutcomesModule",
    "EligibilityModule", 
    "ContactsLocationsModule", 
    "ReferencesModule",
    "IPDSharingStatementModule", 
    "ParticipantFlowModule",
    "BaselineCharacteristicsModule", 
    "OutcomeMeasuresModule",
    "AdverseEventsModule"
);

//baseling Output structure for companytrialanlayzer
class CompanyTrialData(BaseModel):
    company_name: str
    query_date: datetime
    trials: List[Study]  # Full trial data with all modules
    analytics: TrialAnalytics

class Study(BaseModel):
    protocol_section: ProtocolSection  # Contains all module data
    # Other trial metadata

class TrialAnalytics(BaseModel):
    phase_distribution: Dict
    status_summary: Dict
    therapeutic_areas: Dict


    ENHANCED ANALYTICS
    class Study(BaseModel):
    protocol_section: ProtocolSection
    identification_module: Dict
    status_module: Dict
    sponsor_collaborators_module: Dict
    oversight_module: Dict
    description_module: Dict
    conditions_module: Dict
    design_module: Dict
    arms_interventions_module: Dict
    outcomes_module: Dict
    eligibility_module: Dict
    contacts_locations_module: Dict
    references_module: Dict
    ipd_sharing_statement_module: Dict
    participant_flow_module: Dict
    baseline_characteristics_module: Dict
    outcome_measures_module: Dict
    adverse_events_module: Dict

    ENHANCED TRIAL ANALYZER 
    class ClinicalTrial(BaseModel):
    nct_id: str
    company_id: str
    # All modules from above
    metadata: TrialMetadata

class TrialMetadata(BaseModel):
    query_date: datetime
    company_name: str
    last_updated: datetime
    data_source: str = "clinicaltrials.gov"

class TrialAnalytics(BaseModel):
    company_id: str
    # Base analytics
    phase_distribution: Dict
    status_summary: Dict
    therapeutic_areas: Dict
    # Module-specific analytics
    module_analytics: Dict  # Extensible for different module analyses
    metadata: TrialMetadata


// companies collection
{
    _id: ObjectId,
    companyName: String,
    companyWebsite: String,
    companySize: String,
    headquarters: String,
    contactEmail: String,
    enrichedData: Object,
    contextualData: Object,
    clinicalTrials: [String],  // NCT IDs
    lastEnriched: Date,
    createdAt: Date,
    updatedAt: Date,
    therapeuticAreas: [String],
    enrichmentStatus: String,
    lastAnalyzed: Date
}

// clinical_trials collection
{
    _id: String,  // NCT ID
    company_id: ObjectId,  // Reference to companies._id
    modules: {
        identification_module: Object,
        status_module: Object,
        // ... all other modules
    },
    metadata: {
        query_date: Date,
        company_name: String,
        last_updated: Date,
        data_source: String
    }
}

// trial_analytics collection
{
    _id: ObjectId,
    company_id: ObjectId,  // Reference to companies._id
    base_analytics: {
        phase_distribution: Object,
        status_summary: Object,
        therapeutic_areas: Object
    },
    module_analytics: {
        conditions_analysis: Object,
        interventions_analysis: Object,
        // ... other module analytics
    },
    metadata: {
        query_date: Date,
        company_name: String,
        last_updated: Date,
        data_source: String
    }
}

Connectivity
graph TD
    A[Company] -->|1:N| B[ClinicalTrials]
    A -->|1: C[TrialAnalytics]
    B -->|N:1| A
    C -->|1:1| A

    Key Links
    Key Links:
Company.id links to:
ClinicalTrial.company_id
TrialAnalytics.company_id
Company.clinicalTrials array contains NCT IDs matching ClinicalTrial.id
Would you like me to:
Show the FastAPI routes needed?
Detail the data flow between collections?
Explain the query patterns?
