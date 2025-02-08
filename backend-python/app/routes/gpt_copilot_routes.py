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

# Cached API schema instructions with structured response enforcement
CTG_API_SCHEMA = (
    "You are an expert in structuring clinical trial searches for ClinicalTrials.gov API. "
    "Extract and return optimized search parameters in a structured JSON format. "
    "Ensure the query is enhanced by incorporating relevant filters, synonyms, and alternate search strategies. "
    "Do not generate full queries—only return the extracted parameters in JSON format. "
    "Strictly follow this format: { 'query': '...', 'condition': '...', 'intervention': '...', 'study_start_date': 'YYYY-MM-DD', 'study_end_date': 'YYYY-MM-DD', 'phase': '...', 'sort_by': '...', 'page': 1 }. "
    "Ensure the output contains only JSON, without explanations or extra text. "
    "Example Output: { 'query': 'optimized search query', 'condition': 'oncology', 'intervention': 'immunotherapy', 'study_start_date': '2020-01-01', 'study_end_date': '2024-12-31', 'phase': 'Phase 3', 'sort_by': 'start_date', 'page': 1 }"
)

def get_ai_suggestions(query: str, filters: Dict) -> str:
    """
    Uses GPT-4 to generate an optimized search query based on user input.
    """
    try:
        prompt = (
            f"Enhance and extract structured search terms for ClinicalTrials.gov API from the following query and filters. "
            f"Incorporate synonyms, alternate search strategies, and structured API filters to improve relevance. "
            f"Return only a structured JSON object with valid ClinicalTrials.gov API parameters, with no extra text or explanation. "
            f"Query: {query}\nFilters: {json.dumps(filters, indent=2)}"
        )
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in structuring clinical trial searches."},
                {"role": "user", "content": prompt}
            ]
        )
        refined_query = response.choices[0].message.content
        return refined_query.strip()

    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}", exc_info=True)
        return "Error generating AI suggestions."

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return "An unexpected error occurred while generating AI suggestions."

    
@router.post("/gpt-query")
async def process_gpt_query(request: QueryRequest):
    """
    Process a GPT Copilot query and fetch clinical trial information.
    """
    try:
        filters = request.filters or {}
        logger.info(f"Filters received: {filters}")

        # Step 1: AI analysis
        ai_analysis = get_ai_suggestions(request.query, filters)
        logger.info(f"Results of GPT Query Processing: {ai_analysis}")

        # Step 2: Refine query for Knowledge Graph
        refined_query = {
            "query": get_ai_suggestions(request.query, filters),
            "hypothesis": request.hypothesis,
            **filters  # Merge extracted filters into refined_query
}
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
