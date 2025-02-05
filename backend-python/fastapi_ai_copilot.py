from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests
import os
from openai import OpenAI  # For AI query processing (if using GPT)
import json


# Initialize FastAPI
app = FastAPI()

# OpenAI API Key (Environment Variable)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not set in environment variables.")
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

# ClinicalTrials.gov API Endpoint
CTGOV_API_URL = "https://clinicaltrials.gov/api/v2/studies"

# Define Query Model
class QueryRequest(BaseModel):
    user_query: str

# AI Query Refinement Function (Using OpenAI GPT)
def refine_query(user_input: str) -> dict:
    """
    Process user input using GPT-4 to extract structured trial parameters.
    """
    Chat_Completion = client.chat.completions.create(
         messages=[
            {"role": "system", "content": "You are an AI assistant trained to refine clinical trial queries."},
            {"role": "user", "content": f"Refine this clinical trial query into structured parameters: {user_input}"}
        ]
        model="gpt-4o",
       
    )
    return Chat_Completion["choices"][0]["message"]["content"]

# Function to Query ClinicalTrials.gov
def fetch_trials(refined_query: dict):
    """
    Fetch structured trial data from ClinicalTrials.gov API.
    """
    params = {
        "query.term": refined_query.get("condition", ""),
        "query.phase": refined_query.get("phase", ""),
        "query.status": refined_query.get("status", ""),
        "format": "json"
    }
    response = requests.get(CTGOV_API_URL, params=params)
    return response.json()

# API Endpoint: Process User Query
@app.post("/query")
def process_query(query: QueryRequest):
    refined_query = refine_query(query.user_query)
    trial_data = fetch_trials(json.loads(refined_query))  # Convert GPT response to dict safely
    return {"query": refined_query, "results": trial_data}

# API Endpoint: Get Suggested Query Improvements
@app.get("/suggest")
def suggest_improvements(user_query: str = Query(..., description="User's trial search query")):
    suggestions = refine_query(user_query)
    return {"suggested_refinements": suggestions}
