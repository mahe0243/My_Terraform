# ebot - AWS Resource Manager

A Python-based bot application for managing AWS resources through an interactive CLI interface.

## Features

### EC2 Instance Management
- List all EC2 instances
- Launch new instances
- Start/Stop instances
- Terminate instances

### IAM Role Management
- List all IAM roles
- Create new roles with assume role policies
- Delete roles
- Attach policies to roles
- Create IAM users

### S3 Bucket Management
- List all S3 buckets
- Create new buckets
- Delete buckets
- List objects in buckets
- Upload files to buckets
- Enable versioning on buckets

## Prerequisites

- Python 3.7+
- AWS Account with appropriate permissions
- AWS CLI configured or AWS credentials available

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mahe0243/My_Terraform.git
cd My_Terraform
git checkout ebot-application
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure AWS credentials:
```bash
cp .env.example .env
# Edit .env with your AWS credentials
```

## Configuration

Create a `.env` file with the following variables:

```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
TERRAFORM_DIR=./terraform
LOG_LEVEL=INFO
LOG_FILE=./logs/ebot.log
```

## Usage

1. Navigate to the ebot_app directory:
```bash
cd ebot_app
```

2. Run the bot:
```bash
python bot.py
```

3. Follow the interactive menu to manage AWS resources

## Project Structure

```
ebot_app/
├── config.py           # Configuration management
├── aws_client.py       # AWS client initialization
├── ec2_manager.py      # EC2 operations
├── iam_manager.py      # IAM operations
├── s3_manager.py       # S3 operations
├── bot.py              # Main bot application
├── requirements.txt    # Python dependencies
└── .env.example        # Environment configuration template
```

## Security Considerations

- Never commit `.env` file with real credentials
- Use AWS IAM roles when running on AWS services
- Limit IAM permissions to only required actions
- Rotate access keys regularly
- Use MFA for AWS account access

## Logging

All operations are logged to both console and file:
- Log file location: `./logs/ebot.log`
- Log level can be configured via `.env` file

## Error Handling

The bot includes comprehensive error handling for:
- AWS API failures
- Invalid user input
- Missing credentials
- Network timeouts

## Future Enhancements

- [ ] Integrate with Terraform for infrastructure as code
- [ ] Add RDS database management
- [ ] Implement batch operations
- [ ] Add resource tagging capabilities
- [ ] Create monitoring and alerting features
- [ ] Add webhook support for automated deployments
- [ ] Implement cost optimization recommendations
- [ ] Add multi-account support

## Contributing

Contributions are welcome! Please follow these steps:
1. Create a new branch for your feature
2. Commit your changes
3. Push to the branch
4. Create a Pull Request

## License

MIT License

## Support

For issues and questions, please create an issue in the GitHub repository.
