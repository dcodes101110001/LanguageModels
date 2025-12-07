"""Data models for SDR Agent"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class IdealCustomerProfile(BaseModel):
    """Ideal Customer Profile definition"""
    industry: str
    company_size_min: Optional[int] = None
    company_size_max: Optional[int] = None
    job_titles: List[str] = Field(default_factory=list)
    geography: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    revenue_range: Optional[str] = None


class Company(BaseModel):
    """Company information"""
    name: str
    industry: Optional[str] = None
    size: Optional[int] = None
    website: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    recent_news: List[str] = Field(default_factory=list)
    trigger_events: List[str] = Field(default_factory=list)


class Contact(BaseModel):
    """Contact information"""
    first_name: str
    last_name: str
    email: Optional[str] = None
    job_title: Optional[str] = None
    company: str
    linkedin_url: Optional[str] = None
    phone: Optional[str] = None


class OutreachMessage(BaseModel):
    """Outreach message"""
    contact: Contact
    subject: str
    body: str
    channel: str = "email"  # email, linkedin, etc.
    generated_at: datetime = Field(default_factory=datetime.now)


class CRMActivity(BaseModel):
    """CRM activity log"""
    contact_email: str
    activity_type: str  # email_sent, linkedin_message, call, etc.
    subject: str
    description: str
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "completed"
