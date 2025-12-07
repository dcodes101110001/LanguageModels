"""CRM Integration - Salesforce"""
from typing import Optional, Dict, Any
from datetime import datetime
from ..config import config
from ..core.models import Contact, CRMActivity
from ..utils.logger import get_logger

logger = get_logger(__name__)


class SalesforceIntegration:
    """Salesforce CRM integration"""
    
    def __init__(self):
        self.username = config.salesforce.username
        self.password = config.salesforce.password
        self.security_token = config.salesforce.security_token
        self.sf = None
        
    def connect(self) -> bool:
        """
        Connect to Salesforce
        
        Returns:
            True if connection successful
        """
        try:
            if not all([self.username, self.password, self.security_token]):
                logger.warning("Salesforce credentials not configured, running in demo mode")
                return False
                
            from simple_salesforce import Salesforce
            
            self.sf = Salesforce(
                username=self.username,
                password=self.password,
                security_token=self.security_token
            )
            logger.info("Connected to Salesforce")
            return True
            
        except ImportError:
            logger.warning("simple-salesforce not installed, running in demo mode")
            return False
        except Exception as e:
            logger.error("Failed to connect to Salesforce", error=str(e))
            return False
    
    def create_lead(self, contact: Contact, company_info: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Create a lead in Salesforce
        
        Args:
            contact: Contact information
            company_info: Optional additional company information
            
        Returns:
            Lead ID if successful
        """
        if not self.sf:
            logger.info("Demo mode: Would create lead", contact=f"{contact.first_name} {contact.last_name}")
            return f"demo_lead_{contact.email or 'noemail'}"
        
        try:
            lead_data = {
                'FirstName': contact.first_name,
                'LastName': contact.last_name,
                'Company': contact.company,
                'Title': contact.job_title or '',
                'Email': contact.email or '',
                'Phone': contact.phone or '',
                'LeadSource': 'AI SDR Agent'
            }
            
            if company_info:
                if 'industry' in company_info:
                    lead_data['Industry'] = company_info['industry']
                if 'website' in company_info:
                    lead_data['Website'] = company_info['website']
            
            result = self.sf.Lead.create(lead_data)
            lead_id = result.get('id')
            
            logger.info("Lead created in Salesforce", lead_id=lead_id)
            return lead_id
            
        except Exception as e:
            logger.error("Error creating lead in Salesforce", error=str(e))
            return None
    
    def log_activity(self, activity: CRMActivity, lead_id: Optional[str] = None) -> bool:
        """
        Log an activity in Salesforce
        
        Args:
            activity: Activity to log
            lead_id: Optional lead ID to associate with
            
        Returns:
            True if successful
        """
        if not self.sf:
            logger.info(
                "Demo mode: Would log activity",
                activity_type=activity.activity_type,
                contact=activity.contact_email
            )
            return True
        
        try:
            task_data = {
                'Subject': activity.subject,
                'Description': activity.description,
                'Status': activity.status,
                'ActivityDate': activity.timestamp.strftime('%Y-%m-%d'),
                'Type': activity.activity_type
            }
            
            if lead_id:
                task_data['WhoId'] = lead_id
            
            result = self.sf.Task.create(task_data)
            logger.info("Activity logged in Salesforce", task_id=result.get('id'))
            return True
            
        except Exception as e:
            logger.error("Error logging activity in Salesforce", error=str(e))
            return False
    
    def update_lead_status(self, lead_id: str, status: str) -> bool:
        """
        Update lead status
        
        Args:
            lead_id: Lead ID
            status: New status
            
        Returns:
            True if successful
        """
        if not self.sf:
            logger.info("Demo mode: Would update lead status", lead_id=lead_id, status=status)
            return True
        
        try:
            self.sf.Lead.update(lead_id, {'Status': status})
            logger.info("Lead status updated", lead_id=lead_id, status=status)
            return True
            
        except Exception as e:
            logger.error("Error updating lead status", error=str(e))
            return False
    
    def search_contact(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Search for existing contact/lead by email
        
        Args:
            email: Contact email
            
        Returns:
            Contact/Lead data if found
        """
        if not self.sf:
            logger.info("Demo mode: Would search for contact", email=email)
            return None
        
        try:
            # Sanitize email input to prevent SOQL injection
            # Remove potentially dangerous characters
            sanitized_email = email.replace("'", "\\'").replace("\\", "\\\\")
            
            # Search in Leads first
            query = f"SELECT Id, FirstName, LastName, Company, Email, Status FROM Lead WHERE Email = '{sanitized_email}' LIMIT 1"
            result = self.sf.query(query)
            
            if result['totalSize'] > 0:
                return result['records'][0]
            
            # If not found in Leads, search Contacts
            query = f"SELECT Id, FirstName, LastName, Email FROM Contact WHERE Email = '{sanitized_email}' LIMIT 1"
            result = self.sf.query(query)
            
            if result['totalSize'] > 0:
                return result['records'][0]
            
            return None
            
        except Exception as e:
            logger.error("Error searching contact", error=str(e))
            return None
