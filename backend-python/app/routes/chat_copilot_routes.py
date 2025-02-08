from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from ..services.chat_copilot_services import refine_query, fetch_trials  # Import AI logic
import logging

logging.basicConfig(level=logging.INFO)  # And this
logger = logging.getLogger(__name__)     # And this

# Define the router with a prefix
router = APIRouter(prefix="/copilot", tags=["copilot"])

# Request and Response models
class QueryRequest(BaseModel):
    user_query: str

class QueryResponse(BaseModel):
    query: dict
    results: list

@router.post("/query", response_model=QueryResponse)
def process_query(query: QueryRequest) -> QueryResponse:
    """
    Processes a user query by refining it and fetching relevant trial data.
    """
    logger.info(f"Processing query: {query.user_query}")
    try:
        # Step 1: Refine the query using AI
        logging.info("Received user query: %s", query.user_query)
        refined_query = refine_query(query.user_query)
        logging.info("Refined query: %s", refined_query)

        # Step 2: Fetch trial data
        trial_data = fetch_trials(refined_query)
        logging.info("Raw trial data fetched: %s", trial_data)

        # Step 3: Validate and transform trial data
        if not trial_data:  # Handle empty responses
            trial_data = []
            logging.info("No trial data found. Returning an empty results list.")
        elif isinstance(trial_data, dict) and "studies" in trial_data:
            trial_data = trial_data["studies"]  # Extract the list of studies
            logging.info("Extracted studies from trial data: %s", trial_data)
        elif not isinstance(trial_data, list):
            raise ValueError("Invalid trial_data format; expected a list or dictionary with 'studies'.")

        # Step 4: Return a valid QueryResponse
        response = QueryResponse(query=refined_query, results=trial_data)
        logging.info("Constructed QueryResponse: %s", response)
        logger.info(f"Query processed successfully, response: {response}")
        return response

    except ValueError as e:
        logging.error("Validation error: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error("Unexpected error during query processing: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the query.")

@router.get("/suggest")
def suggest_improvements(user_query: str = Query(..., description="User's trial search query")):
    """
    Suggests query refinements based on the user's initial input.
    """
    try:
        logging.info("Received user query for suggestions: %s", user_query)
        suggestions = refine_query(user_query)
        logging.info("Generated suggestions: %s", suggestions)
        return {"suggested_refinements": suggestions}  # Returns AI-refined query improvements
    except Exception as e:
        logging.error("Error while suggesting improvements: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while generating suggestions.")
