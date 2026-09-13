import logging
import sys
from datetime import datetime
from config import LOG_LEVEL, LOG_FILE, BOT_NAME, BOT_VERSION
from ec2_manager import EC2Manager
from iam_manager import IAMManager
from s3_manager import S3Manager
from aws_client import AWSClient

# Setup logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EBot:
    """Main ebot application class"""
    
    def __init__(self):
        logger.info(f"Initializing {BOT_NAME} v{BOT_VERSION}")
        self.aws = AWSClient()
        self.ec2 = EC2Manager()
        self.iam = IAMManager()
        self.s3 = S3Manager()
    
    def start(self):
        """Start the bot"""
        logger.info(f"{BOT_NAME} started at {datetime.now()}")
        print(f"\n{'='*50}")
        print(f"{BOT_NAME} v{BOT_VERSION} - AWS Resource Manager")
        print(f"{'='*50}\n")
        
        if not self.aws.verify_credentials():
            logger.error("Failed to verify AWS credentials")
            print("ERROR: Failed to verify AWS credentials. Please check your configuration.")
            sys.exit(1)
        
        self.show_menu()
    
    def show_menu(self):
        """Display main menu"""
        while True:
            print("\nMain Menu:")
            print("1. EC2 Instance Management")
            print("2. IAM Role Management")
            print("3. S3 Bucket Management")
            print("4. Exit")
            
            choice = input("\nSelect an option (1-4): ").strip()
            
            if choice == '1':
                self.ec2_menu()
            elif choice == '2':
                self.iam_menu()
            elif choice == '3':
                self.s3_menu()
            elif choice == '4':
                logger.info(f"{BOT_NAME} stopped at {datetime.now()}")
                print("\nExiting...")
                break
            else:
                print("Invalid option. Please try again.")
    
    def ec2_menu(self):
        """EC2 management menu"""
        while True:
            print("\nEC2 Instance Management:")
            print("1. List all instances")
            print("2. Launch new instance")
            print("3. Start instance")
            print("4. Stop instance")
            print("5. Terminate instance")
            print("6. Back to main menu")
            
            choice = input("\nSelect an option (1-6): ").strip()
            
            if choice == '1':
                instances = self.ec2.list_instances()
                if instances:
                    print("\nEC2 Instances:")
                    for inst in instances:
                        print(f"  - {inst['InstanceId']} ({inst['InstanceType']}) - {inst['State']}")
            elif choice == '2':
                image_id = input("Enter AMI ID: ").strip()
                instance_type = input("Enter instance type (default: t2.micro): ").strip() or 't2.micro'
                instance_id = self.ec2.launch_instance(image_id, instance_type)
                if instance_id:
                    print(f"Instance launched successfully: {instance_id}")
            elif choice == '3':
                instance_id = input("Enter instance ID: ").strip()
                if self.ec2.start_instance(instance_id):
                    print(f"Instance {instance_id} started successfully")
            elif choice == '4':
                instance_id = input("Enter instance ID: ").strip()
                if self.ec2.stop_instance(instance_id):
                    print(f"Instance {instance_id} stopped successfully")
            elif choice == '5':
                instance_id = input("Enter instance ID: ").strip()
                confirm = input(f"Are you sure you want to terminate {instance_id}? (yes/no): ").strip()
                if confirm.lower() == 'yes':
                    if self.ec2.terminate_instance(instance_id):
                        print(f"Instance {instance_id} terminated successfully")
            elif choice == '6':
                break
            else:
                print("Invalid option. Please try again.")
    
    def iam_menu(self):
        """IAM management menu"""
        while True:
            print("\nIAM Role Management:")
            print("1. List all roles")
            print("2. Create new role")
            print("3. Delete role")
            print("4. Back to main menu")
            
            choice = input("\nSelect an option (1-4): ").strip()
            
            if choice == '1':
                roles = self.iam.list_roles()
                if roles:
                    print("\nIAM Roles:")
                    for role in roles:
                        print(f"  - {role['RoleName']} ({role['Arn']})")
            elif choice == '2':
                role_name = input("Enter role name: ").strip()
                # Basic assume role policy for EC2
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "ec2.amazonaws.com"},
                            "Action": "sts:AssumeRole"
                        }
                    ]
                }
                arn = self.iam.create_role(role_name, policy)
                if arn:
                    print(f"Role created successfully: {arn}")
            elif choice == '3':
                role_name = input("Enter role name: ").strip()
                if self.iam.delete_role(role_name):
                    print(f"Role {role_name} deleted successfully")
            elif choice == '4':
                break
            else:
                print("Invalid option. Please try again.")
    
    def s3_menu(self):
        """S3 bucket management menu"""
        while True:
            print("\nS3 Bucket Management:")
            print("1. List all buckets")
            print("2. Create new bucket")
            print("3. Delete bucket")
            print("4. List objects in bucket")
            print("5. Upload file to bucket")
            print("6. Enable versioning")
            print("7. Back to main menu")
            
            choice = input("\nSelect an option (1-7): ").strip()
            
            if choice == '1':
                buckets = self.s3.list_buckets()
                if buckets:
                    print("\nS3 Buckets:")
                    for bucket in buckets:
                        print(f"  - {bucket['Name']} (Created: {bucket['CreationDate']})")
            elif choice == '2':
                bucket_name = input("Enter bucket name: ").strip()
                if self.s3.create_bucket(bucket_name):
                    print(f"Bucket {bucket_name} created successfully")
            elif choice == '3':
                bucket_name = input("Enter bucket name: ").strip()
                confirm = input(f"Are you sure you want to delete {bucket_name}? (yes/no): ").strip()
                if confirm.lower() == 'yes':
                    if self.s3.delete_bucket(bucket_name):
                        print(f"Bucket {bucket_name} deleted successfully")
            elif choice == '4':
                bucket_name = input("Enter bucket name: ").strip()
                objects = self.s3.list_objects(bucket_name)
                if objects:
                    print(f"\nObjects in {bucket_name}:")
                    for obj in objects:
                        print(f"  - {obj['Key']} ({obj['Size']} bytes)")
            elif choice == '5':
                bucket_name = input("Enter bucket name: ").strip()
                file_path = input("Enter file path: ").strip()
                if self.s3.upload_file(bucket_name, file_path):
                    print(f"File uploaded successfully to {bucket_name}")
            elif choice == '6':
                bucket_name = input("Enter bucket name: ").strip()
                if self.s3.enable_versioning(bucket_name):
                    print(f"Versioning enabled for {bucket_name}")
            elif choice == '7':
                break
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    bot = EBot()
    bot.start()
