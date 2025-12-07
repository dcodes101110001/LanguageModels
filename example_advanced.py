"""
Advanced example: Custom SDR workflow with follow-ups

This example shows how to:
1. Use the SDR agent with custom workflows
2. Generate follow-up messages
3. Handle different message channels (email, LinkedIn)
"""

from sdr_agent.agent import SDRAgent
from sdr_agent.core.models import IdealCustomerProfile, Company, Contact
from sdr_agent.core.message_generator import MessageGenerator


def custom_workflow_example():
    """Example of custom SDR workflow"""
    
    print("Custom SDR Workflow Example")
    print("=" * 60)
    print()
    
    # Initialize components
    agent = SDRAgent(crm_type="hubspot")
    message_gen = MessageGenerator()
    
    # Define ICP for fintech companies
    icp = IdealCustomerProfile(
        industry="Financial Services",
        company_size_min=100,
        company_size_max=5000,
        job_titles=["Chief Financial Officer", "VP of Finance", "Finance Director"],
        geography="North America",
        technologies=["Blockchain", "API", "Cloud"],
        revenue_range="$50M - $500M"
    )
    
    value_proposition = """
Our AI-powered financial forecasting platform helps CFOs make data-driven decisions
with 95% accuracy, reducing forecasting time by 60% and improving cash flow management.
    """.strip()
    
    # Example: Process a single high-value prospect with custom workflow
    print("Processing high-value prospect with custom workflow...")
    print()
    
    prospect_name = "FinTech Innovations Inc"
    prospect_website = "https://fintechinnovations.example.com"
    
    # Process the prospect
    result = agent.process_prospect(
        company_name=prospect_name,
        icp=icp,
        value_proposition=value_proposition,
        company_website=prospect_website,
        send_email=False
    )
    
    print(f"Prospect: {prospect_name}")
    print(f"ICP Fit Score: {result.get('icp_fit_score')}/100")
    print(f"Trigger Events Found: {len(result.get('trigger_events', []))}")
    print()
    
    # Example: Generate LinkedIn message for the same contacts
    if result.get('contacts_identified', 0) > 0:
        print("Generating LinkedIn messages for multi-channel outreach...")
        print()
        
        # Create sample contact (in real usage, you'd get this from the results)
        sample_contact = Contact(
            first_name="Sarah",
            last_name="Johnson",
            job_title="Chief Financial Officer",
            company=prospect_name,
            email="sarah.johnson@fintechinnovations.example.com",
            linkedin_url="https://linkedin.com/in/sarahjohnson"
        )
        
        # Create sample company
        sample_company = Company(
            name=prospect_name,
            industry="Financial Services",
            website=prospect_website,
            description="Leading fintech company providing innovative financial solutions"
        )
        
        # Generate LinkedIn message
        linkedin_msg = message_gen.generate_linkedin_message(
            contact=sample_contact,
            company=sample_company,
            value_proposition=value_proposition
        )
        
        print(f"LinkedIn Message for {sample_contact.first_name} {sample_contact.last_name}:")
        print(f"Subject: {linkedin_msg.subject}")
        print(f"Message:\n{linkedin_msg.body}")
        print()
        
        # Example: Generate follow-up email
        print("Generating follow-up message (for use after 3 days with no response)...")
        print()
        
        previous_email = """
Hi Sarah,

I noticed FinTech Innovations recently expanded into blockchain solutions. 
As CFO, you're likely looking for ways to improve financial forecasting accuracy 
in this rapidly evolving landscape.

Our AI platform helps CFOs like you achieve 95% forecasting accuracy while 
reducing the time spent on projections by 60%.

Would you be open to a brief 15-minute call next week to explore if this could 
benefit FinTech Innovations?

Best regards,
AI SDR Agent
        """.strip()
        
        follow_up = message_gen.generate_follow_up(
            contact=sample_contact,
            previous_message=previous_email,
            days_since_last_contact=3
        )
        
        print(f"Follow-up Email:")
        print(f"Subject: {follow_up.subject}")
        print(f"Body:\n{follow_up.body}")
        print()
    
    print("=" * 60)
    print("Custom workflow complete!")
    print()


def multi_channel_campaign():
    """Example of multi-channel outreach campaign"""
    
    print("Multi-Channel Campaign Example")
    print("=" * 60)
    print()
    
    print("This example demonstrates:")
    print("1. Email outreach to primary contacts")
    print("2. LinkedIn outreach to secondary contacts")
    print("3. Follow-up sequencing across channels")
    print()
    
    # In a real implementation, you would:
    # - Send initial email to primary decision maker
    # - Connect on LinkedIn with other stakeholders
    # - Follow up via email after 3-5 days
    # - Follow up on LinkedIn after 7 days
    # - Multi-thread within the account
    
    print("Multi-channel sequencing strategy:")
    print("  Day 0: Email to CFO")
    print("  Day 1: LinkedIn connection to VP Finance")
    print("  Day 3: Email follow-up to CFO")
    print("  Day 7: LinkedIn message to VP Finance")
    print("  Day 10: Final email to both contacts")
    print()
    
    print("=" * 60)


if __name__ == "__main__":
    custom_workflow_example()
    print("\n")
    multi_channel_campaign()
