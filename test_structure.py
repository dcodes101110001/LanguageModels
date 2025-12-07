"""
Test script to validate SDR Agent structure and components
This script tests the agent without requiring actual API keys
"""

import sys
from sdr_agent.core.models import IdealCustomerProfile, Company, Contact, OutreachMessage
from sdr_agent.config import config


def test_models():
    """Test data models"""
    print("Testing Data Models...")
    
    # Test ICP
    icp = IdealCustomerProfile(
        industry="Technology",
        company_size_min=50,
        company_size_max=1000,
        job_titles=["CTO", "VP Engineering"],
        geography="United States"
    )
    assert icp.industry == "Technology"
    print("  ✓ IdealCustomerProfile model working")
    
    # Test Company
    company = Company(
        name="Test Corp",
        industry="Technology",
        size=500,
        website="https://test.com",
        description="A test company"
    )
    assert company.name == "Test Corp"
    print("  ✓ Company model working")
    
    # Test Contact
    contact = Contact(
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        job_title="CTO",
        company="Test Corp"
    )
    assert contact.first_name == "John"
    print("  ✓ Contact model working")
    
    # Test OutreachMessage
    message = OutreachMessage(
        contact=contact,
        subject="Test Subject",
        body="Test Body",
        channel="email"
    )
    assert message.subject == "Test Subject"
    print("  ✓ OutreachMessage model working")
    
    print("✓ All data models validated successfully!\n")
    return True


def test_config():
    """Test configuration"""
    print("Testing Configuration...")
    
    # Test config loading
    assert config.agent.agent_name is not None
    print(f"  ✓ Agent name: {config.agent.agent_name}")
    
    # Test validation
    missing = config.validate_required()
    print(f"  ℹ Missing config fields: {missing if missing else 'None (all set)'}")
    
    print("✓ Configuration validated!\n")
    return True


def test_integrations():
    """Test integration initialization"""
    print("Testing Integrations...")
    
    from sdr_agent.integrations.salesforce import SalesforceIntegration
    from sdr_agent.integrations.hubspot import HubSpotIntegration
    from sdr_agent.integrations.email import EmailIntegration
    
    # Test Salesforce
    sf = SalesforceIntegration()
    result = sf.connect()
    print(f"  ✓ Salesforce integration initialized (connected: {result})")
    
    # Test HubSpot
    hs = HubSpotIntegration()
    result = hs.connect()
    print(f"  ✓ HubSpot integration initialized (connected: {result})")
    
    # Test Email
    email = EmailIntegration()
    result = email.connect()
    print(f"  ✓ Email integration initialized (connected: {result})")
    
    print("✓ All integrations validated!\n")
    return True


def test_agent_structure():
    """Test agent structure"""
    print("Testing Agent Structure...")
    
    from sdr_agent.agent import SDRAgent
    
    try:
        agent = SDRAgent(crm_type="salesforce")
        print("  ✓ SDR Agent initialized with Salesforce")
        
        agent2 = SDRAgent(crm_type="hubspot")
        print("  ✓ SDR Agent initialized with HubSpot")
        
        print("✓ Agent structure validated!\n")
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_workflow_structure():
    """Test workflow structure without API calls"""
    print("Testing Workflow Structure...")
    
    # Create test data
    icp = IdealCustomerProfile(
        industry="Technology",
        company_size_min=50,
        company_size_max=1000,
        job_titles=["CTO", "VP Engineering"]
    )
    
    company = Company(
        name="Test Corp",
        industry="Technology",
        size=500
    )
    
    contact = Contact(
        first_name="Jane",
        last_name="Smith",
        email="jane@testcorp.com",
        job_title="CTO",
        company="Test Corp"
    )
    
    print(f"  ✓ Created ICP for {icp.industry} industry")
    print(f"  ✓ Created company: {company.name}")
    print(f"  ✓ Created contact: {contact.first_name} {contact.last_name}")
    
    # Test workflow components exist
    from sdr_agent.core.icp_identifier import ICPIdentifier
    from sdr_agent.core.researcher import CompanyResearcher
    from sdr_agent.core.message_generator import MessageGenerator
    
    print("  ✓ ICP Identifier module loaded")
    print("  ✓ Company Researcher module loaded")
    print("  ✓ Message Generator module loaded")
    
    print("✓ Workflow structure validated!\n")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("SDR Agent Validation Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Data Models", test_models),
        ("Configuration", test_config),
        ("Integrations", test_integrations),
        ("Agent Structure", test_agent_structure),
        ("Workflow Structure", test_workflow_structure),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} failed with error: {e}\n")
            results.append((name, False))
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
