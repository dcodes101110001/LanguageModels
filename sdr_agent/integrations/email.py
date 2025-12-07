"""Email Integration"""
from typing import Optional
from ..config import config
from ..core.models import OutreachMessage, CRMActivity
from ..utils.logger import get_logger

logger = get_logger(__name__)


class EmailIntegration:
    """Email sending integration using SendGrid"""
    
    def __init__(self):
        self.api_key = config.email.sendgrid_api_key
        self.from_email = config.email.from_email
        self.sg = None
        
    def connect(self) -> bool:
        """
        Initialize SendGrid client
        
        Returns:
            True if connection successful
        """
        try:
            if not self.api_key or not self.from_email:
                logger.warning("SendGrid not configured, running in demo mode")
                return False
            
            from sendgrid import SendGridAPIClient
            
            self.sg = SendGridAPIClient(api_key=self.api_key)
            logger.info("SendGrid client initialized")
            return True
            
        except ImportError:
            logger.warning("sendgrid not installed, running in demo mode")
            return False
        except Exception as e:
            logger.error("Failed to initialize SendGrid", error=str(e))
            return False
    
    def send_email(self, message: OutreachMessage) -> bool:
        """
        Send an email message
        
        Args:
            message: Outreach message to send
            
        Returns:
            True if email sent successfully
        """
        if not self.sg:
            logger.info(
                "Demo mode: Would send email",
                to=message.contact.email,
                subject=message.subject
            )
            return True
        
        if not message.contact.email:
            logger.error("Cannot send email: contact has no email address")
            return False
        
        try:
            from sendgrid.helpers.mail import Mail, Email, To, Content
            
            mail = Mail(
                from_email=Email(self.from_email),
                to_emails=To(message.contact.email),
                subject=message.subject,
                plain_text_content=Content("text/plain", message.body)
            )
            
            response = self.sg.send(mail)
            
            if response.status_code in [200, 201, 202]:
                logger.info(
                    "Email sent successfully",
                    to=message.contact.email,
                    status_code=response.status_code
                )
                return True
            else:
                logger.error(
                    "Email send failed",
                    status_code=response.status_code,
                    body=response.body
                )
                return False
                
        except Exception as e:
            logger.error("Error sending email", error=str(e))
            return False
    
    def send_bulk_emails(self, messages: list[OutreachMessage]) -> dict:
        """
        Send multiple emails
        
        Args:
            messages: List of outreach messages
            
        Returns:
            Dictionary with success/failure counts
        """
        results = {
            'sent': 0,
            'failed': 0,
            'errors': []
        }
        
        for message in messages:
            if self.send_email(message):
                results['sent'] += 1
            else:
                results['failed'] += 1
                results['errors'].append(f"Failed to send to {message.contact.email}")
        
        logger.info(
            "Bulk email send complete",
            sent=results['sent'],
            failed=results['failed']
        )
        
        return results
    
    def create_activity_log(self, message: OutreachMessage, status: str = "sent") -> CRMActivity:
        """
        Create CRM activity log for sent email
        
        Args:
            message: Outreach message that was sent
            status: Email status (sent, failed, etc.)
            
        Returns:
            CRMActivity object
        """
        return CRMActivity(
            contact_email=message.contact.email or "unknown",
            activity_type="email_sent",
            subject=message.subject,
            description=f"Sent cold email to {message.contact.first_name} {message.contact.last_name}\n\nSubject: {message.subject}\n\nBody:\n{message.body}",
            status=status
        )
