"""
Validation utility functions for system updates and migrations.
"""

async def validate_before_updates():
    validator = PreUpdateValidator()
    report = await validator.validate_current_state()
    
    if not report["safe_to_proceed"]:
        print("Critical issues found:")
        for issue in report["issues"]["critical"]:
            print(f"- {issue}")
        print("\nRecommendations:")
        for rec in report["recommendations"]:
            print(f"- {rec}")
        return False
        
    print("Validation passed - safe to proceed with updates")
    return True 