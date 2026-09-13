import logging
import json
from aws_client import AWSClient

logger = logging.getLogger(__name__)

class IAMManager:
    """Manage IAM roles and policies"""
    
    def __init__(self):
        self.aws = AWSClient()
        self.iam = self.aws.iam_client
    
    def list_roles(self):
        """List all IAM roles"""
        try:
            response = self.iam.list_roles()
            roles = []
            for role in response['Roles']:
                roles.append({
                    'RoleName': role['RoleName'],
                    'Arn': role['Arn'],
                    'CreateDate': str(role['CreateDate'])
                })
            logger.info(f"Retrieved {len(roles)} IAM roles")
            return roles
        except Exception as e:
            logger.error(f"Error listing roles: {str(e)}")
            return None
    
    def create_role(self, role_name, assume_role_policy_document):
        """Create a new IAM role"""
        try:
            response = self.iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(assume_role_policy_document)
            )
            logger.info(f"Role created: {role_name}")
            return response['Role']['Arn']
        except Exception as e:
            logger.error(f"Error creating role: {str(e)}")
            return None
    
    def attach_policy_to_role(self, role_name, policy_arn):
        """Attach a policy to a role"""
        try:
            self.iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            logger.info(f"Policy attached to role: {role_name}")
            return True
        except Exception as e:
            logger.error(f"Error attaching policy: {str(e)}")
            return False
    
    def create_user(self, user_name):
        """Create a new IAM user"""
        try:
            response = self.iam.create_user(UserName=user_name)
            logger.info(f"User created: {user_name}")
            return response['User']['Arn']
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return None
    
    def delete_role(self, role_name):
        """Delete an IAM role"""
        try:
            self.iam.delete_role(RoleName=role_name)
            logger.info(f"Role deleted: {role_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting role: {str(e)}")
            return False
