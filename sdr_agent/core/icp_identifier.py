"""ICP Identification Module"""
from typing import List
from openai import OpenAI
from ..config import config
from ..core.models import IdealCustomerProfile, Company, Contact
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ICPIdentifier:
    """Identifies ideal customer profiles and potential leads"""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.openai.api_key)
        self.model = config.openai.model
    
    def analyze_icp_fit(self, company: Company, icp: IdealCustomerProfile) -> dict:
        """
        Analyze how well a company fits the ICP criteria
        
        Args:
            company: Company to analyze
            icp: Ideal customer profile criteria
            
        Returns:
            Dictionary with fit score and reasoning
        """
        logger.info("Analyzing ICP fit", company=company.name)
        
        prompt = f"""
You are an expert sales analyst. Analyze if the following company matches the ideal customer profile.

Company Information:
- Name: {company.name}
- Industry: {company.industry or 'Unknown'}
- Size: {company.size or 'Unknown'} employees
- Location: {company.location or 'Unknown'}
- Description: {company.description or 'Not available'}

Ideal Customer Profile:
- Target Industry: {icp.industry}
- Company Size: {icp.company_size_min or 'Any'} - {icp.company_size_max or 'Any'} employees
- Geography: {icp.geography or 'Any'}
- Technologies: {', '.join(icp.technologies) if icp.technologies else 'Any'}

Provide a fit score (0-100) and brief reasoning for the score.
Format your response as JSON with keys: "fit_score" (integer), "reasoning" (string), "recommendation" (string).
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a sales analyst expert. Always respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            logger.info("ICP analysis complete", company=company.name, fit_score=result.get("fit_score"))
            return result
            
        except Exception as e:
            logger.error("Error analyzing ICP fit", error=str(e))
            return {
                "fit_score": 0,
                "reasoning": f"Error during analysis: {str(e)}",
                "recommendation": "Manual review required"
            }
    
    def identify_decision_makers(self, company: Company, job_titles: List[str]) -> List[Contact]:
        """
        Identify potential decision makers at a company
        
        Args:
            company: Target company
            job_titles: List of relevant job titles to look for
            
        Returns:
            List of potential contacts
        """
        logger.info("Identifying decision makers", company=company.name)
        
        # In a real implementation, this would integrate with LinkedIn Sales Navigator
        # For now, we'll create a template response
        
        prompt = f"""
Based on the company '{company.name}' in the {company.industry or 'unknown'} industry,
suggest 3 typical decision-maker contacts with the following job titles: {', '.join(job_titles)}.

Provide realistic example names and titles. Format as JSON array with keys: 
"first_name", "last_name", "job_title", "company".
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a B2B sales expert. Respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Convert to Contact objects
            contacts = []
            if "contacts" in result:
                for contact_data in result["contacts"]:
                    contacts.append(Contact(
                        first_name=contact_data.get("first_name", ""),
                        last_name=contact_data.get("last_name", ""),
                        job_title=contact_data.get("job_title", ""),
                        company=company.name
                    ))
            
            logger.info("Decision makers identified", count=len(contacts))
            return contacts
            
        except Exception as e:
            logger.error("Error identifying decision makers", error=str(e))
            return []
