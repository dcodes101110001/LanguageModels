"""Message Generation Module"""
from typing import Optional
from openai import OpenAI
from ..config import config
from ..core.models import Contact, Company, OutreachMessage
from ..utils.logger import get_logger

logger = get_logger(__name__)


class MessageGenerator:
    """Generates personalized outreach messages"""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.openai.api_key)
        self.model = config.openai.model
    
    def generate_cold_email(
        self,
        contact: Contact,
        company: Company,
        value_proposition: str,
        trigger_events: Optional[list] = None
    ) -> OutreachMessage:
        """
        Generate a personalized cold email
        
        Args:
            contact: Target contact
            company: Contact's company
            value_proposition: Your product/service value proposition
            trigger_events: Optional list of recent trigger events
            
        Returns:
            OutreachMessage with subject and body
        """
        logger.info("Generating cold email", contact=f"{contact.first_name} {contact.last_name}")
        
        trigger_context = ""
        if trigger_events and len(trigger_events) > 0:
            trigger_context = f"\n\nRecent company developments:\n" + "\n".join(f"- {event}" for event in trigger_events)
        
        prompt = f"""
You are an expert sales development representative. Write a highly personalized cold email.

Contact Information:
- Name: {contact.first_name} {contact.last_name}
- Title: {contact.job_title or 'Decision Maker'}
- Company: {contact.company}

Company Information:
- Industry: {company.industry or 'Unknown'}
- Description: {company.description or 'N/A'}
{trigger_context}

Value Proposition:
{value_proposition}

Requirements:
1. Keep it concise (150-200 words max)
2. Reference specific trigger events or company context if available
3. Focus on value, not features
4. Include a clear, low-friction call-to-action
5. Professional but conversational tone
6. Avoid hype or overselling

Provide your response as JSON with keys:
- "subject": Email subject line (compelling, under 50 characters)
- "body": Email body (personalized, value-focused)
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert B2B sales development representative. Respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            message = OutreachMessage(
                contact=contact,
                subject=result.get("subject", "Quick question"),
                body=result.get("body", ""),
                channel="email"
            )
            
            logger.info("Cold email generated", contact=f"{contact.first_name} {contact.last_name}")
            return message
            
        except Exception as e:
            logger.error("Error generating cold email", error=str(e))
            return OutreachMessage(
                contact=contact,
                subject="Error generating email",
                body=f"Error: {str(e)}",
                channel="email"
            )
    
    def generate_linkedin_message(
        self,
        contact: Contact,
        company: Company,
        value_proposition: str
    ) -> OutreachMessage:
        """
        Generate a personalized LinkedIn connection request or message
        
        Args:
            contact: Target contact
            company: Contact's company
            value_proposition: Your product/service value proposition
            
        Returns:
            OutreachMessage for LinkedIn
        """
        logger.info("Generating LinkedIn message", contact=f"{contact.first_name} {contact.last_name}")
        
        prompt = f"""
You are an expert at LinkedIn networking. Write a brief, personalized LinkedIn connection message.

Contact Information:
- Name: {contact.first_name} {contact.last_name}
- Title: {contact.job_title or 'Professional'}
- Company: {contact.company}

Company Information:
- Industry: {company.industry or 'Unknown'}

Value Proposition:
{value_proposition}

Requirements:
1. Keep it very brief (under 300 characters for connection request OR under 200 words for InMail)
2. Be genuine and professional
3. Reference their role or company
4. Soft value mention without being salesy
5. Create curiosity

Provide your response as JSON with keys:
- "subject": Message subject (for InMail, under 40 characters)
- "body": Message body (brief and personalized)
- "message_type": Either "connection_request" or "inmail"
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a LinkedIn networking expert. Respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            message = OutreachMessage(
                contact=contact,
                subject=result.get("subject", "Let's connect"),
                body=result.get("body", ""),
                channel="linkedin"
            )
            
            logger.info("LinkedIn message generated", contact=f"{contact.first_name} {contact.last_name}")
            return message
            
        except Exception as e:
            logger.error("Error generating LinkedIn message", error=str(e))
            return OutreachMessage(
                contact=contact,
                subject="Error generating message",
                body=f"Error: {str(e)}",
                channel="linkedin"
            )
    
    def generate_follow_up(
        self,
        contact: Contact,
        previous_message: str,
        days_since_last_contact: int
    ) -> OutreachMessage:
        """
        Generate a follow-up message
        
        Args:
            contact: Target contact
            previous_message: Previous message sent
            days_since_last_contact: Days since last outreach
            
        Returns:
            Follow-up message
        """
        logger.info("Generating follow-up", contact=f"{contact.first_name} {contact.last_name}")
        
        prompt = f"""
Generate a brief follow-up email for a cold outreach that received no response.

Contact: {contact.first_name} {contact.last_name}
Days since last contact: {days_since_last_contact}

Previous message:
{previous_message}

Requirements:
1. Keep it very brief (under 100 words)
2. Add new value or insight
3. Make it easy to respond
4. Don't be pushy
5. Consider timing (adjust tone based on days passed)

Provide JSON with keys: "subject", "body"
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a sales follow-up expert. Respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            message = OutreachMessage(
                contact=contact,
                subject=result.get("subject", "Following up"),
                body=result.get("body", ""),
                channel="email"
            )
            
            logger.info("Follow-up generated")
            return message
            
        except Exception as e:
            logger.error("Error generating follow-up", error=str(e))
            return OutreachMessage(
                contact=contact,
                subject="Following up",
                body=f"Error: {str(e)}",
                channel="email"
            )
