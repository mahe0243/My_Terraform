# ebot Application Setup Guide

## 🤖 Welcome to ebot - AWS Resource Manager Bot

This guide will help you set up and run the **ebot** application created on **September 13, 2024**.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager - usually comes with Python)
- **AWS Account** with appropriate credentials
- **Git** (optional, for cloning the repository)

---

## 🚀 Quick Start (5 minutes)

### Step 1: Navigate to the Project Directory

```bash
cd My_Terraform
```

### Step 2: Run the Startup Script

**On Linux/macOS:**
```bash
chmod +x start_ebot.sh
./start_ebot.sh
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
mkdir logs
cd ebot_app
python app.py
```

### Step 3: Open Your Browser

Visit: **http://localhost:5000**

You should see the beautiful ebot dashboard with all available features!

---

## 📝 Manual Setup (Step-by-Step)

### Step 1: Create Virtual Environment

```bash
python3 -m venv venv
```

### Step 2: Activate Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `boto3==1.26.137` - AWS SDK for Python
- `botocore==1.29.137` - Botocore library
- `python-dotenv==1.0.0` - Environment variable loader
- `requests==2.31.0` - HTTP library
- `flask==3.0.0` - Web framework
- `werkzeug==3.0.0` - WSGI utility library

### Step 4: Configure AWS Credentials

Edit the `.env` file in the root directory:

```env
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/ebot.log
```

