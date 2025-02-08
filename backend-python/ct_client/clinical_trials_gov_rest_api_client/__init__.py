"""
A client library for accessing ClinicalTrials.gov REST API
"""
"""
A client library for accessing ClinicalTrials.gov REST API
"""
from .client import AuthenticatedClient, Client
from .client import Configuration
from .api.studies.fetch_study import sync as fetch_study_sync

__all__ = (
    "AuthenticatedClient",
    "Client",
    "Configuration",
    "fetch_study_sync",
)


__all__ = (
    "AuthenticatedClient",
    "Client",
    "ClinicalTrialsApi",
    "Configuration",
)
