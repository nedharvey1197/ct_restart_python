"""
Tests for TrialAnalysisService functionality.

This test file covers the near-term analytics functionality provided by TrialAnalysisService.
For current production functionality, see test_trial_analysis.py.
For future functionality, see tests/future_concepts/.
"""

import pytest
from ..models.trial import ClinicalTrial, TrialAnalytics
from ..services.trial_service import TrialAnalysisService
from .fixtures.load_real_data import get_sample_trials
from datetime import datetime

@pytest.mark.asyncio
async def test_analyze_batch():
    """Test batch analysis of trials."""
    # Get sample trials
    trials = await get_sample_trials()
    assert trials, "No sample trials found"
    
    # Convert to ClinicalTrial objects
    trial_objects = [ClinicalTrial(**trial) for trial in trials]
    
    # Analyze trials
    analytics = await TrialAnalysisService.analyze_batch(trial_objects)
    
    # Verify analytics structure
    assert isinstance(analytics, TrialAnalytics)
    assert hasattr(analytics, 'phase_distribution')
    assert hasattr(analytics, 'status_summary')
    assert hasattr(analytics, 'therapeutic_areas')
    assert hasattr(analytics, 'total_trials')
    assert hasattr(analytics, 'enrollment_stats')
    
    # Verify analytics content
    assert analytics.total_trials == len(trials)
    assert all(isinstance(count, int) for count in analytics.phase_distribution.values())
    assert all(isinstance(count, int) for count in analytics.status_summary.values())
    assert isinstance(analytics.enrollment_stats, dict)
    assert all(key in analytics.enrollment_stats for key in ['total', 'average', 'median']) 