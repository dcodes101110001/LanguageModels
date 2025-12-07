# Setup and Usage Guide

This guide will help you set up and use the Autonomous SDR Agent.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/dcodes101110001/LanguageModels.git
cd LanguageModels
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Copy the example environment file and edit it with your API keys:

```bash
cp .env.example .env
```

Edit `.env` file with your credentials:

```env
# Required for core functionality
OPENAI_API_KEY=sk-...your_actual_key...
OPENAI_MODEL=gpt-4

# Optional: Salesforce (choose one CRM)
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password
SALESFORCE_SECURITY_TOKEN=your_token

# Optional: HubSpot (alternative to Salesforce)
HUBSPOT_API_KEY=your_hubspot_key

# Optional: SendGrid (for sending emails)
SENDGRID_API_KEY=SG.your_key
SENDGRID_FROM_EMAIL=your_email@company.com

# Agent Settings
SDR_AGENT_NAME=Your Sales Agent
SDR_AGENT_COMPANY=Your Company
```

## Getting Your API Keys

### OpenAI API Key (Required)

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

**Cost Estimate**: ~$0.01-0.05 per prospect (depending on GPT-4 usage)

### Salesforce (Optional)

1. Log in to Salesforce
2. Go to Setup → Reset Security Token
3. Your security token will be emailed to you
4. Add credentials to `.env`:
   - Username: Your Salesforce login email
   - Password: Your Salesforce password
   - Security Token: The token from email

### HubSpot (Optional)

1. Log in to HubSpot
2. Go to Settings → Integrations → API Key
3. Create or view your API key
4. Copy to `.env` file

### SendGrid (Optional)

1. Sign up at https://sendgrid.com/
2. Go to Settings → API Keys
3. Create a new API key with "Mail Send" permission
4. Copy to `.env` file
5. Verify your sender email address in SendGrid

## Testing the Installation

Run the validation test:

```bash
python test_structure.py
```

You should see:
```
✓ All tests passed!
```

## Running Examples

### Basic Example (Demo Mode - No Emails Sent)

```bash
python example.py
```

This will:
- Initialize the agent
- Process 3 sample prospects
- Generate personalized messages
- Show what would be sent (demo mode)
- Simulate CRM logging

### Advanced Example

```bash
python example_advanced.py
```

This demonstrates:
- Custom workflows
- LinkedIn message generation
- Follow-up sequences

## Using the Agent in Your Code

### Minimal Example

```python
from sdr_agent.agent import SDRAgent
from sdr_agent.core.models import IdealCustomerProfile

# Define your ICP
icp = IdealCustomerProfile(
    industry="Technology",
    company_size_min=50,
    company_size_max=1000,
    job_titles=["CTO", "VP Engineering"],
    geography="United States"
)

# Your value proposition
value_prop = "We help companies reduce costs by 40% with our solution."

# Initialize agent
agent = SDRAgent(crm_type="salesforce")  # or "hubspot"

# Process a prospect
result = agent.process_prospect(
    company_name="Target Company Inc",
    icp=icp,
    value_proposition=value_prop,
    send_email=False  # True to send actual emails
)

# View results
print(f"ICP Fit: {result['icp_fit_score']}/100")
print(f"Messages Generated: {result['messages_generated']}")
```

### Processing Multiple Prospects

```python
prospects = [
    {"name": "Company A", "website": "https://companya.com"},
    {"name": "Company B", "website": "https://companyb.com"},
    {"name": "Company C", "website": "https://companyc.com"},
]

results = agent.process_prospect_list(
    prospects=prospects,
    icp=icp,
    value_proposition=value_prop,
    send_email=False
)

# Generate report
report = agent.generate_campaign_report(results)
print(report)
```

## Best Practices

### 1. Start in Demo Mode

Always test with `send_email=False` first to review generated messages.

### 2. Refine Your ICP

Start with a narrow ICP and expand based on results:
- Review fit scores
- Analyze which industries/sizes work best
- Adjust criteria iteratively

### 3. Test Your Value Proposition

Try different value propositions and compare:
- Message quality
- Response rates
- Conversion metrics

### 4. Monitor API Costs

- OpenAI charges per token (input + output)
- Each prospect costs approximately $0.01-0.05
- Process in batches to control costs

### 5. Gradual Rollout

1. Start with 5-10 prospects
2. Review generated messages manually
3. Gradually increase volume as you gain confidence

## Troubleshooting

### "Missing configuration" warning

**Cause**: API keys not set in `.env` file  
**Solution**: Add required API keys (at minimum, OPENAI_API_KEY)

### "Connection error" messages

**Cause**: No OpenAI API key configured  
**Solution**: Add valid OPENAI_API_KEY to `.env` file

### Agent runs but messages are generic

**Cause**: Insufficient context in value proposition  
**Solution**: Provide more detailed value prop with:
- Specific benefits
- Metrics/numbers
- Target use cases

### CRM integration not working

**Cause**: Invalid CRM credentials  
**Solution**: 
- For Salesforce: Verify username, password, and security token
- For HubSpot: Verify API key has correct permissions
- Check credentials by logging into CRM directly

### Emails not sending

**Cause**: SendGrid not configured or invalid API key  
**Solution**:
- Verify SENDGRID_API_KEY in `.env`
- Verify sender email is verified in SendGrid
- Check SendGrid dashboard for errors

## Performance Tips

### 1. Batch Processing

Process prospects in batches of 10-20 for better error handling:

```python
import time

for batch in prospect_batches:
    results = agent.process_prospect_list(batch, icp, value_prop)
    time.sleep(5)  # Rate limiting
```

### 2. Error Handling

```python
try:
    result = agent.process_prospect(...)
    if result.get('errors'):
        print(f"Errors: {result['errors']}")
except Exception as e:
    print(f"Failed to process: {e}")
```

### 3. Logging

Enable detailed logging for debugging:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Advanced Configuration

### Custom Message Templates

Extend the MessageGenerator class for custom templates:

```python
from sdr_agent.core.message_generator import MessageGenerator

class CustomMessageGenerator(MessageGenerator):
    def generate_cold_email(self, contact, company, value_prop, **kwargs):
        # Add custom logic here
        return super().generate_cold_email(contact, company, value_prop, **kwargs)
```

### Custom Research Sources

Extend the CompanyResearcher class:

```python
from sdr_agent.core.researcher import CompanyResearcher

class EnhancedResearcher(CompanyResearcher):
    def research_company(self, company_name, website=None):
        # Add custom data sources
        # e.g., scrape LinkedIn, Crunchbase, etc.
        return super().research_company(company_name, website)
```

## Support

For issues or questions:
1. Check this guide first
2. Review example scripts
3. Check GitHub issues
4. Open a new issue with:
   - Error messages
   - Configuration (without API keys!)
   - Steps to reproduce

## Next Steps

1. ✅ Install and configure
2. ✅ Run validation tests
3. ✅ Try demo examples
4. ✅ Test with real API keys (demo mode)
5. ✅ Review generated messages
6. ✅ Send first test email
7. ✅ Scale up gradually

Happy prospecting! 🚀
