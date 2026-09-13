import logging
from aws_client import AWSClient

logger = logging.getLogger(__name__)

class EC2Manager:
    """Manage EC2 instances"""
    
    def __init__(self):
        self.aws = AWSClient()
        self.ec2 = self.aws.ec2_client
    
    def list_instances(self):
        """List all EC2 instances"""
        try:
            response = self.ec2.describe_instances()
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        'InstanceId': instance['InstanceId'],
                        'InstanceType': instance['InstanceType'],
                        'State': instance['State']['Name'],
                        'LaunchTime': str(instance['LaunchTime']),
                        'PublicIpAddress': instance.get('PublicIpAddress', 'N/A')
                    })
            logger.info(f"Retrieved {len(instances)} instances")
            return instances
        except Exception as e:
            logger.error(f"Error listing instances: {str(e)}")
            return None
    
    def launch_instance(self, image_id, instance_type='t2.micro', key_name=None, security_group_ids=None):
        """Launch a new EC2 instance"""
        try:
            params = {
                'ImageId': image_id,
                'MinCount': 1,
                'MaxCount': 1,
                'InstanceType': instance_type
            }
            
            if key_name:
                params['KeyName'] = key_name
            if security_group_ids:
                params['SecurityGroupIds'] = security_group_ids
            
            response = self.ec2.run_instances(**params)
            instance_id = response['Instances'][0]['InstanceId']
            logger.info(f"Instance launched: {instance_id}")
            return instance_id
        except Exception as e:
            logger.error(f"Error launching instance: {str(e)}")
            return None
    
    def stop_instance(self, instance_id):
        """Stop an EC2 instance"""
        try:
            self.ec2.stop_instances(InstanceIds=[instance_id])
            logger.info(f"Instance stopped: {instance_id}")
            return True
        except Exception as e:
            logger.error(f"Error stopping instance: {str(e)}")
            return False
    
    def start_instance(self, instance_id):
        """Start an EC2 instance"""
        try:
            self.ec2.start_instances(InstanceIds=[instance_id])
            logger.info(f"Instance started: {instance_id}")
            return True
        except Exception as e:
            logger.error(f"Error starting instance: {str(e)}")
            return False
    
    def terminate_instance(self, instance_id):
        """Terminate an EC2 instance"""
        try:
            self.ec2.terminate_instances(InstanceIds=[instance_id])
            logger.info(f"Instance terminated: {instance_id}")
            return True
        except Exception as e:
            logger.error(f"Error terminating instance: {str(e)}")
            return False
