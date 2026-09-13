import logging
import json
from flask import Flask, request, jsonify
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

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize managers
aws_client = AWSClient()
ec2_manager = EC2Manager()
iam_manager = IAMManager()
s3_manager = S3Manager()

# ============= HEALTH & INFO ENDPOINTS =============

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'bot_name': BOT_NAME,
        'bot_version': BOT_VERSION,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/info', methods=['GET'])
def info():
    """Get bot information"""
    return jsonify({
        'name': BOT_NAME,
        'version': BOT_VERSION,
        'description': 'AWS Resource Manager Bot',
        'endpoints': {
            'health': '/health',
            'info': '/api/info',
            'ec2': '/api/ec2/*',
            'iam': '/api/iam/*',
            's3': '/api/s3/*'
        }
    }), 200


# ============= EC2 ENDPOINTS =============

@app.route('/api/ec2/instances', methods=['GET'])
def get_instances():
    """Get all EC2 instances"""
    try:
        instances = ec2_manager.list_instances()
        if instances is not None:
            return jsonify({
                'status': 'success',
                'count': len(instances),
                'instances': instances
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to list instances'
            }), 500
    except Exception as e:
        logger.error(f"Error in get_instances: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/ec2/instances', methods=['POST'])
def launch_instance():
    """Launch a new EC2 instance"""
    try:
        data = request.get_json()
        
        if not data or 'image_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: image_id'
            }), 400
        
        image_id = data['image_id']
        instance_type = data.get('instance_type', 't2.micro')
        key_name = data.get('key_name')
        security_group_ids = data.get('security_group_ids')
        
        instance_id = ec2_manager.launch_instance(
            image_id=image_id,
            instance_type=instance_type,
            key_name=key_name,
            security_group_ids=security_group_ids
        )
        
        if instance_id:
            return jsonify({
                'status': 'success',
                'message': 'Instance launched successfully',
                'instance_id': instance_id
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to launch instance'
            }), 500
    except Exception as e:
        logger.error(f"Error in launch_instance: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/ec2/instances/<instance_id>/start', methods=['POST'])
def start_instance_api(instance_id):
    """Start an EC2 instance"""
    try:
        success = ec2_manager.start_instance(instance_id)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Instance {instance_id} started successfully'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to start instance {instance_id}'
            }), 500
    except Exception as e:
        logger.error(f"Error in start_instance_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/ec2/instances/<instance_id>/stop', methods=['POST'])
def stop_instance_api(instance_id):
    """Stop an EC2 instance"""
    try:
        success = ec2_manager.stop_instance(instance_id)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Instance {instance_id} stopped successfully'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to stop instance {instance_id}'
            }), 500
    except Exception as e:
        logger.error(f"Error in stop_instance_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/ec2/instances/<instance_id>/terminate', methods=['POST'])
def terminate_instance_api(instance_id):
    """Terminate an EC2 instance"""
    try:
        success = ec2_manager.terminate_instance(instance_id)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Instance {instance_id} terminated successfully'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to terminate instance {instance_id}'
            }), 500
    except Exception as e:
        logger.error(f"Error in terminate_instance_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============= IAM ENDPOINTS =============

@app.route('/api/iam/roles', methods=['GET'])
def get_roles():
    """Get all IAM roles"""
    try:
        roles = iam_manager.list_roles()
        if roles is not None:
            return jsonify({
                'status': 'success',
                'count': len(roles),
                'roles': roles
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to list roles'
            }), 500
    except Exception as e:
        logger.error(f"Error in get_roles: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/iam/roles', methods=['POST'])
def create_role_api():
    """Create a new IAM role"""
    try:
        data = request.get_json()
        
        if not data or 'role_name' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: role_name'
            }), 400
        
        role_name = data['role_name']
        assume_role_policy = data.get('assume_role_policy', {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "ec2.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        })
        
        arn = iam_manager.create_role(role_name, assume_role_policy)
        
        if arn:
            return jsonify({
                'status': 'success',
                'message': 'Role created successfully',
                'role_arn': arn
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to create role'
            }), 500
    except Exception as e:
        logger.error(f"Error in create_role_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/iam/roles/<role_name>/attach-policy', methods=['POST'])
def attach_policy_api(role_name):
    """Attach a policy to an IAM role"""
    try:
        data = request.get_json()
        
        if not data or 'policy_arn' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: policy_arn'
            }), 400
        
        policy_arn = data['policy_arn']
        success = iam_manager.attach_policy_to_role(role_name, policy_arn)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Policy attached to role {role_name}'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to attach policy to role {role_name}'
            }), 500
    except Exception as e:
        logger.error(f"Error in attach_policy_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/iam/roles/<role_name>', methods=['DELETE'])
def delete_role_api(role_name):
    """Delete an IAM role"""
    try:
        success = iam_manager.delete_role(role_name)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Role {role_name} deleted successfully'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to delete role {role_name}'
            }), 500
    except Exception as e:
        logger.error(f"Error in delete_role_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/iam/users', methods=['POST'])
def create_user_api():
    """Create a new IAM user"""
    try:
        data = request.get_json()
        
        if not data or 'user_name' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: user_name'
            }), 400
        
        user_name = data['user_name']
        arn = iam_manager.create_user(user_name)
        
        if arn:
            return jsonify({
                'status': 'success',
                'message': 'User created successfully',
                'user_arn': arn
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to create user'
            }), 500
    except Exception as e:
        logger.error(f"Error in create_user_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============= S3 ENDPOINTS =============

@app.route('/api/s3/buckets', methods=['GET'])
def get_buckets():
    """Get all S3 buckets"""
    try:
        buckets = s3_manager.list_buckets()
        if buckets is not None:
            return jsonify({
                'status': 'success',
                'count': len(buckets),
                'buckets': buckets
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to list buckets'
            }), 500
    except Exception as e:
        logger.error(f"Error in get_buckets: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/s3/buckets', methods=['POST'])
def create_bucket_api():
    """Create a new S3 bucket"""
    try:
        data = request.get_json()
        
        if not data or 'bucket_name' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: bucket_name'
            }), 400
        
        bucket_name = data['bucket_name']
        region = data.get('region')
        
        success = s3_manager.create_bucket(bucket_name, region)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Bucket {bucket_name} created successfully'
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to create bucket {bucket_name}'
            }), 500
    except Exception as e:
        logger.error(f"Error in create_bucket_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/s3/buckets/<bucket_name>', methods=['DELETE'])
def delete_bucket_api(bucket_name):
    """Delete an S3 bucket"""
    try:
        success = s3_manager.delete_bucket(bucket_name)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Bucket {bucket_name} deleted successfully'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to delete bucket {bucket_name}'
            }), 500
    except Exception as e:
        logger.error(f"Error in delete_bucket_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/s3/buckets/<bucket_name>/objects', methods=['GET'])
def get_bucket_objects(bucket_name):
    """List objects in an S3 bucket"""
    try:
        objects = s3_manager.list_objects(bucket_name)
        if objects is not None:
            return jsonify({
                'status': 'success',
                'bucket': bucket_name,
                'count': len(objects),
                'objects': objects
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to list objects in bucket {bucket_name}'
            }), 500
    except Exception as e:
        logger.error(f"Error in get_bucket_objects: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/s3/buckets/<bucket_name>/upload', methods=['POST'])
def upload_file_api(bucket_name):
    """Upload a file to an S3 bucket"""
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: file_path'
            }), 400
        
        file_path = data['file_path']
        object_name = data.get('object_name')
        
        success = s3_manager.upload_file(bucket_name, file_path, object_name)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'File uploaded to {bucket_name}'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to upload file to {bucket_name}'
            }), 500
    except Exception as e:
        logger.error(f"Error in upload_file_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/s3/buckets/<bucket_name>/versioning', methods=['POST'])
def enable_versioning_api(bucket_name):
    """Enable versioning on an S3 bucket"""
    try:
        success = s3_manager.enable_versioning(bucket_name)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Versioning enabled for {bucket_name}'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to enable versioning for {bucket_name}'
            }), 500
    except Exception as e:
        logger.error(f"Error in enable_versioning_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'path': request.path
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Method not allowed',
        'path': request.path
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    logger.info(f"Starting {BOT_NAME} v{BOT_VERSION}")
    app.run(debug=True, host='0.0.0.0', port=5000)
