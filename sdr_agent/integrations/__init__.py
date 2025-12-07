"""Integration modules for CRM and communication platforms"""
from .salesforce import SalesforceIntegration
from .hubspot import HubSpotIntegration
from .email import EmailIntegration

__all__ = [
    'SalesforceIntegration',
    'HubSpotIntegration',
    'EmailIntegration',
]
