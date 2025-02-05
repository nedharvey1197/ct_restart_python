"""
Pre-update validation to ensure safe schema transitions.
Validates current system state before making schema updates.
"""

from datetime import datetime
import asyncio
from typing import Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config.database import MongoDB
from app.system_specs.schemas import EnhancedCompany, EnhancedTrial, RelationshipBase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

class PreUpdateValidator:
    """Validates current system state before schema updates"""
    
    SAMPLE_SIZE = 100
    OPERATION_TIMEOUT = 30  # 30 seconds timeout for operations

    def __init__(self):
        self.validation_results = {}
        
    async def __aenter__(self):
        await MongoDB.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await MongoDB.close()
        
    async def validate_current_state(self) -> Dict[str, Any]:
        """
        Validates current database state and returns detailed report
        """
        try:
            self.validation_results = {
                "timestamp": datetime.utcnow(),
                "trials": await self._validate_trials(),
                "companies": await self._validate_companies(),
                "relationships": await self._validate_relationships(),
                "data_integrity": await self._check_data_integrity()
            }
            return self.generate_validation_report()
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            return {
                "error": f"Database connection error: {str(e)}",
                "timestamp": datetime.utcnow(),
                "status": "failed"
            }
        except asyncio.TimeoutError:
            return {
                "error": "Operation timed out",
                "timestamp": datetime.utcnow(),
                "status": "timeout"
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}",
                "timestamp": datetime.utcnow(),
                "status": "error"
            }

    async def _validate_trials(self) -> Dict[str, Any]:
        """Validate trial documents"""
        try:
            async with MongoDB.get_collection("trials") as collection:
                trial_count = await asyncio.wait_for(
                    collection.count_documents({}),
                    timeout=self.OPERATION_TIMEOUT
                )
                
                sample = await asyncio.wait_for(
                    collection.find().limit(self.SAMPLE_SIZE).to_list(None),
                    timeout=self.OPERATION_TIMEOUT
                )

                required_fields = ["nct_id", "title", "status"]
                field_presence = self._check_required_fields(sample, required_fields)
                
                return {
                    "total_count": trial_count,
                    "sample_validated": len(sample),
                    "fields_present": field_presence,
                    "schema_compliance": self._check_schema_compliance(sample, EnhancedTrial)
                }
        except asyncio.TimeoutError:
            return {
                "error": "Trial validation timed out",
                "status": "timeout"
            }
        except Exception as e:
            return {
                "error": f"Trial validation error: {str(e)}",
                "status": "error"
            }

    async def _validate_companies(self) -> Dict[str, Any]:
        """Validate company documents"""
        try:
            async with MongoDB.get_collection("companies") as collection:
                company_count = await asyncio.wait_for(
                    collection.count_documents({}),
                    timeout=self.OPERATION_TIMEOUT
                )
                
                sample = await asyncio.wait_for(
                    collection.find().limit(self.SAMPLE_SIZE).to_list(None),
                    timeout=self.OPERATION_TIMEOUT
                )

                required_fields = ["name", "company_identifiers", "status"]
                field_presence = self._check_required_fields(sample, required_fields)
                
                return {
                    "total_count": company_count,
                    "sample_validated": len(sample),
                    "fields_present": field_presence,
                    "schema_compliance": self._check_schema_compliance(sample, EnhancedCompany)
                }
        except asyncio.TimeoutError:
            return {
                "error": "Company validation timed out",
                "status": "timeout"
            }
        except Exception as e:
            return {
                "error": f"Company validation error: {str(e)}",
                "status": "error"
            }

    async def _validate_relationships(self) -> Dict[str, Any]:
        """Check existing relationships between entities"""
        company_relationships = await self._check_company_relationships()
        trial_relationships = await self._check_trial_relationships()
        orphaned = await self._check_orphaned_references()
        
        return {
            "company_relationships": company_relationships,
            "trial_relationships": trial_relationships,
            "orphaned_references": orphaned,
            "integrity_check": await self._validate_relationship_integrity()
        }
    
    async def _check_company_relationships(self) -> Dict[str, Any]:
        """Validate company relationship structures"""
        try:
            async with MongoDB.get_collection("companies") as collection:
                companies = await asyncio.wait_for(
                    collection.find(
                        {"relationships": {"$exists": True}},
                        {"relationships": 1}
                    ).to_list(None),
                    timeout=self.OPERATION_TIMEOUT
                )
                
                results = {
                    "total_with_relationships": len(companies),
                    "valid_structure": 0,
                    "invalid_structure": 0,
                    "errors": []
                }
                
                for company in companies:
                    try:
                        if "relationships" in company:
                            for rel_type, rels in company.get("relationships", {}).items():
                                for rel in rels:
                                    RelationshipBase(**rel)
                            results["valid_structure"] += 1
                    except Exception as e:
                        results["invalid_structure"] += 1
                        results["errors"].append(str(e))
                
                return results
        except asyncio.TimeoutError:
            return {
                "error": "Relationship validation timed out",
                "status": "timeout"
            }
        except Exception as e:
            return {
                "error": f"Relationship validation error: {str(e)}",
                "status": "error"
            }
    
    async def _check_trial_relationships(self) -> Dict[str, Any]:
        """Validate trial relationship structures"""
        try:
            async with MongoDB.get_collection("trials") as collection:
                trials = await asyncio.wait_for(
                    collection.find(
                        {"relationships": {"$exists": True}},
                        {"relationships": 1}
                    ).to_list(None),
                    timeout=self.OPERATION_TIMEOUT
                )
                
                results = {
                    "total_with_relationships": len(trials),
                    "valid_structure": 0,
                    "invalid_structure": 0,
                    "errors": []
                }
                
                for trial in trials:
                    try:
                        if "relationships" in trial:
                            for rel_type, rels in trial.get("relationships", {}).items():
                                for rel in rels:
                                    RelationshipBase(**rel)
                            results["valid_structure"] += 1
                    except Exception as e:
                        results["invalid_structure"] += 1
                        results["errors"].append(str(e))
                
                return results
        except asyncio.TimeoutError:
            return {
                "error": "Trial relationship validation timed out",
                "status": "timeout"
            }
        except Exception as e:
            return {
                "error": f"Trial relationship validation error: {str(e)}",
                "status": "error"
            }
    
    async def _check_orphaned_references(self) -> Dict[str, Any]:
        """Check for orphaned relationship references"""
        try:
            results = {
                "company_orphans": 0,
                "trial_orphans": 0,
                "details": []
            }
            
            # Check company relationships for valid trial references
            async with MongoDB.get_collection("companies") as companies_collection:
                async with MongoDB.get_collection("trials") as trials_collection:
                    companies = await asyncio.wait_for(
                        companies_collection.find({"relationships": {"$exists": True}}).to_list(None),
                        timeout=self.OPERATION_TIMEOUT
                    )
                    
                    for company in companies:
                        for rel_type, rels in company.get("relationships", {}).items():
                            for rel in rels:
                                if "target_id" in rel:
                                    target_exists = await asyncio.wait_for(
                                        trials_collection.count_documents({"_id": rel["target_id"]}),
                                        timeout=self.OPERATION_TIMEOUT
                                    )
                                    if not target_exists:
                                        results["trial_orphans"] += 1
                                        results["details"].append(
                                            f"Company {company['_id']} has orphaned trial reference {rel['target_id']}"
                                        )
                    
                    # Check trial relationships for valid company references
                    trials = await asyncio.wait_for(
                        trials_collection.find({"relationships": {"$exists": True}}).to_list(None),
                        timeout=self.OPERATION_TIMEOUT
                    )
                    
                    for trial in trials:
                        for rel_type, rels in trial.get("relationships", {}).items():
                            for rel in rels:
                                if "target_id" in rel:
                                    target_exists = await asyncio.wait_for(
                                        companies_collection.count_documents({"_id": rel["target_id"]}),
                                        timeout=self.OPERATION_TIMEOUT
                                    )
                                    if not target_exists:
                                        results["company_orphans"] += 1
                                        results["details"].append(
                                            f"Trial {trial['_id']} has orphaned company reference {rel['target_id']}"
                                        )
            
            return results
        except asyncio.TimeoutError:
            return {
                "error": "Orphaned reference check timed out",
                "status": "timeout"
            }
        except Exception as e:
            return {
                "error": f"Orphaned reference check error: {str(e)}",
                "status": "error"
            }

    async def _validate_relationship_integrity(self) -> Dict[str, bool]:
        """Validate relationship integrity between entities"""
        return {
            "bidirectional_valid": await self._check_bidirectional_relationships(),
            "no_self_references": await self._check_self_references(),
            "valid_relationship_types": await self._check_relationship_types()
        }
    
    async def _check_data_integrity(self) -> Dict[str, Any]:
        """Validate data integrity across collections"""
        return {
            "duplicate_trials": await self._check_duplicate_trials(),
            "duplicate_companies": await self._check_duplicate_companies(),
            "invalid_references": await self._check_invalid_references()
        }
    
    def generate_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report with recommendations"""
        issues = self._identify_issues()
        
        return {
            "timestamp": self.validation_results["timestamp"],
            "summary": {
                "trials": self.validation_results["trials"]["total_count"],
                "companies": self.validation_results["companies"]["total_count"],
                "issues_found": len(issues)
            },
            "detailed_results": self.validation_results,
            "issues": issues,
            "recommendations": self._generate_recommendations(issues),
            "safe_to_proceed": len(issues.get("critical", [])) == 0
        }
    
    def _identify_issues(self) -> Dict[str, List[str]]:
        """Identify issues from validation results"""
        issues = {
            "critical": [],
            "warnings": [],
            "info": []
        }
        
        # Add logic to identify specific issues
        return issues
    
    def _generate_recommendations(self, issues: Dict[str, List[str]]) -> List[str]:
        """Generate recommendations based on identified issues"""
        recommendations = []
        
        if issues["critical"]:
            recommendations.append("Must resolve critical issues before proceeding")
            
        # Add specific recommendations based on issues
        return recommendations

    def _check_schema_compliance(self, documents: List[Dict], schema_class) -> Dict[str, Any]:
        """Check if documents comply with schema"""
        results = {
            "compliant": 0,
            "non_compliant": 0,
            "errors": []
        }
        
        for doc in documents:
            try:
                schema_class(**doc)
                results["compliant"] += 1
            except Exception as e:
                results["non_compliant"] += 1
                results["errors"].append(str(e))
        
        return results

    async def _check_bidirectional_relationships(self) -> bool:
        """Check if relationships are properly bidirectional"""
        try:
            async with MongoDB.get_collection("companies") as companies_collection:
                async with MongoDB.get_collection("trials") as trials_collection:
                    # Get all relationships
                    companies = await asyncio.wait_for(
                        companies_collection.find({"relationships": {"$exists": True}}).to_list(None),
                        timeout=self.OPERATION_TIMEOUT
                    )
                    trials = await asyncio.wait_for(
                        trials_collection.find({"relationships": {"$exists": True}}).to_list(None),
                        timeout=self.OPERATION_TIMEOUT
                    )
                    
                    # Check company -> trial relationships
                    for company in companies:
                        for rel_type, rels in company.get("relationships", {}).items():
                            for rel in rels:
                                if "target_id" in rel:
                                    trial = await trials_collection.find_one({"_id": rel["target_id"]})
                                    if not trial or not self._check_reverse_relationship(trial, company["_id"], rel_type):
                                        return False
                    
                    # Check trial -> company relationships
                    for trial in trials:
                        for rel_type, rels in trial.get("relationships", {}).items():
                            for rel in rels:
                                if "target_id" in rel:
                                    company = await companies_collection.find_one({"_id": rel["target_id"]})
                                    if not company or not self._check_reverse_relationship(company, trial["_id"], rel_type):
                                        return False
                    
                    return True
        except (asyncio.TimeoutError, Exception):
            return False

    def _check_reverse_relationship(self, entity: Dict, source_id: str, rel_type: str) -> bool:
        """Helper method to check for reverse relationship"""
        if "relationships" not in entity:
            return False
        
        # Get the reverse relationship type (you might want to implement a proper mapping)
        reverse_type = f"reverse_{rel_type}"  # This is a simplistic example
        
        for rel in entity.get("relationships", {}).get(reverse_type, []):
            if rel.get("target_id") == source_id:
                return True
        return False

    async def _check_self_references(self) -> bool:
        """Check for invalid self-references in relationships"""
        try:
            async with MongoDB.get_collection("companies") as companies_collection:
                async with MongoDB.get_collection("trials") as trials_collection:
                    # Check companies
                    companies = await asyncio.wait_for(
                        companies_collection.find({"relationships": {"$exists": True}}).to_list(None),
                        timeout=self.OPERATION_TIMEOUT
                    )
                    for company in companies:
                        if self._has_self_reference(company):
                            return False
                    
                    # Check trials
                    trials = await asyncio.wait_for(
                        trials_collection.find({"relationships": {"$exists": True}}).to_list(None),
                        timeout=self.OPERATION_TIMEOUT
                    )
                    for trial in trials:
                        if self._has_self_reference(trial):
                            return False
                    
                    return True
        except (asyncio.TimeoutError, Exception):
            return False

    def _has_self_reference(self, entity: Dict) -> bool:
        """Helper method to check for self-references"""
        entity_id = entity.get("_id")
        for rel_type, rels in entity.get("relationships", {}).items():
            for rel in rels:
                if rel.get("target_id") == entity_id:
                    return True
        return False

    async def _check_relationship_types(self) -> bool:
        """Validate that all relationship types are valid"""
        VALID_RELATIONSHIP_TYPES = {
            "sponsor", "investigator", "collaborator", "site",
            "reverse_sponsor", "reverse_investigator", "reverse_collaborator", "reverse_site"
        }
        
        try:
            async with MongoDB.get_collection("companies") as companies_collection:
                async with MongoDB.get_collection("trials") as trials_collection:
                    # Check companies
                    companies = await asyncio.wait_for(
                        companies_collection.find({"relationships": {"$exists": True}}).to_list(None),
                        timeout=self.OPERATION_TIMEOUT
                    )
                    for company in companies:
                        if not all(rel_type in VALID_RELATIONSHIP_TYPES 
                                 for rel_type in company.get("relationships", {}).keys()):
                            return False
                    
                    # Check trials
                    trials = await asyncio.wait_for(
                        trials_collection.find({"relationships": {"$exists": True}}).to_list(None),
                        timeout=self.OPERATION_TIMEOUT
                    )
                    for trial in trials:
                        if not all(rel_type in VALID_RELATIONSHIP_TYPES 
                                 for rel_type in trial.get("relationships", {}).keys()):
                            return False
                    
                    return True
        except (asyncio.TimeoutError, Exception):
            return False

    def _check_required_fields(self, documents: List[Dict], required_fields: List[str]) -> Dict[str, Any]:
        """Check presence of required fields in documents"""
        results = {field: 0 for field in required_fields}
        total = len(documents)
        
        for doc in documents:
            for field in required_fields:
                if field in doc:
                    results[field] += 1
        
        # Convert to percentages
        return {field: (count / total * 100 if total > 0 else 0) 
                for field, count in results.items()}

    async def _check_duplicate_trials(self) -> Dict[str, Any]:
        """Check for duplicate trial entries"""
        try:
            async with MongoDB.get_collection("trials") as collection:
                pipeline = [
                    {"$group": {
                        "_id": "$nct_id",
                        "count": {"$sum": 1},
                        "ids": {"$push": "$_id"}
                    }},
                    {"$match": {"count": {"$gt": 1}}}
                ]
                
                duplicates = await asyncio.wait_for(
                    collection.aggregate(pipeline).to_list(None),
                    timeout=self.OPERATION_TIMEOUT
                )
                
                return {
                    "duplicate_count": len(duplicates),
                    "details": [{"nct_id": d["_id"], "count": d["count"], "ids": d["ids"]} 
                              for d in duplicates]
                }
        except asyncio.TimeoutError:
            return {
                "error": "Duplicate trial check timed out",
                "status": "timeout"
            }
        except Exception as e:
            return {
                "error": f"Duplicate trial check error: {str(e)}",
                "status": "error"
            }

    async def _check_duplicate_companies(self) -> Dict[str, Any]:
        """Check for duplicate company entries"""
        try:
            async with MongoDB.get_collection("companies") as collection:
                pipeline = [
                    {"$group": {
                        "_id": "$name",
                        "count": {"$sum": 1},
                        "ids": {"$push": "$_id"}
                    }},
                    {"$match": {"count": {"$gt": 1}}}
                ]
                
                duplicates = await asyncio.wait_for(
                    collection.aggregate(pipeline).to_list(None),
                    timeout=self.OPERATION_TIMEOUT
                )
                
                return {
                    "duplicate_count": len(duplicates),
                    "details": [{"name": d["_id"], "count": d["count"], "ids": d["ids"]} 
                              for d in duplicates]
                }
        except asyncio.TimeoutError:
            return {
                "error": "Duplicate company check timed out",
                "status": "timeout"
            }
        except Exception as e:
            return {
                "error": f"Duplicate company check error: {str(e)}",
                "status": "error"
            }

    async def _check_invalid_references(self) -> Dict[str, Any]:
        """Check for invalid references in both trials and companies"""
        try:
            results = {
                "invalid_trial_refs": 0,
                "invalid_company_refs": 0,
                "details": []
            }
            
            async with MongoDB.get_collection("companies") as companies_collection:
                async with MongoDB.get_collection("trials") as trials_collection:
                    # Check company references
                    companies = await asyncio.wait_for(
                        companies_collection.find({"trial_ids": {"$exists": True}}).to_list(None),
                        timeout=self.OPERATION_TIMEOUT
                    )
                    
                    for company in companies:
                        for trial_id in company.get("trial_ids", []):
                            trial_exists = await asyncio.wait_for(
                                trials_collection.count_documents({"_id": trial_id}),
                                timeout=self.OPERATION_TIMEOUT
                            )
                            if not trial_exists:
                                results["invalid_trial_refs"] += 1
                                results["details"].append(
                                    f"Company {company['_id']} has invalid trial reference: {trial_id}"
                                )
                    
                    # Check trial references
                    trials = await asyncio.wait_for(
                        trials_collection.find({"company_ids": {"$exists": True}}).to_list(None),
                        timeout=self.OPERATION_TIMEOUT
                    )
                    
                    for trial in trials:
                        for company_id in trial.get("company_ids", []):
                            company_exists = await asyncio.wait_for(
                                companies_collection.count_documents({"_id": company_id}),
                                timeout=self.OPERATION_TIMEOUT
                            )
                            if not company_exists:
                                results["invalid_company_refs"] += 1
                                results["details"].append(
                                    f"Trial {trial['_id']} has invalid company reference: {company_id}"
                                )
            
            return results
        except asyncio.TimeoutError:
            return {
                "error": "Invalid reference check timed out",
                "status": "timeout"
            }
        except Exception as e:
            return {
                "error": f"Invalid reference check error: {str(e)}",
                "status": "error"
            }