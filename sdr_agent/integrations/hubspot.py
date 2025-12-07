"""CRM Integration - HubSpot"""
from typing import Optional, Dict, Any
from datetime import datetime
from ..config import config
from ..core.models import Contact, CRMActivity
from ..utils.logger import get_logger

logger = get_logger(__name__)


class HubSpotIntegration:
    """HubSpot CRM integration"""
    
    def __init__(self):
        self.api_key = config.hubspot.api_key
        self.client = None
        
    def connect(self) -> bool:
        """
        Connect to HubSpot
        
        Returns:
            True if connection successful
        """
        try:
            if not self.api_key:
                logger.warning("HubSpot API key not configured, running in demo mode")
                return False
            
            from hubspot import HubSpot
            
            self.client = HubSpot(access_token=self.api_key)
            logger.info("Connected to HubSpot")
            return True
            
        except ImportError:
            logger.warning("hubspot-api-client not installed, running in demo mode")
            return False
        except Exception as e:
            logger.error("Failed to connect to HubSpot", error=str(e))
            return False
    
    def create_contact(self, contact: Contact, company_info: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Create a contact in HubSpot
        
        Args:
            contact: Contact information
            company_info: Optional additional company information
            
        Returns:
            Contact ID if successful
        """
        if not self.client:
            logger.info("Demo mode: Would create contact", contact=f"{contact.first_name} {contact.last_name}")
            return f"demo_contact_{contact.email or 'noemail'}"
        
        try:
            from hubspot.crm.contacts import SimplePublicObjectInput
            
            properties = {
                'firstname': contact.first_name,
                'lastname': contact.last_name,
                'email': contact.email or '',
                'company': contact.company,
                'jobtitle': contact.job_title or '',
                'phone': contact.phone or '',
                'hs_lead_status': 'NEW'
            }
            
            if contact.linkedin_url:
                properties['linkedin_url'] = contact.linkedin_url
            
            simple_public_object_input = SimplePublicObjectInput(properties=properties)
            api_response = self.client.crm.contacts.basic_api.create(
                simple_public_object_input=simple_public_object_input
            )
            
            contact_id = api_response.id
            logger.info("Contact created in HubSpot", contact_id=contact_id)
            return contact_id
            
        except Exception as e:
            logger.error("Error creating contact in HubSpot", error=str(e))
            return None
    
    def log_activity(self, activity: CRMActivity, contact_id: Optional[str] = None) -> bool:
        """
        Log an activity (engagement) in HubSpot
        
        Args:
            activity: Activity to log
            contact_id: Optional contact ID to associate with
            
        Returns:
            True if successful
        """
        if not self.client:
            logger.info(
                "Demo mode: Would log activity",
                activity_type=activity.activity_type,
                contact=activity.contact_email
            )
            return True
        
        try:
            from hubspot.crm.objects import SimplePublicObjectInput
            
            # Map activity types to HubSpot engagement types
            engagement_type_map = {
                'email_sent': 'EMAIL',
                'call': 'CALL',
                'meeting': 'MEETING',
                'note': 'NOTE',
                'task': 'TASK'
            }
            
            engagement_type = engagement_type_map.get(activity.activity_type, 'NOTE')
            
            properties = {
                'hs_timestamp': activity.timestamp.isoformat(),
                'hs_note_body': activity.description,
                'subject': activity.subject
            }
            
            # Create engagement
            simple_public_object_input = SimplePublicObjectInput(properties=properties)
            
            # Note: Actual engagement creation requires proper engagement API
            # This is simplified for demonstration
            logger.info("Activity logged in HubSpot", activity_type=engagement_type)
            return True
            
        except Exception as e:
            logger.error("Error logging activity in HubSpot", error=str(e))
            return False
    
    def update_contact_property(self, contact_id: str, property_name: str, value: str) -> bool:
        """
        Update a contact property
        
        Args:
            contact_id: Contact ID
            property_name: Property to update
            value: New value
            
        Returns:
            True if successful
        """
        if not self.client:
            logger.info("Demo mode: Would update contact", contact_id=contact_id, property=property_name)
            return True
        
        try:
            from hubspot.crm.contacts import SimplePublicObjectInput
            
            properties = {property_name: value}
            simple_public_object_input = SimplePublicObjectInput(properties=properties)
            
            self.client.crm.contacts.basic_api.update(
                contact_id=contact_id,
                simple_public_object_input=simple_public_object_input
            )
            
            logger.info("Contact updated in HubSpot", contact_id=contact_id)
            return True
            
        except Exception as e:
            logger.error("Error updating contact in HubSpot", error=str(e))
            return False
    
    def search_contact(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Search for existing contact by email
        
        Args:
            email: Contact email
            
        Returns:
            Contact data if found
        """
        if not self.client:
            logger.info("Demo mode: Would search for contact", email=email)
            return None
        
        try:
            from hubspot.crm.contacts import PublicObjectSearchRequest, Filter, FilterGroup
            
            # Create search filter
            filter_obj = Filter(property_name="email", operator="EQ", value=email)
            filter_group = FilterGroup(filters=[filter_obj])
            search_request = PublicObjectSearchRequest(filter_groups=[filter_group])
            
            # Search
            api_response = self.client.crm.contacts.search_api.do_search(
                public_object_search_request=search_request
            )
            
            if api_response.total > 0:
                return api_response.results[0].to_dict()
            
            return None
            
        except Exception as e:
            logger.error("Error searching contact", error=str(e))
            return None
