import logging
from aws_client import AWSClient

logger = logging.getLogger(__name__)

class S3Manager:
    """Manage S3 buckets"""
    
    def __init__(self):
        self.aws = AWSClient()
        self.s3 = self.aws.s3_client
    
    def list_buckets(self):
        """List all S3 buckets"""
        try:
            response = self.s3.list_buckets()
            buckets = []
            for bucket in response['Buckets']:
                buckets.append({
                    'Name': bucket['Name'],
                    'CreationDate': str(bucket['CreationDate'])
                })
            logger.info(f"Retrieved {len(buckets)} S3 buckets")
            return buckets
        except Exception as e:
            logger.error(f"Error listing buckets: {str(e)}")
            return None
    
    def create_bucket(self, bucket_name, region=None):
        """Create a new S3 bucket"""
        try:
            if region and region != 'us-east-1':
                self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            else:
                self.s3.create_bucket(Bucket=bucket_name)
            logger.info(f"Bucket created: {bucket_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating bucket: {str(e)}")
            return False
    
    def delete_bucket(self, bucket_name):
        """Delete an S3 bucket"""
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
            logger.info(f"Bucket deleted: {bucket_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting bucket: {str(e)}")
            return False
    
    def upload_file(self, bucket_name, file_path, object_name=None):
        """Upload a file to S3 bucket"""
        try:
            if object_name is None:
                object_name = file_path.split('/')[-1]
            
            self.s3.upload_file(file_path, bucket_name, object_name)
            logger.info(f"File uploaded to {bucket_name}/{object_name}")
            return True
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            return False
    
    def list_objects(self, bucket_name):
        """List objects in S3 bucket"""
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            objects = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    objects.append({
                        'Key': obj['Key'],
                        'Size': obj['Size'],
                        'LastModified': str(obj['LastModified'])
                    })
            logger.info(f"Retrieved {len(objects)} objects from {bucket_name}")
            return objects
        except Exception as e:
            logger.error(f"Error listing objects: {str(e)}")
            return None
    
    def enable_versioning(self, bucket_name):
        """Enable versioning on S3 bucket"""
        try:
            self.s3.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={'Status': 'Enabled'}
            )
            logger.info(f"Versioning enabled for {bucket_name}")
            return True
        except Exception as e:
            logger.error(f"Error enabling versioning: {str(e)}")
            return False
