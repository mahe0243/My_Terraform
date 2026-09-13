import os
from dotenv import load_dotenv

load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Bot Configuration
BOT_NAME = 'ebot'
BOT_VERSION = '1.0.0'

# Terraform Configuration
TERRAFORM_DIR = os.getenv('TERRAFORM_DIR', './terraform')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', './logs/ebot.log')

# Features
ENABLE_EC2 = True
ENABLE_IAM = True
ENABLE_S3 = True
ENABLE_RDS = True
