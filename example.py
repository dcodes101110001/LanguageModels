"""
Example usage of the Autonomous SDR Agent

This script demonstrates how to use the SDR Agent to:
1. Define an Ideal Customer Profile (ICP)
2. Process prospects
3. Generate personalized outreach messages
4. Log activities in CRM
"""

from sdr_agent.agent import SDRAgent
from sdr_agent.core.models import IdealCustomerProfile


def main():
    """Main example function"""
    
    print("=" * 60)
    print("Autonomous SDR Agent - Example Usage")
    print("=" * 60)
    print()
    
    # Step 1: Define your Ideal Customer Profile
    print("Step 1: Defining Ideal Customer Profile (ICP)...")
    icp = IdealCustomerProfile(
        industry="Technology",
        company_size_min=50,
        company_size_max=1000,
        job_titles=[
            "Chief Technology Officer",
            "VP of Engineering",
            "Director of Engineering",
            "Head of Product"
        ],
        geography="United States",
        technologies=["Cloud", "SaaS", "API"],
        revenue_range="$10M - $100M"
    )
    print(f"  ✓ ICP defined for {icp.industry} industry")
    print(f"  ✓ Target roles: {', '.join(icp.job_titles[:2])}...")
    print()
    
    # Step 2: Define your value proposition
    print("Step 2: Setting value proposition...")
    value_proposition = """
We help engineering teams reduce deployment time by 70% through our AI-powered 
DevOps automation platform. Our solution integrates seamlessly with your existing 
CI/CD pipeline and provides real-time insights into bottlenecks and optimization 
opportunities.
    """.strip()
    print(f"  ✓ Value proposition defined")
    print()
    
    # Step 3: Define prospect list
    print("Step 3: Creating prospect list...")
    prospects = [
        {
            "name": "TechCorp Solutions",
            "website": "https://techcorp.example.com"
        },
        {
            "name": "CloudScale Systems",
            "website": "https://cloudscale.example.com"
        },
        {
            "name": "DataFlow Analytics",
            "website": "https://dataflow.example.com"
        }
    ]
    print(f"  ✓ {len(prospects)} prospects added to list")
    print()
    
    # Step 4: Initialize SDR Agent
    print("Step 4: Initializing SDR Agent...")
    print("  Note: Running in DEMO mode (no actual emails will be sent)")
    print("  Note: CRM operations will be simulated")
    print()
    
    # You can choose "salesforce" or "hubspot"
    agent = SDRAgent(crm_type="salesforce")
    print("  ✓ SDR Agent initialized with Salesforce CRM")
    print()
    
    # Step 5: Process prospects
    print("Step 5: Processing prospects...")
    print("-" * 60)
    
    results = agent.process_prospect_list(
        prospects=prospects,
        icp=icp,
        value_proposition=value_proposition,
        send_email=False  # Set to True to actually send emails
    )
    
    print()
    print("-" * 60)
    print()
    
    # Step 6: Display results
    print("Step 6: Results Summary")
    print("=" * 60)
    
    for result in results:
        company = result.get('company', 'Unknown')
        print(f"\nCompany: {company}")
        print(f"  ICP Fit Score: {result.get('icp_fit_score', 'N/A')}/100")
        print(f"  Contacts Identified: {result.get('contacts_identified', 0)}")
        print(f"  Messages Generated: {result.get('messages_generated', 0)}")
        print(f"  Steps Completed: {', '.join(result.get('steps_completed', []))}")
        
        if result.get('skipped'):
            print(f"  Status: ⚠️  SKIPPED - {result.get('skip_reason')}")
        else:
            print(f"  Status: ✓ PROCESSED")
        
        # Display generated messages
        if 'messages' in result:
            print(f"\n  Generated Messages:")
            for i, msg in enumerate(result['messages'], 1):
                print(f"\n  Message {i} to {msg['to']}:")
                print(f"    Subject: {msg['subject']}")
                print(f"    Body Preview: {msg['body'][:100]}...")
        
        if result.get('errors'):
            print(f"\n  Errors: {', '.join(result['errors'])}")
    
    # Step 7: Generate campaign report
    print("\n" + "=" * 60)
    print("Campaign Report")
    print("=" * 60)
    report = agent.generate_campaign_report(results)
    print(report)
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Configure your API keys in .env file")
    print("2. Set send_email=True to send actual emails")
    print("3. Integrate with your actual prospect data source")
    print("4. Set up automated scheduling for regular campaigns")
    print()


if __name__ == "__main__":
    main()
