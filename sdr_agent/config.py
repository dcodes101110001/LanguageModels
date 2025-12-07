"""Configuration management for SDR Agent"""
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OpenAIConfig(BaseModel):
    """OpenAI API configuration"""
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = Field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4"))


class SalesforceConfig(BaseModel):
    """Salesforce CRM configuration"""
    username: str = Field(default_factory=lambda: os.getenv("SALESFORCE_USERNAME", ""))
    password: str = Field(default_factory=lambda: os.getenv("SALESFORCE_PASSWORD", ""))
    security_token: str = Field(default_factory=lambda: os.getenv("SALESFORCE_SECURITY_TOKEN", ""))


class HubSpotConfig(BaseModel):
    """HubSpot CRM configuration"""
    api_key: str = Field(default_factory=lambda: os.getenv("HUBSPOT_API_KEY", ""))


class EmailConfig(BaseModel):
    """Email configuration"""
    sendgrid_api_key: str = Field(default_factory=lambda: os.getenv("SENDGRID_API_KEY", ""))
    from_email: str = Field(default_factory=lambda: os.getenv("SENDGRID_FROM_EMAIL", ""))


class LinkedInConfig(BaseModel):
    """LinkedIn configuration"""
    api_key: str = Field(default_factory=lambda: os.getenv("LINKEDIN_API_KEY", ""))


class AgentConfig(BaseModel):
    """Agent configuration"""
    agent_name: str = Field(default_factory=lambda: os.getenv("SDR_AGENT_NAME", "AI SDR Agent"))
    company_name: str = Field(default_factory=lambda: os.getenv("SDR_AGENT_COMPANY", "Your Company"))


class Config(BaseModel):
    """Main configuration class"""
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    salesforce: SalesforceConfig = Field(default_factory=SalesforceConfig)
    hubspot: HubSpotConfig = Field(default_factory=HubSpotConfig)
    email: EmailConfig = Field(default_factory=EmailConfig)
    linkedin: LinkedInConfig = Field(default_factory=LinkedInConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    
    def validate_required(self) -> list[str]:
        """Validate required configuration fields"""
        missing = []
        if not self.openai.api_key:
            missing.append("OPENAI_API_KEY")
        return missing


# Global config instance
config = Config()
