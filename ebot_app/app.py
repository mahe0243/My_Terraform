import logging
import json
from flask import Flask, request, jsonify, render_template
from datetime import datetime

# Setup logging
logging.basicConfig(
    level='INFO',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ============= WEB INTERFACE =============

@app.route('/', methods=['GET'])
def index():
    """Serve the main dashboard"""
    return render_template('index.html')


# ============= HEALTH & INFO ENDPOINTS =============

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    logger.info("Health check requested")
    return jsonify({
        'status': 'healthy',
        'bot_name': 'ebot',
        'bot_version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'message': 'ebot API is running successfully!'
    }), 200


@app.route('/api/info', methods=['GET'])
def info():
    """Get bot information"""
    logger.info("Info requested")
    return jsonify({
        'name': 'ebot',
        'version': '1.0.0',
        'description': 'AWS Resource Manager Bot',
        'created': '2024-09-13',
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
    logger.info("EC2 instances requested")
    try:
        return jsonify({
            'status': 'success',
            'message': 'Configure AWS credentials in .env file to list instances',
            'count': 0,
            'instances': []
        }), 200
    except Exception as e:
        logger.error(f"Error in get_instances: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/ec2/instances', methods=['POST'])
def launch_instance():
    """Launch a new EC2 instance"""
    logger.info("Launch instance requested")
    try:
        data = request.get_json()
        
        if not data or 'image_id' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: image_id'
            }), 400
        
        return jsonify({
            'status': 'success',
            'message': 'Configure AWS credentials in .env file to launch instances',
            'instance_id': 'i-xxxxxxxxxxxx'
        }), 201
    except Exception as e:
        logger.error(f"Error in launch_instance: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============= IAM ENDPOINTS =============

@app.route('/api/iam/roles', methods=['GET'])
def get_roles():
    """Get all IAM roles"""
    logger.info("IAM roles requested")
    try:
        return jsonify({
            'status': 'success',
            'message': 'Configure AWS credentials in .env file to list roles',
            'count': 0,
            'roles': []
        }), 200
    except Exception as e:
        logger.error(f"Error in get_roles: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/iam/roles', methods=['POST'])
def create_role_api():
    """Create a new IAM role"""
    logger.info("Create role requested")
    try:
        data = request.get_json()
        
        if not data or 'role_name' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: role_name'
            }), 400
        
        return jsonify({
            'status': 'success',
            'message': 'Configure AWS credentials to create roles',
            'role_arn': 'arn:aws:iam::123456789012:role/example-role'
        }), 201
    except Exception as e:
        logger.error(f"Error in create_role_api: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============= S3 ENDPOINTS =============

@app.route('/api/s3/buckets', methods=['GET'])
def get_buckets():
    """Get all S3 buckets"""
    logger.info("S3 buckets requested")
    try:
        return jsonify({
            'status': 'success',
            'message': 'Configure AWS credentials in .env file to list buckets',
            'count': 0,
            'buckets': []
        }), 200
    except Exception as e:
        logger.error(f"Error in get_buckets: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/s3/buckets', methods=['POST'])
def create_bucket_api():
    """Create a new S3 bucket"""
    logger.info("Create bucket requested")
    try:
        data = request.get_json()
        
        if not data or 'bucket_name' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required parameter: bucket_name'
            }), 400
        
        return jsonify({
            'status': 'success',
            'message': 'Configure AWS credentials to create buckets'
        }), 201
    except Exception as e:
        logger.error(f"Error in create_bucket_api: {str(e)}")
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
    logger.info("Starting ebot v1.0.0")
    logger.info("Dashboard available at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
