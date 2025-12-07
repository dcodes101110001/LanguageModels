"""
Demo script showing what the SDR agent generates
Run this to see sample outputs without needing API keys
"""

from sdr_agent.core.models import IdealCustomerProfile, Company, Contact, OutreachMessage
from datetime import datetime


def display_sample_workflow():
    """Display a sample workflow with mock data"""
    
    print("=" * 70)
    print("AUTONOMOUS SDR AGENT - SAMPLE WORKFLOW DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Step 1: Define ICP
    print("📋 STEP 1: IDEAL CUSTOMER PROFILE (ICP)")
    print("-" * 70)
    
    icp = IdealCustomerProfile(
        industry="Technology / SaaS",
        company_size_min=100,
        company_size_max=1000,
        job_titles=[
            "Chief Technology Officer",
            "VP of Engineering",
            "Director of Engineering",
            "Head of DevOps"
        ],
        geography="North America",
        technologies=["Cloud", "Kubernetes", "CI/CD", "Microservices"],
        revenue_range="$10M - $100M"
    )
    
    print(f"Target Industry: {icp.industry}")
    print(f"Company Size: {icp.company_size_min} - {icp.company_size_max} employees")
    print(f"Geography: {icp.geography}")
    print(f"Revenue Range: {icp.revenue_range}")
    print(f"Target Roles:")
    for title in icp.job_titles:
        print(f"  • {title}")
    print(f"Technologies: {', '.join(icp.technologies)}")
    print()
    
    # Step 2: Target Company
    print("🏢 STEP 2: TARGET COMPANY RESEARCH")
    print("-" * 70)
    
    company = Company(
        name="CloudScale Systems",
        industry="Technology / SaaS",
        size=450,
        website="https://cloudscale.example.com",
        location="San Francisco, CA",
        description="Enterprise cloud infrastructure automation platform helping DevOps teams scale efficiently",
        recent_news=[
            "Raised $25M Series B led by Accel Partners",
            "Launched new Kubernetes management product",
            "Expanded engineering team by 40% in Q3"
        ],
        trigger_events=[
            "Recent $25M Series B funding round",
            "New product launch - Kubernetes management platform",
            "Rapid engineering team expansion"
        ]
    )
    
    print(f"Company: {company.name}")
    print(f"Industry: {company.industry}")
    print(f"Size: {company.size} employees")
    print(f"Location: {company.location}")
    print(f"Website: {company.website}")
    print(f"\nDescription: {company.description}")
    
    print(f"\n📰 Recent News:")
    for news in company.recent_news:
        print(f"  • {news}")
    
    print(f"\n🎯 Trigger Events (Sales Opportunities):")
    for event in company.trigger_events:
        print(f"  • {event}")
    print()
    
    # Step 3: ICP Fit Analysis
    print("🎯 STEP 3: ICP FIT ANALYSIS")
    print("-" * 70)
    
    fit_score = 85
    print(f"ICP Fit Score: {fit_score}/100 ⭐⭐⭐⭐")
    print()
    print("Reasoning:")
    print(f"  ✓ Perfect industry match (Technology/SaaS)")
    print(f"  ✓ Company size within target range (450 employees)")
    print(f"  ✓ Strong technology alignment (Cloud, Kubernetes)")
    print(f"  ✓ Multiple trigger events indicating growth and investment")
    print(f"  ✓ Geographic match (North America)")
    print()
    print("Recommendation: HIGH PRIORITY PROSPECT - Proceed with outreach")
    print()
    
    # Step 4: Decision Makers
    print("👥 STEP 4: IDENTIFIED DECISION MAKERS")
    print("-" * 70)
    
    contacts = [
        Contact(
            first_name="Sarah",
            last_name="Chen",
            email="sarah.chen@cloudscale.example.com",
            job_title="Chief Technology Officer",
            company=company.name,
            linkedin_url="https://linkedin.com/in/sarahchen"
        ),
        Contact(
            first_name="Michael",
            last_name="Rodriguez",
            email="michael.rodriguez@cloudscale.example.com",
            job_title="VP of Engineering",
            company=company.name,
            linkedin_url="https://linkedin.com/in/michaelrodriguez"
        ),
        Contact(
            first_name="Emily",
            last_name="Taylor",
            email="emily.taylor@cloudscale.example.com",
            job_title="Director of DevOps",
            company=company.name,
            linkedin_url="https://linkedin.com/in/emilytaylor"
        )
    ]
    
    for i, contact in enumerate(contacts, 1):
        print(f"{i}. {contact.first_name} {contact.last_name}")
        print(f"   Title: {contact.job_title}")
        print(f"   Email: {contact.email}")
        print(f"   LinkedIn: {contact.linkedin_url}")
        print()
    
    # Step 5: Generated Messages
    print("✉️  STEP 5: PERSONALIZED OUTREACH MESSAGES")
    print("-" * 70)
    
    # Sample email for CTO
    print("\n📧 EMAIL #1 - To Sarah Chen (CTO)")
    print("-" * 70)
    
    email1 = """Subject: Congrats on the Series B - Scaling CloudScale's Infrastructure

Hi Sarah,

Congratulations on CloudScale's recent $25M Series B! I noticed you're also 
expanding the engineering team by 40% and launching your new Kubernetes 
management platform.

As your team scales, deployment complexity typically grows exponentially. 
I work with CTOs at similar-stage SaaS companies (like Datadog and HashiCorp) 
who've reduced their deployment time by 70% using our AI-powered DevOps 
automation platform.

Given your Kubernetes focus and rapid team growth, I thought you might find 
value in seeing how other engineering leaders are handling similar scaling 
challenges.

Would you be open to a brief 15-minute call next week? I can share specific 
examples from companies at your stage.

Best regards,
AI SDR Agent

P.S. - Loved your recent blog post about microservices orchestration!"""
    
    print(email1)
    print()
    
    # Sample email for VP Engineering
    print("\n📧 EMAIL #2 - To Michael Rodriguez (VP Engineering)")
    print("-" * 70)
    
    email2 = """Subject: Scaling your 40% larger engineering team efficiently

Hi Michael,

I saw CloudScale recently expanded the engineering team by 40% - that's 
impressive growth! As VP of Engineering, you're probably thinking a lot about 
maintaining velocity while onboarding all that new talent.

We help VP Engs at fast-growing SaaS companies reduce onboarding time by 60% 
and improve deployment confidence through AI-powered automation and real-time 
insights.

With your new Kubernetes platform launch and team expansion happening 
simultaneously, maintaining deployment reliability becomes critical.

Quick question: What's your current biggest bottleneck as the team scales?

If reducing deployment friction while scaling is a priority, I'd love to 
share how companies like Vercel and Render handled similar growth phases.

Worth a 15-minute conversation?

Best,
AI SDR Agent"""
    
    print(email2)
    print()
    
    # LinkedIn message
    print("\n💼 LINKEDIN MESSAGE - To Emily Taylor (Director of DevOps)")
    print("-" * 70)
    
    linkedin_msg = """Subject: CloudScale's DevOps automation during rapid growth

Hi Emily,

I've been following CloudScale's growth story - congrats on the Series B and 
new Kubernetes platform! 🎉

As Director of DevOps during a 40% team expansion, you're likely juggling 
scaling infrastructure while maintaining reliability. I work with DevOps 
leaders at similar SaaS companies on automating deployment workflows.

Would love to connect and share insights from companies that navigated similar 
growth phases. No pitch, just sharing what worked for others.

Looking forward to connecting!"""
    
    print(linkedin_msg)
    print()
    
    # Step 6: Next Actions
    print("📊 STEP 6: AUTOMATED CRM LOGGING")
    print("-" * 70)
    
    print("Activities logged to Salesforce/HubSpot:")
    print()
    for i, contact in enumerate(contacts, 1):
        print(f"✓ Created lead: {contact.first_name} {contact.last_name}")
        print(f"  Company: {company.name}")
        print(f"  Title: {contact.job_title}")
        print(f"  Source: AI SDR Agent")
        print(f"  Status: Contacted")
        print(f"  ✓ Logged activity: Cold email sent")
        print(f"  ✓ Added note: ICP fit score 85/100")
        print(f"  ✓ Added note: Trigger events - Series B, team expansion, product launch")
        print()
    
    # Summary
    print("=" * 70)
    print("📈 CAMPAIGN SUMMARY")
    print("=" * 70)
    print()
    print(f"Company Analyzed: 1")
    print(f"ICP Fit Score: {fit_score}/100")
    print(f"Decision Makers Identified: {len(contacts)}")
    print(f"Personalized Emails Generated: {len(contacts)}")
    print(f"LinkedIn Messages Generated: 1")
    print(f"CRM Leads Created: {len(contacts)}")
    print(f"CRM Activities Logged: {len(contacts)}")
    print()
    print("✅ All activities completed autonomously by the SDR Agent!")
    print()
    print("=" * 70)
    print()
    print("💡 NEXT STEPS:")
    print("  1. Review and approve generated messages")
    print("  2. Send emails (set send_email=True)")
    print("  3. Track responses in CRM")
    print("  4. Agent handles follow-ups automatically")
    print()


if __name__ == "__main__":
    display_sample_workflow()
