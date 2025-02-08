from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import requests
from ct_client.clinical_trials_gov_rest_api_client.api.studies.fetch_study import sync as fetch_study_sync
from ct_client.clinical_trials_gov_rest_api_client.client import Client
import logging

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class QueryRequest(BaseModel):
    query: str
    hypothesis: str = None
    filters: dict = {}



def get_ai_suggestions(query, filters=None):
    """
    Generates AI suggestions based on the input query and optional filters.
    """
    filters = filters or {}  # Ensure filters is a dictionary

    # Base analysis for the query
    analysis = f"Analyzing the query: {query}."

    # Include filters in the analysis (if provided)
    if filters.get("phase"):
        analysis += f" Considering trials in phase: {filters['phase']}."
    if filters.get("condition"):
        analysis += f" Focused on condition: {filters['condition']}."
    if filters.get("intervention"):
        analysis += f" Filtering by intervention type: {filters['intervention']}."
    if filters.get("design"):
        analysis += f" Based on design: {filters['design']}."

    return analysis



def generate_cypher_query(query, hypothesis, filters=None):
    """
    Refines the input query for use with the Knowledge Graph.
    Includes optional filters for additional constraints.
    """
    filters = filters or {}  # Default to an empty dictionary if no filters provided
    cypher_query = f"MATCH (t:Trial) WHERE t.text CONTAINS '{query}'"

    # Dynamically include filters in the query
    if hypothesis:
        cypher_query += f" AND t.hypothesis = '{hypothesis}'"
    if filters.get("phase"):
        cypher_query += f" AND t.phase = '{filters['phase']}'"
    if filters.get("condition"):
        cypher_query += f" AND t.condition = '{filters['condition']}'"
    if filters.get("intervention"):
        cypher_query += f" AND t.intervention = '{filters['intervention']}'"
    if filters.get("design"):
        cypher_query += f" AND t.design = '{filters['design']}'"

    cypher_query += " RETURN t.trial_name, t.phase, t.condition"
    return cypher_query


class ClinicalTrialsService:
    def __init__(self):
        # Initialize the client (replace with AuthenticatedClient if required)
        self.client = Client(base_url="https://clinicaltrials.gov/api/v2")


    def fetch_trials(self, refined_query: str, filters: dict = None):
        """
        Fetch clinical trials with optimized API calls.
        """
        filters = filters or {}
        trial_results = []
        successful_trials = []

        try:
            # Initialize HTTPX client
            httpx_client = self.client.get_httpx_client()

            # Build API parameters dynamically
            params = {
                "query.term": refined_query,
                "filter.phase": filters.get("phase"),
                "query.cond": filters.get("condition"),
                "filter.intervention": filters.get("intervention"),
                "filter.design": filters.get("design"),
            }
            params = {k: v for k, v in params.items() if v}  # Remove empty values

            # Fetch trial summaries in a single call
            response = httpx_client.get("/studies", params=params)
            response.raise_for_status()
            trial_summaries = response.json()

            # Fetch details for each trial in parallel
            for trial in trial_summaries.get("studies", []):
                try:
                    trial_details = fetch_study_sync(
                        nct_id=trial["nct_id"],
                        client=self.client,
                        format_="json",
                        markup_format="markdown",
                        fields=["nct_id", "title", "status"],  # Request only necessary fields
                    )
                    trial_results.append(trial_details)
                except Exception as e:
                    logger.error(f"Error fetching details for trial {trial['nct_id']}: {e}")

            # Fetch successful trials if required
            if "success" in filters:
                successful_trials = self.search_successful_trials(refined_query)

        except Exception as e:
            logger.error(f"Error fetching trials: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error fetching clinical trial data: {str(e)}")

        return {
            "trial_results": trial_results,
            "successful_trials": successful_trials,
        }

    def search_successful_trials(self, refined_query: str):
        """
        Search for successful clinical trials.
        """
        try:
            httpx_client = self.client.get_httpx_client()
            response = httpx_client.get("/successful-trials", params={"query": refined_query})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching successful trials: {e}", exc_info=True)
            return []
