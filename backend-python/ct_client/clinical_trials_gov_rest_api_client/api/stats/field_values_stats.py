from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import openai
import logging
import json
from app.services.gpt_copilot_services import (
    ClinicalTrialsService,
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the router
router = APIRouter(prefix="/GPTCopilot", tags=["GPTCopilot"])

# Request body schema
class QueryRequest(BaseModel):
    query: str
    hypothesis: Optional[str] = None
    filters: Optional[Dict] = None  # Filters are optional

# Initialize ClinicalTrialsService
trials_service = ClinicalTrialsService()

# Cached API schema instructions
CTG_API_SCHEMA = (
    "You are an expert in structuring clinical trial searches for ClinicalTrials.gov API. "
    "Extract and return optimized search parameters in a structured JSON format. "
    "Ensure the query is enhanced by incorporating relevant filters, synonyms, and alternate search strategies. "
    "Do not generate full queries—only return the extracted parameters in JSON format. "
    "Strictly follow this format: { 'query': '...', 'condition': '...', 'intervention': '...', 'study_start_date': 'YYYY-MM-DD', 'study_end_date': 'YYYY-MM-DD', 'phase': '...', 'sort_by': '...', 'page': 1 }. "
    "Ensure the output contains only JSON, without explanations or extra text. "
    "Example Output: { 'query': 'optimized search query', 'condition': 'oncology', 'intervention': 'immunotherapy', 'study_start_date': '2020-01-01', 'study_end_date': '2024-12-31', 'phase': 'Phase 3', 'sort_by': 'start_date', 'page': 1 }"
)

def get_ai_suggestions(query: str, filters: Dict) -> Dict:
    """
    Uses GPT-4 to extract and enhance structured search parameters for ClinicalTrials.gov API.
    """
    try:
        prompt = (
            f"Enhance and extract structured search terms for ClinicalTrials.gov API from the following query and filters. "
            f"Incorporate synonyms, alternate search strategies, and structured API filters to improve relevance. "
            f"Return only a structured JSON object with valid ClinicalTrials.gov API parameters, with no extra text or explanation. "
            f"Query: {query}\nFilters: {json.dumps(filters, indent=2)}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": CTG_API_SCHEMA},
                {"role": "user", "content": prompt}
            ]
        )
        structured_query = response["choices"][0]["message"]["content"].strip()
        return json.loads(structured_query)  # Ensure strict JSON format
    except openai.OpenAIError as e:
        logger.error(f"Error generating AI suggestions: {e}", exc_info=True)
        return filters  # Fall back to filters if AI fails
    except json.JSONDecodeError as e:
        logger.error(f"AI response is not valid JSON: {e}", exc_info=True)
        return filters  # Prevent breaking on invalid AI responses
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return filters

@router.post("/gpt-query")
async def process_gpt_query(request: QueryRequest):
    """
    Process a GPT Copilot query and fetch clinical trial information.
    """
    try:
        filters = request.filters or {}
        logger.info(f"Filters received: {filters}")

        # Step 1: AI analysis using GPT-4 to generate structured query
        ai_analysis = get_ai_suggestions(request.query, filters)
        logger.info(f"AI Analysis: {ai_analysis}")

        # Step 2: Create refined query for search
        refined_query = ai_analysis  # Directly use AI-generated structured query
        logger.info(f"Refined Query: {refined_query}")

        # Step 3: Fetch clinical trial data
        trial_results = trials_service.fetch_trials(refined_query, filters)
        
        if not trial_results:
            trial_results = [{"message": "No trials found for the given query."}]
            logger.error("No trials found.")

        # Step 4: Prepare the response
        response_payload = {
            "query": request.query,
            "analysis": ai_analysis,
            "refined_query": refined_query,
            "result": trial_results,
            "filters_used": filters,
        }
        return response_payload

    except Exception as e:
        logger.error(f"Error in gpt-query route: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
