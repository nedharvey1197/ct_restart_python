from typing import Dict, Any
import requests
import os
from openai import OpenAI
import json
import logging
from ct_client.clinical_trials_gov_rest_api_client.api.studies.fetch_study import sync as fetch_study_sync
from ct_client.clinical_trials_gov_rest_api_client.client import Client
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)  # And this
logger = logging.getLogger(__name__)     # And this

# OpenAI API Key (Environment Variable)
client = OpenAI()  # Will automatically use OPENAI_API_KEY from environment

# ClinicalTrials.gov API Endpoint
CTGOV_API_URL = "https://clinicaltrials.gov/api/v2/studies"

class QueryRequest(BaseModel):
    user_query: str

class QueryResponse(BaseModel):
    query: Dict[str, Any]  # Keep as Dict to maintain structured data
    results: Dict[str, Any]

def refine_query(user_input: str) -> dict:
    """
    Process user input using GPT-4 to extract structured trial parameters.
    Returns a dictionary with the structured parameters.
    """
    logger.info(f"Refining query for user input: {user_input}")
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": """You are an AI assistant trained to refine clinical trial queries.
                You must ALWAYS respond with valid JSON only, in exactly this format:
                {
                    "condition": "disease or condition name",
                    "phase": "trial phase",
                    "status": "trial status"
                }
                Do not include any other text or explanation."""},
                {"role": "user", "content": f"Convert this query into structured parameters: {user_input}"}
            ],
            model="gpt-4o",
        )
        
        # Convert the Pydantic model to a dict and get the content
        response_dict = response.model_dump()
        result = response_dict['choices'][0]['message']['content']
        
        # Parse the JSON string into a dictionary
        try:
            logger.info(f"Refined query result: {result}")
            return json.loads(result)
        except json.JSONDecodeError as e:
            print(f"Failed to parse GPT response: {result}")
            return {
                "condition": user_input,
                "phase": "",
                "status": ""
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# Logging setup
logger = logging.getLogger(__name__)

def fetch_trials(refined_query: str, filters: dict = None):
    """
    Fetch clinical trials from ClinicalTrials.gov based on a refined query and filters.

    Args:
        refined_query (str): The refined query for the knowledge graph.
        filters (dict): Additional filters for the clinical trial search.

    Returns:
        list: List of clinical trial data.
    """
    # Initialize the client (replace with AuthenticatedClient if required)
    client = Client(base_url="https://clinicaltrials.gov/api/v2")
    filters = filters or {}

    # Initialize ClinicalTrials.gov client
    # config = Configuration(base_url="https://clinicaltrials.gov/api/v2")
    # client = ApiClient(config)
    # ct_api = ClinicalTrialsApi(client)

    # Build API parameters
    params = {"query.term": refined_query}  # Basic query
    if "phase" in filters:
        params["filter.phase"] = filters["phase"]
    if "condition" in filters:
        params["query.cond"] = filters["condition"]
    if "intervention" in filters:
        params["query.intr"] = filters["intervention"]
    if "design" in filters:
        params["query.design"] = filters["design"]

    try:
        # Initialize HTTPX client
        httpx_client = client.get_httpx_client()

        # Log the request parameters
        logger.info(f"Fetching trials with parameters: {params}")

        # Fetch studies using the generated client
        response = httpx_client.get("/studies", params=params)
        logger.info(f"Trials fetched successfully: {response.json()}")
        studies_list = [
            {
                "NCT_ID": study.get("protocolSection", {}).get("identificationModule", {}).get("nctId"),
                "Title": study.get("protocolSection", {}).get("identificationModule", {}).get("briefTitle"),
                "Status": study.get("protocolSection", {}).get("statusModule", {}).get("overallStatus"),
                "Conditions": study.get("protocolSection", {}).get("conditionsModule", {}).get("conditions", []),
                "Locations": study.get("protocolSection", {}).get("locationModule", {}).get("locations", [])
            }
            for study in response.json().get("studies", [])
        ]

        # Log the raw response
        logger.info(f"Trials fetched successfully: {studies_list}")

        return studies_list # Assuming `response.studies` contains the list of trials

    except Exception as e:
        logger.error(f"Error fetching trials: {e}", exc_info=True)
        raise RuntimeError(f"Failed to fetch trials: {str(e)}")