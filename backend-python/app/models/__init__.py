"""
  Models Package

  This package contains data models used throughout the application.
  It includes models for companies, trials, and other entities.

  Submodules:
  - company: Defines the Company model and related operations.
  - trial: Defines the Trial model and related operations.

  Usage:
  Import the necessary models from this package to utilize the application's data layer.

  Example:
  from app.models import Company, Trial
  """

from .trial_analysis import TrialAnalysis
from .trial import ClinicalTrial
from .company import Company
from .analysis_options import AnalysisOptions# This file makes the models directory a Python package