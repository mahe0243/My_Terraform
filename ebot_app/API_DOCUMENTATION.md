# ebot Flask API Documentation

## Overview
The ebot Flask API provides REST endpoints for managing AWS resources including EC2 instances, IAM roles, and S3 buckets.

## Getting Started

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
cd ebot_app
python app.py
```

The API will start on `http://localhost:5000`

---

## API Endpoints

### Health & Info Endpoints

#### Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "bot_name": "ebot",
  "bot_version": "1.0.0",
  "timestamp": "2026-09-13T10:30:45.123456"
}
```

#### Get Bot Information
```
GET /api/info
```
**Response:**
```json
{
  "name": "ebot",
  "version": "1.0.0",
  "description": "AWS Resource Manager Bot",
  "endpoints": {
    "health": "/health",
    "info": "/api/info",
    "ec2": "/api/ec2/*",
    "iam": "/api/iam/*",
    "s3": "/api/s3/*"
  }
}
```

---

## EC2 Endpoints

### List All EC2 Instances
```
GET /api/ec2/instances
```
**Response:**
```json
{
  "status": "success",
  "count": 2,
  "instances": [
    {
      "InstanceId": "i-1234567890abcdef0",
      "InstanceType": "t2.micro",
      "State": "running",
      "LaunchTime": "2026-09-13 10:15:30.123456",
      "PublicIpAddress": "54.123.45.67"
    }
  ]
}
```

### Launch New EC2 Instance
```
POST /api/ec2/instances
```
**Request Body:**
```json
{
  "image_id": "ami-0c55b159cbfafe1f0",
  "instance_type": "t2.micro",
  "key_name": "my-key",
  "security_group_ids": ["sg-12345678"]
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Instance launched successfully",
  "instance_id": "i-1234567890abcdef0"
}
```

### Start EC2 Instance
```
POST /api/ec2/instances/<instance_id>/start
```
**Response:**
```json
{
  "status": "success",
  "message": "Instance i-1234567890abcdef0 started successfully"
}
```

### Stop EC2 Instance
```
POST /api/ec2/instances/<instance_id>/stop
```
**Response:**
```json
{
  "status": "success",
  "message": "Instance i-1234567890abcdef0 stopped successfully"
}
```

### Terminate EC2 Instance
```
POST /api/ec2/instances/<instance_id>/terminate
```
**Response:**
```json
{
  "status": "success",
  "message": "Instance i-1234567890abcdef0 terminated successfully"
}
```

---

## IAM Endpoints

### List All IAM Roles
```
GET /api/iam/roles
```
**Response:**
```json
{
  "status": "success",
  "count": 2,
  "roles": [
    {
      "RoleName": "EC2-Role",
      "Arn": "arn:aws:iam::123456789012:role/EC2-Role",
      "CreateDate": "2026-09-13 10:00:00.123456"
    }
  ]
}
```

### Create New IAM Role
```
POST /api/iam/roles
```
**Request Body:**
```json
{
  "role_name": "MyNewRole",
  "assume_role_policy": {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {"Service": "ec2.amazonaws.com"},
        "Action": "sts:AssumeRole"
      }
    ]
  }
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Role created successfully",
  "role_arn": "arn:aws:iam::123456789012:role/MyNewRole"
}
```

### Attach Policy to Role
```
POST /api/iam/roles/<role_name>/attach-policy
```
**Request Body:**
```json
{
  "policy_arn": "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Policy attached to role MyNewRole"
}
```

### Delete IAM Role
```
DELETE /api/iam/roles/<role_name>
```
**Response:**
```json
{
  "status": "success",
  "message": "Role MyNewRole deleted successfully"
}
```

### Create IAM User
```
POST /api/iam/users
```
**Request Body:**
```json
{
  "user_name": "john.doe"
}
```
**Response:**
```json
{
  "status": "success",
  "message": "User created successfully",
  "user_arn": "arn:aws:iam::123456789012:user/john.doe"
}
```

---

## S3 Endpoints

### List All S3 Buckets
```
GET /api/s3/buckets
```
**Response:**
```json
{
  "status": "success",
  "count": 2,
  "buckets": [
    {
      "Name": "my-bucket",
      "CreationDate": "2026-09-13 09:30:00.123456"
    }
  ]
}
```

### Create New S3 Bucket
```
POST /api/s3/buckets
```
**Request Body:**
```json
{
  "bucket_name": "my-new-bucket",
  "region": "us-west-2"
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Bucket my-new-bucket created successfully"
}
```

### Delete S3 Bucket
```
DELETE /api/s3/buckets/<bucket_name>
```
**Response:**
```json
{
  "status": "success",
  "message": "Bucket my-bucket deleted successfully"
}
```

### List Objects in Bucket
```
GET /api/s3/buckets/<bucket_name>/objects
```
**Response:**
```json
{
  "status": "success",
  "bucket": "my-bucket",
  "count": 3,
  "objects": [
    {
      "Key": "file1.txt",
      "Size": 1024,
      "LastModified": "2026-09-13 09:45:00.123456"
    }
  ]
}
```

### Upload File to Bucket
```
POST /api/s3/buckets/<bucket_name>/upload
```
**Request Body:**
```json
{
  "file_path": "/path/to/local/file.txt",
  "object_name": "remote-file.txt"
}
```
**Response:**
```json
{
  "status": "success",
  "message": "File uploaded to my-bucket"
}
```

### Enable Versioning on Bucket
```
POST /api/s3/buckets/<bucket_name>/versioning
```
**Response:**
```json
{
  "status": "success",
  "message": "Versioning enabled for my-bucket"
}
```

---

## Error Responses

### 404 - Not Found
```json
{
  "status": "error",
  "message": "Endpoint not found",
  "path": "/api/invalid/path"
}
```

### 405 - Method Not Allowed
```json
{
  "status": "error",
  "message": "Method not allowed",
  "path": "/api/ec2/instances"
}
```

### 500 - Internal Server Error
```json
{
  "status": "error",
  "message": "Internal server error"
}
```

---

## Testing with cURL

### List EC2 Instances
```bash
curl -X GET http://localhost:5000/api/ec2/instances
```

### Launch New Instance
```bash
curl -X POST http://localhost:5000/api/ec2/instances \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "ami-0c55b159cbfafe1f0",
    "instance_type": "t2.micro"
  }'
```

### Stop an Instance
```bash
curl -X POST http://localhost:5000/api/ec2/instances/i-1234567890abcdef0/stop
```

### List S3 Buckets
```bash
curl -X GET http://localhost:5000/api/s3/buckets
```

### Create S3 Bucket
```bash
curl -X POST http://localhost:5000/api/s3/buckets \
  -H "Content-Type: application/json" \
  -d '{
    "bucket_name": "my-new-bucket"
  }'
```

---

## Configuration

Update `.env` file with your AWS credentials:
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
LOG_LEVEL=INFO
LOG_FILE=./logs/ebot.log
```

---

## Notes

- All timestamps are in ISO 8601 format
- AWS credentials must be configured in `.env` file
- Ensure proper AWS IAM permissions are set for your credentials
- The API runs on port 5000 by default (configurable in `app.py`)
