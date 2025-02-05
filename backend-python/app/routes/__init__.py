"""
  Routes Package

  this package contains route definitions for the application.

   Modules:
   - trial_routes: Routes for managing clinical trials.
   - company_routes: Routes for managing companies.
   - health: Health check routes.

   Usage:
   Import the necessary route modules from this package to define application endpoints.

   Example:
   from app.routes import trial_routes, company_routes, health
"""

from .trial_routes import *
from .company_routes import *
# from .health import * # TODO: add health check routes ehnr ready, need to be update to new schema and structurws