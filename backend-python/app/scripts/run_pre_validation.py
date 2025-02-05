"""
Script to run pre-update validation before schema changes.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any
from app.system_specs.validation.pre_update import PreUpdateValidator

def format_validation_results(results: Dict[str, Any]) -> str:
    """Format validation results for display"""
    output = []
    
    # Handle error cases
    if "error" in results:
        return f"Validation failed: {results['error']}"
    
    # Summary section
    output.append("\n=== Validation Summary ===")
    summary = results.get("summary", {})
    output.append(f"Total Trials: {summary.get('trials', 0)}")
    output.append(f"Total Companies: {summary.get('companies', 0)}")
    output.append(f"Issues Found: {summary.get('issues_found', 0)}")
    
    # Issues section
    issues = results.get("issues", {})
    if issues:
        output.append("\n=== Issues ===")
        for severity, issue_list in issues.items():
            if issue_list:
                output.append(f"\n{severity.upper()}:")
                for issue in issue_list:
                    output.append(f"- {issue}")
    
    # Recommendations
    recommendations = results.get("recommendations", [])
    if recommendations:
        output.append("\n=== Recommendations ===")
        for rec in recommendations:
            output.append(f"- {rec}")
    
    # Detailed Results
    detailed = results.get("detailed_results", {})
    if detailed:
        output.append("\n=== Detailed Results ===")
        
        # Trial validation
        trials = detailed.get("trials", {})
        if trials and "error" not in trials:
            output.append("\nTrial Validation:")
            output.append(f"- Sample Size: {trials.get('sample_validated', 0)}")
            output.append(f"- Schema Compliant: {trials.get('schema_compliance', {}).get('compliant', 0)}")
            output.append(f"- Schema Non-Compliant: {trials.get('schema_compliance', {}).get('non_compliant', 0)}")
        
        # Company validation
        companies = detailed.get("companies", {})
        if companies and "error" not in companies:
            output.append("\nCompany Validation:")
            output.append(f"- Sample Size: {companies.get('sample_validated', 0)}")
            output.append(f"- Schema Compliant: {companies.get('schema_compliance', {}).get('compliant', 0)}")
            output.append(f"- Schema Non-Compliant: {companies.get('schema_compliance', {}).get('non_compliant', 0)}")
        
        # Relationship validation
        relationships = detailed.get("relationships", {})
        if relationships:
            output.append("\nRelationship Validation:")
            orphaned = relationships.get("orphaned_references", {})
            output.append(f"- Orphaned Company References: {orphaned.get('company_orphans', 0)}")
            output.append(f"- Orphaned Trial References: {orphaned.get('trial_orphans', 0)}")
    
    # Final status
    output.append(f"\nSafe to Proceed: {'Yes' if results.get('safe_to_proceed', False) else 'No'}")
    
    return "\n".join(output)

async def main():
    print(f"Starting pre-update validation at {datetime.utcnow()}")
    try:
        async with PreUpdateValidator() as validator:
            results = await validator.validate_current_state()
            
            # Format and display results
            print(format_validation_results(results))
            
            # Save results to file
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"validation_report_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, default=str, indent=2)
            print(f"\nDetailed report saved to: {filename}")
            
            return results.get("safe_to_proceed", False)
    except Exception as e:
        print(f"Error during validation: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)  # Use exit code to indicate success/failure
