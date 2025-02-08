from ct_client import ClinicalTrialsApi, Configuration, ApiClient

class ClinicalTrialsService:
    def __init__(self):
        # Initialize the client with the correct configuration
        config = Configuration(host="https://clinicaltrials.gov/api/v2")
        self.client = ApiClient(config)
        self.api = ClinicalTrialsApi(self.client)

    def fetch_studies(self, query_params):
        """
        Fetch studies based on query parameters.
        """
        try:
            response = self.api.search_studies(**query_params)
            return response
        except Exception as e:
            print(f"Error fetching studies: {e}")
            raise

    def fetch_study_details(self, study_id):
        """
        Fetch detailed information for a specific study by ID.
        """
        try:
            response = self.api.get_study_by_id(study_id=study_id)
            return response
        except Exception as e:
            print(f"Error fetching study details: {e}")
            raise
