# Autonomous Sales Development Representative (SDR) Agent

An AI-powered sales development agent that autonomously handles the entire top-of-funnel sales process, from identifying ideal customer profiles to generating personalized outreach and logging activities in your CRM.

## 🚀 Features

- **Ideal Customer Profile (ICP) Identification**: Automatically analyze companies against your ICP criteria
- **Company Research**: Gather company information, news, and trigger events
- **Trigger Event Detection**: Identify sales opportunities from company developments
- **Personalized Message Generation**: Create context-aware cold emails and LinkedIn messages using LLM
- **Multi-Channel Outreach**: Support for email and LinkedIn campaigns
- **CRM Integration**: Automatic logging to Salesforce or HubSpot
- **Email Automation**: Send emails via SendGrid
- **Follow-up Sequences**: Generate intelligent follow-up messages

## 📋 Requirements

- Python 3.8+
- OpenAI API key (for GPT-4)
- Optional: Salesforce or HubSpot credentials
- Optional: SendGrid API key for sending emails
- Optional: LinkedIn Sales Navigator API (future integration)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/dcodes101110001/LanguageModels.git
cd LanguageModels
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## 🔧 Configuration

Create a `.env` file with your credentials:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Optional: Salesforce
SALESFORCE_USERNAME=your_salesforce_username
SALESFORCE_PASSWORD=your_salesforce_password
SALESFORCE_SECURITY_TOKEN=your_salesforce_security_token

# Optional: HubSpot
HUBSPOT_API_KEY=your_hubspot_api_key

# Optional: SendGrid
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=your_email@example.com

# Agent Settings
SDR_AGENT_NAME=AI SDR Agent
SDR_AGENT_COMPANY=Your Company Name
```

## 📖 Quick Start

### Basic Usage

```python
from sdr_agent.agent import SDRAgent
from sdr_agent.core.models import IdealCustomerProfile

# Define your Ideal Customer Profile
icp = IdealCustomerProfile(
    industry="Technology",
    company_size_min=50,
    company_size_max=1000,
    job_titles=["CTO", "VP Engineering", "Director of Engineering"],
    geography="United States",
    technologies=["Cloud", "SaaS", "API"]
)

# Define your value proposition
value_proposition = """
We help engineering teams reduce deployment time by 70% through our 
AI-powered DevOps automation platform.
"""

# Initialize the agent
agent = SDRAgent(crm_type="salesforce")  # or "hubspot"

# Process a single prospect
result = agent.process_prospect(
    company_name="TechCorp Solutions",
    icp=icp,
    value_proposition=value_proposition,
    send_email=False  # Set to True to send actual emails
)

print(f"ICP Fit Score: {result['icp_fit_score']}/100")
print(f"Contacts Identified: {result['contacts_identified']}")
print(f"Messages Generated: {result['messages_generated']}")
```

### Process Multiple Prospects

```python
# Define prospect list
prospects = [
    {"name": "TechCorp Solutions", "website": "https://techcorp.example.com"},
    {"name": "CloudScale Systems", "website": "https://cloudscale.example.com"},
    {"name": "DataFlow Analytics", "website": "https://dataflow.example.com"}
]

# Process all prospects
results = agent.process_prospect_list(
    prospects=prospects,
    icp=icp,
    value_proposition=value_proposition,
    send_email=False
)

# Generate campaign report
report = agent.generate_campaign_report(results)
print(report)
```

## 📚 Examples

Run the included examples:

### Basic Example
```bash
python example.py
```

This demonstrates:
- ICP definition
- Prospect processing
- Message generation
- CRM logging (simulated)

### Advanced Example
```bash
python example_advanced.py
```

This shows:
- Custom workflows
- Multi-channel outreach (email + LinkedIn)
- Follow-up message generation

## 🏗️ Architecture

```
sdr_agent/
├── agent.py                 # Main SDR Agent orchestrator
├── config.py                # Configuration management
├── core/
│   ├── models.py           # Data models (ICP, Contact, Company, etc.)
│   ├── icp_identifier.py   # ICP analysis and contact identification
│   ├── researcher.py       # Company research and trigger events
│   └── message_generator.py # Personalized message generation
├── integrations/
│   ├── salesforce.py       # Salesforce CRM integration
│   ├── hubspot.py          # HubSpot CRM integration
│   └── email.py            # Email sending (SendGrid)
└── utils/
    └── logger.py           # Structured logging
```

## 🔄 Workflow

The SDR Agent follows this workflow for each prospect:

1. **Research Company**: Gather company information from available sources
2. **Analyze ICP Fit**: Score the company against your ICP criteria (0-100)
3. **Identify Trigger Events**: Find recent company news and developments
4. **Gather Company News**: Research recent press and announcements
5. **Identify Decision Makers**: Find relevant contacts based on job titles
6. **Generate Messages**: Create personalized outreach for each contact
7. **Send Emails**: Deliver messages via configured channels (optional)
8. **Log to CRM**: Record all activities in Salesforce/HubSpot

## 🎯 Use Cases

- **Outbound Sales Teams**: Automate top-of-funnel prospecting
- **Growth Marketing**: Scale personalized outreach campaigns
- **Business Development**: Identify and engage high-fit prospects
- **Account-Based Marketing**: Research and engage target accounts
- **Lead Generation**: Build and nurture prospect pipelines

## 🔐 Security & Privacy

- All API keys are stored in environment variables (`.env`)
- CRM credentials are encrypted in transit
- Email content is generated per-prospect (no bulk templates)
- Activity logging ensures full audit trail

## 🚧 Future Enhancements

- [ ] LinkedIn Sales Navigator API integration
- [ ] Additional CRM support (Pipedrive, Close, etc.)
- [ ] Advanced trigger event detection with news APIs
- [ ] A/B testing for message variants
- [ ] Response tracking and sentiment analysis
- [ ] Automated follow-up sequences
- [ ] Meeting scheduling integration (Calendly, etc.)
- [ ] Performance analytics dashboard

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## ⚠️ Disclaimer

This tool is designed for legitimate B2B sales outreach. Please ensure compliance with:
- CAN-SPAM Act (US)
- GDPR (EU)
- CASL (Canada)
- Your organization's sales and privacy policies

Always obtain proper consent before sending marketing communications.
