import boto3
import logging
from config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

logger = logging.getLogger(__name__)

class AWSClient:
    """AWS Client for managing AWS resources"""
    
    def __init__(self):
        self.region = AWS_REGION
        self.ec2_client = boto3.client(
            'ec2',
            region_name=self.region,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        self.iam_client = boto3.client(
            'iam',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        self.s3_client = boto3.client(
            's3',
            region_name=self.region,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        self.rds_client = boto3.client(
            'rds',
            region_name=self.region,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        logger.info(f"AWS Client initialized for region: {self.region}")

    def verify_credentials(self):
        """Verify AWS credentials"""
        try:
            sts = boto3.client('sts',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            identity = sts.get_caller_identity()
            logger.info(f"AWS credentials verified. Account: {identity['Account']}")
            return True
        except Exception as e:
            logger.error(f"Failed to verify AWS credentials: {str(e)}")
            return False
