"""Main SDR Agent Orchestrator"""
from typing import List, Optional, Dict, Any
from datetime import datetime

from .config import config
from .core.models import IdealCustomerProfile, Company, Contact, OutreachMessage, CRMActivity
from .core.icp_identifier import ICPIdentifier
from .core.researcher import CompanyResearcher
from .core.message_generator import MessageGenerator
from .integrations.salesforce import SalesforceIntegration
from .integrations.hubspot import HubSpotIntegration
from .integrations.email import EmailIntegration
from .utils.logger import get_logger

logger = get_logger(__name__)


class SDRAgent:
    """
    Autonomous Sales Development Representative Agent
    
    This agent performs the entire top-of-funnel sales process autonomously:
    - Identifies ideal customer profiles (ICPs)
    - Researches company news and trigger events
    - Generates personalized, context-aware cold emails/messages
    - Logs activities in CRM systems
    """
    
    def __init__(self, crm_type: str = "salesforce"):
        """
        Initialize SDR Agent
        
        Args:
            crm_type: CRM system to use ("salesforce" or "hubspot")
        """
        logger.info("Initializing SDR Agent", crm_type=crm_type)
        
        # Validate configuration
        missing = config.validate_required()
        if missing:
            logger.warning("Missing configuration", missing_fields=missing)
        
        # Initialize components
        self.icp_identifier = ICPIdentifier()
        self.researcher = CompanyResearcher()
        self.message_generator = MessageGenerator()
        self.email = EmailIntegration()
        
        # Initialize CRM
        self.crm_type = crm_type
        if crm_type == "salesforce":
            self.crm = SalesforceIntegration()
        elif crm_type == "hubspot":
            self.crm = HubSpotIntegration()
        else:
            raise ValueError(f"Unsupported CRM type: {crm_type}")
        
        # Connect to services
        self.crm.connect()
        self.email.connect()
        
        logger.info("SDR Agent initialized successfully")
    
    def process_prospect(
        self,
        company_name: str,
        icp: IdealCustomerProfile,
        value_proposition: str,
        company_website: Optional[str] = None,
        send_email: bool = False
    ) -> Dict[str, Any]:
        """
        Process a single prospect through the entire SDR workflow
        
        Args:
            company_name: Target company name
            icp: Ideal customer profile criteria
            value_proposition: Your product/service value proposition
            company_website: Optional company website
            send_email: Whether to actually send emails (False = demo mode)
            
        Returns:
            Dictionary with processing results
        """
        logger.info("Processing prospect", company=company_name)
        
        results = {
            'company': company_name,
            'timestamp': datetime.now().isoformat(),
            'steps_completed': [],
            'contacts_identified': 0,
            'messages_generated': 0,
            'emails_sent': 0,
            'crm_logged': False,
            'errors': []
        }
        
        try:
            # Step 1: Research the company
            logger.info("Step 1: Researching company")
            company = self.researcher.research_company(company_name, company_website)
            results['steps_completed'].append('research_company')
            
            # Step 2: Analyze ICP fit
            logger.info("Step 2: Analyzing ICP fit")
            icp_analysis = self.icp_identifier.analyze_icp_fit(company, icp)
            results['icp_fit_score'] = icp_analysis.get('fit_score', 0)
            results['icp_reasoning'] = icp_analysis.get('reasoning', '')
            results['steps_completed'].append('analyze_icp')
            
            # If fit score is too low, skip this prospect
            if icp_analysis.get('fit_score', 0) < 50:
                logger.info("Low ICP fit score, skipping", score=icp_analysis.get('fit_score'))
                results['skipped'] = True
                results['skip_reason'] = 'Low ICP fit score'
                return results
            
            # Step 3: Identify trigger events
            logger.info("Step 3: Identifying trigger events")
            trigger_events = self.researcher.identify_trigger_events(company)
            results['trigger_events'] = trigger_events
            results['steps_completed'].append('identify_triggers')
            
            # Step 4: Gather company news
            logger.info("Step 4: Gathering company news")
            news = self.researcher.gather_company_news(company)
            results['company_news'] = news
            results['steps_completed'].append('gather_news')
            
            # Step 5: Identify decision makers
            logger.info("Step 5: Identifying decision makers")
            contacts = self.icp_identifier.identify_decision_makers(company, icp.job_titles)
            results['contacts_identified'] = len(contacts)
            results['steps_completed'].append('identify_contacts')
            
            if not contacts:
                logger.warning("No contacts identified")
                results['errors'].append("No contacts identified")
                return results
            
            # Step 6: Generate personalized messages for each contact
            logger.info("Step 6: Generating personalized messages")
            messages = []
            for contact in contacts:
                message = self.message_generator.generate_cold_email(
                    contact=contact,
                    company=company,
                    value_proposition=value_proposition,
                    trigger_events=trigger_events[:2]  # Use top 2 trigger events
                )
                messages.append(message)
            
            results['messages_generated'] = len(messages)
            results['steps_completed'].append('generate_messages')
            
            # Step 7: Send emails (if enabled)
            if send_email:
                logger.info("Step 7: Sending emails")
                email_results = self.email.send_bulk_emails(messages)
                results['emails_sent'] = email_results['sent']
                results['email_errors'] = email_results['errors']
                results['steps_completed'].append('send_emails')
            else:
                logger.info("Step 7: Skipping email send (demo mode)")
                results['messages'] = [
                    {
                        'to': f"{msg.contact.first_name} {msg.contact.last_name}",
                        'email': msg.contact.email or 'N/A',
                        'subject': msg.subject,
                        'body': msg.body
                    }
                    for msg in messages
                ]
            
            # Step 8: Log activities in CRM
            logger.info("Step 8: Logging activities in CRM")
            for contact in contacts:
                # Create/update contact in CRM
                company_info = {
                    'industry': company.industry,
                    'website': company.website,
                    'description': company.description
                }
                
                if self.crm_type == "salesforce":
                    lead_id = self.crm.create_lead(contact, company_info)
                    
                    # Log email activity
                    for message in messages:
                        if message.contact.email == contact.email:
                            activity = self.email.create_activity_log(message)
                            self.crm.log_activity(activity, lead_id)
                            
                elif self.crm_type == "hubspot":
                    contact_id = self.crm.create_contact(contact, company_info)
                    
                    # Log email activity
                    for message in messages:
                        if message.contact.email == contact.email:
                            activity = self.email.create_activity_log(message)
                            self.crm.log_activity(activity, contact_id)
            
            results['crm_logged'] = True
            results['steps_completed'].append('log_crm')
            
            logger.info("Prospect processing complete", company=company_name)
            
        except Exception as e:
            logger.error("Error processing prospect", error=str(e))
            results['errors'].append(str(e))
        
        return results
    
    def process_prospect_list(
        self,
        prospects: List[Dict[str, str]],
        icp: IdealCustomerProfile,
        value_proposition: str,
        send_email: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Process a list of prospects
        
        Args:
            prospects: List of prospect dicts with 'name' and optional 'website'
            icp: Ideal customer profile criteria
            value_proposition: Your product/service value proposition
            send_email: Whether to actually send emails
            
        Returns:
            List of processing results for each prospect
        """
        logger.info("Processing prospect list", count=len(prospects))
        
        all_results = []
        
        for prospect in prospects:
            company_name = prospect.get('name')
            company_website = prospect.get('website')
            
            if not company_name:
                logger.warning("Skipping prospect with no name")
                continue
            
            result = self.process_prospect(
                company_name=company_name,
                icp=icp,
                value_proposition=value_proposition,
                company_website=company_website,
                send_email=send_email
            )
            
            all_results.append(result)
        
        logger.info("Prospect list processing complete", total=len(all_results))
        return all_results
    
    def generate_campaign_report(self, results: List[Dict[str, Any]]) -> str:
        """
        Generate a summary report of a campaign
        
        Args:
            results: List of processing results
            
        Returns:
            Formatted report string
        """
        total_prospects = len(results)
        processed = len([r for r in results if not r.get('skipped')])
        skipped = len([r for r in results if r.get('skipped')])
        total_contacts = sum(r.get('contacts_identified', 0) for r in results)
        total_messages = sum(r.get('messages_generated', 0) for r in results)
        total_sent = sum(r.get('emails_sent', 0) for r in results)
        
        report = f"""
SDR Campaign Report
==================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Summary:
--------
Total Prospects: {total_prospects}
Processed: {processed}
Skipped (Low ICP Fit): {skipped}
Total Contacts Identified: {total_contacts}
Total Messages Generated: {total_messages}
Total Emails Sent: {total_sent}

Prospect Details:
----------------
"""
        
        for result in results:
            company = result.get('company', 'Unknown')
            fit_score = result.get('icp_fit_score', 'N/A')
            contacts = result.get('contacts_identified', 0)
            messages = result.get('messages_generated', 0)
            
            report += f"\n{company}:\n"
            report += f"  ICP Fit Score: {fit_score}\n"
            report += f"  Contacts: {contacts}\n"
            report += f"  Messages: {messages}\n"
            
            if result.get('skipped'):
                report += f"  Status: SKIPPED - {result.get('skip_reason', 'Unknown')}\n"
            else:
                report += f"  Status: PROCESSED\n"
        
        return report