**How to get AWS credentials:**
1. Log in to [AWS Console](https://console.aws.amazon.com)
2. Go to **IAM > Users > Security Credentials**
3. Create an access key
4. Copy the Access Key ID and Secret Access Key
5. Paste them into the `.env` file

### Step 5: Create Logs Directory

```bash
mkdir -p logs
```

### Step 6: Run the Application

```bash
cd ebot_app
python app.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Step 7: Access the Dashboard

Open your web browser and go to:
- **Main Dashboard:** http://localhost:5000
- **Health Check:** http://localhost:5000/health
- **API Info:** http://localhost:5000/api/info

---

## 🎯 Features Overview

### EC2 Management 📦
- List all EC2 instances
- Launch new instances
- Start/stop instances
- Terminate instances

**Example API Call:**
```bash
curl -X GET http://localhost:5000/api/ec2/instances
```

### IAM Management 👥
- List IAM roles
- Create new roles
- Create IAM users
- Attach policies to roles
- Delete roles

**Example API Call:**
```bash
curl -X GET http://localhost:5000/api/iam/roles
```

### S3 Management 🪣
- List S3 buckets
- Create new buckets
- Delete buckets
- List bucket objects
- Upload files
- Enable versioning

**Example API Call:**
```bash
curl -X GET http://localhost:5000/api/s3/buckets
```

---

## 🌐 Web Dashboard Features

The beautiful web dashboard at `http://localhost:5000` includes:

1. **Health Status Card** - Check bot status
2. **EC2 Management Card** - Manage EC2 instances
3. **IAM Management Card** - Manage IAM resources
4. **S3 Management Card** - Manage S3 buckets
5. **Quick Test Buttons** - Test each service
6. **Live Response Display** - See API responses in real-time
7. **Feature List** - View all available features
8. **API Documentation** - Learn how to use the API
9. **Configuration Guide** - Understand environment variables

---

## 📡 API Endpoints

### Health & Info
```
GET  /health              - Health check
GET  /api/info           - Bot information
```

### EC2 Management
```
GET  /api/ec2/instances                    - List instances
POST /api/ec2/instances                    - Launch instance
POST /api/ec2/instances/{id}/start         - Start instance
POST /api/ec2/instances/{id}/stop          - Stop instance
POST /api/ec2/instances/{id}/terminate     - Terminate instance
```

### IAM Management
```
GET  /api/iam/roles                        - List roles
POST /api/iam/roles                        - Create role
POST /api/iam/roles/{name}/attach-policy   - Attach policy
DELETE /api/iam/roles/{name}               - Delete role
POST /api/iam/users                        - Create user
```

### S3 Management
```
GET  /api/s3/buckets                           - List buckets
POST /api/s3/buckets                           - Create bucket
DELETE /api/s3/buckets/{name}                  - Delete bucket
GET  /api/s3/buckets/{name}/objects            - List objects
POST /api/s3/buckets/{name}/upload             - Upload file
POST /api/s3/buckets/{name}/versioning         - Enable versioning
```

---

## 📚 Example API Calls

### Get Health Status
```bash
curl http://localhost:5000/health
```

### List EC2 Instances
```bash
curl http://localhost:5000/api/ec2/instances
```

### Launch EC2 Instance
```bash
curl -X POST http://localhost:5000/api/ec2/instances \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "ami-0c55b159cbfafe1f0",
    "instance_type": "t2.micro"
  }'
```

### List S3 Buckets
```bash
curl http://localhost:5000/api/s3/buckets
```

### Create S3 Bucket
```bash
curl -X POST http://localhost:5000/api/s3/buckets \
  -H "Content-Type: application/json" \
  -d '{
    "bucket_name": "my-test-bucket-123",
    "region": "us-east-1"
  }'
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | AWS access key | - |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | - |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_FILE` | Log file path | `./logs/ebot.log` |

### Log Levels

- **DEBUG** - Detailed information for debugging
- **INFO** - General information (recommended)
- **WARNING** - Warning messages
- **ERROR** - Error messages only

---

## 🐛 Troubleshooting

### Issue: "AWS credentials not found"

**Solution:**
1. Make sure `.env` file exists in the root directory
2. Check that `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are set
3. Verify your credentials are correct from AWS console

### Issue: "Port 5000 already in use"

**Solution:**
1. Kill the process using port 5000:
   ```bash
   # Linux/macOS
   lsof -i :5000
   kill -9 <PID>
   
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```
2. Or change the port in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
1. Make sure virtual environment is activated
2. Run: `pip install -r requirements.txt`

### Issue: "Cannot connect to localhost:5000"

**Solution:**
1. Make sure the Flask app is running
2. Check console output for errors
3. Try accessing: http://127.0.0.1:5000
4. Check firewall settings

---

## 📊 Monitoring & Logs

### View Application Logs

```bash
tail -f logs/ebot.log
```

### Check Application Status

Visit: http://localhost:5000/health

The response will show:
```json
{
  "status": "healthy",
  "bot_name": "ebot",
  "bot_version": "1.0.0",
  "timestamp": "2024-09-13T12:34:56.123456"
}
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Keep it in `.gitignore`
2. **Use IAM User** - Create a separate IAM user for ebot with minimal permissions
3. **Rotate Credentials** - Regularly rotate your AWS access keys
4. **Use HTTPS** - In production, use HTTPS instead of HTTP
5. **API Keys** - Implement API key authentication for production

---

## 🚀 Production Deployment

### Using Gunicorn

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run the app:
   ```bash
   cd ebot_app
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Using Docker

1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   WORKDIR /app/ebot_app
   CMD ["python", "app.py"]
   ```

2. Build and run:
   ```bash
   docker build -t ebot .
   docker run -p 5000:5000 --env-file ../.env ebot
   ```

---

## 📞 Support & Resources

- **AWS Documentation:** https://docs.aws.amazon.com
- **Flask Documentation:** https://flask.palletsprojects.com
- **Boto3 Documentation:** https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

---

## 📄 Project Structure

```
My_Terraform/
├── ebot_app/
│   ├── templates/
│   │   └── index.html          # Web dashboard
│   ├── app.py                  # Main Flask application
│   ├── config.py               # Configuration
│   ├── ec2_manager.py          # EC2 operations
│   ├── iam_manager.py          # IAM operations
│   ├── s3_manager.py           # S3 operations
│   └── aws_client.py           # AWS client
├── logs/                       # Application logs
├── .env                        # Environment variables
├── .env.example               # Example environment file
├── requirements.txt           # Python dependencies
├── start_ebot.sh             # Startup script
└── README.md                 # Project documentation
```

---

## ✅ Checklist

Before using the app, make sure you:

- [ ] Installed Python 3.8+
- [ ] Created `.env` file with AWS credentials
- [ ] Ran `pip install -r requirements.txt`
- [ ] Created `logs` directory
- [ ] Started the application with `python app.py`
- [ ] Opened http://localhost:5000 in browser
- [ ] Tested health endpoint by clicking "Check Health" button

---

## 🎉 You're All Set!

Your ebot application is now ready to manage your AWS resources! 

Start by visiting **http://localhost:5000** and explore the dashboard.

Happy resource managing! 🚀

---

**Application Created:** September 13, 2024  
**Version:** 1.0.0  
**Developed by:** mahe0243
