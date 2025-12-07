"""Company Research Module"""
import requests
from typing import List
from openai import OpenAI
from bs4 import BeautifulSoup
from ..config import config
from ..core.models import Company
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CompanyResearcher:
    """Researches companies and identifies trigger events"""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.openai.api_key)
        self.model = config.openai.model
    
    def research_company(self, company_name: str, website: str = None) -> Company:
        """
        Research a company and gather relevant information
        
        Args:
            company_name: Name of the company
            website: Optional company website
            
        Returns:
            Company object with gathered information
        """
        logger.info("Researching company", company=company_name)
        
        # In a real implementation, this would scrape the website or use APIs
        # For now, we'll use LLM to generate realistic company info
        
        prompt = f"""
Research and provide information about the company: {company_name}
{f"Website: {website}" if website else ""}

Provide the following information in JSON format:
- industry: Industry sector
- size: Approximate number of employees (integer)
- location: Headquarters location
- description: Brief company description (1-2 sentences)

Be realistic and if you don't know, use your best judgment based on the company name.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business research analyst. Respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            import json
            data = json.loads(response.choices[0].message.content)
            
            company = Company(
                name=company_name,
                website=website,
                industry=data.get("industry"),
                size=data.get("size"),
                location=data.get("location"),
                description=data.get("description")
            )
            
            logger.info("Company research complete", company=company_name)
            return company
            
        except Exception as e:
            logger.error("Error researching company", error=str(e))
            return Company(name=company_name, website=website)
    
    def identify_trigger_events(self, company: Company) -> List[str]:
        """
        Identify recent trigger events for a company
        
        Args:
            company: Company to research
            
        Returns:
            List of trigger events
        """
        logger.info("Identifying trigger events", company=company.name)
        
        # In production, this would search news APIs, press releases, etc.
        # For now, we'll use LLM to generate realistic trigger events
        
        prompt = f"""
Based on the company information below, suggest 2-3 realistic trigger events that would 
be good sales opportunities (e.g., funding rounds, new product launches, expansions, 
leadership changes, acquisitions).

Company: {company.name}
Industry: {company.industry or 'Unknown'}
Description: {company.description or 'N/A'}

Provide a JSON object with a "trigger_events" array of strings.
Each event should be a brief, realistic statement.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business intelligence analyst. Respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            trigger_events = result.get("trigger_events", [])
            
            company.trigger_events = trigger_events
            logger.info("Trigger events identified", count=len(trigger_events))
            return trigger_events
            
        except Exception as e:
            logger.error("Error identifying trigger events", error=str(e))
            return []
    
    def gather_company_news(self, company: Company) -> List[str]:
        """
        Gather recent news about a company
        
        Args:
            company: Company to research
            
        Returns:
            List of recent news items
        """
        logger.info("Gathering company news", company=company.name)
        
        # In production, this would use news APIs like Google News API, NewsAPI, etc.
        # For demo purposes, we'll generate realistic news items
        
        prompt = f"""
Generate 2-3 realistic recent news headlines about {company.name}, 
a company in the {company.industry or 'technology'} industry.

Provide a JSON object with a "news" array of strings.
Each headline should be professional and realistic.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business news analyst. Respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            news = result.get("news", [])
            
            company.recent_news = news
            logger.info("Company news gathered", count=len(news))
            return news
            
        except Exception as e:
            logger.error("Error gathering company news", error=str(e))
            return []
