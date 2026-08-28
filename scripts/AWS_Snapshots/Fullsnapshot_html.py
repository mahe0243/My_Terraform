#!/usr/bin/env python3
from flask import Flask, request, render_template_string, redirect, url_for, session
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import datetime

app = Flask(__name__)
app.secret_key = "your-secret-key"  # change this to something secure

# Simple user store
USERS = {"admin": "password123"}  # username: password

# Login page HTML
login_html = """
<!doctype html>
<html>
<head>
<title>Login</title>
<style>
body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #2196F3, #4CAF50);
       height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center; }
.login-container { background: #fff; padding: 30px; border-radius: 10px;
                   box-shadow: 0px 4px 10px rgba(0,0,0,0.2); width: 350px; text-align: center; }
h2 { margin-bottom: 20px; color: #333; }
input[type=text], input[type=password] { width: 90%; padding: 10px; margin: 10px 0;
                                         border: 1px solid #ccc; border-radius: 5px; }
input[type=submit] { background: #2196F3; color: #fff; border: none; padding: 10px 20px;
                     border-radius: 5px; cursor: pointer; }
input[type=submit]:hover { background: #1976D2; }
</style>
</head>
<body>
<div class="login-container">
  <h2>Login</h2>
  <form method=post>
    <input type=text name=username placeholder="Username"><br>
    <input type=password name=password placeholder="Password"><br>
    <input type=submit value="Login">
  </form>
</div>
</body>
</html>
"""

# Dashboard HTML
dashboard_html = """
<!doctype html>
<html>
<head>
<title>AWS Snapshot Dashboard</title>
<style>
body { font-family: Arial, sans-serif; margin: 20px; background: #f9f9f9; }
h2 { color: #333; }
.tabs { display: flex; cursor: pointer; margin-bottom: 10px; }
.tab { padding: 10px 20px; border-radius: 5px 5px 0 0; margin-right: 5px; color: #fff; }
.tab.create { background: #4CAF50; }
.tab.list { background: #2196F3; }
.tab.delete { background: #f44336; }
.tab.active { opacity: 0.9; font-weight: bold; }
.tab-content { border: 1px solid #ccc; padding: 20px; background: #fff; border-radius: 0 5px 5px 5px; }
.hidden { display: none; }
input[type=text], input[type=number] { margin: 5px 0; padding: 5px; width: 250px; }
input[type=submit] { margin-top: 10px; padding: 8px 15px; border: none; border-radius: 4px; cursor: pointer; }
input[value="Create Snapshot"] { background: #4CAF50; color: #fff; }
input[value="List Snapshots"] { background: #2196F3; color: #fff; }
input[value="Delete Snapshot"] { background: #f44336; color: #fff; }
</style>
<script>
function showTab(tabId) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
  document.getElementById(tabId).classList.remove('hidden');
  document.querySelector('[data-tab="'+tabId+'"]').classList.add('active');
}
</script>
</head>
<body>

<h2>AWS Snapshot Dashboard</h2>
<p>Logged in as {{user}}</p>
<a href="/logout">Logout</a>

<div class="tabs">
  <div class="tab create active" data-tab="create" onclick="showTab('create')">Create</div>
  <div class="tab list" data-tab="list" onclick="showTab('list')">List</div>
  <div class="tab delete" data-tab="delete" onclick="showTab('delete')">Delete</div>
</div>

<div id="create" class="tab-content">
  <h3>Create Snapshots</h3>
  <form method=post action="/create">
    Instance Name (tag:Name): <input type=text name=instance_name><br>
    OR Instance ID: <input type=text name=instance_id><br>
    AWS Region: <input type=text name=region value="us-east-1"><br>
    Retention Days: <input type=number name=retention value=7><br>
    <input type=submit value="Create Snapshot">
  </form>
</div>

<div id="list" class="tab-content hidden">
  <h3>List Snapshots</h3>
  <form method=get action="/list">
    AWS Region: <input type=text name=region value="us-east-1"><br>
    <input type=submit value="List Snapshots">
  </form>
</div>

<div id="delete" class="tab-content hidden">
  <h3>Delete Snapshot</h3>
  <form method=post action="/delete">
    AWS Region: <input type=text name=region value="us-east-1"><br>
    Snapshot ID: <input type=text name=snapshot_id><br>
    <input type=submit value="Delete Snapshot">
  </form>
</div>

</body>
</html>
"""

# Auth decorator
def login_required(f):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if USERS.get(username) == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials"
    return render_template_string(login_html)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/", methods=["GET"])
@login_required
def dashboard():
    return render_template_string(dashboard_html, user=session["user"])

@app.route("/create", methods=["POST"])
@login_required
def create_snapshot():
    instance_id = request.form.get("instance_id")
    instance_name = request.form.get("instance_name")
    region = request.form["region"]
    retention = int(request.form["retention"])
    ec2 = boto3.client("ec2", region_name=region)
    try:
        if instance_name:
            reservations = ec2.describe_instances(
                Filters=[{"Name": "tag:Name", "Values": [instance_name]}]
            )["Reservations"]
            if not reservations:
                return f"No instance found with Name tag {instance_name}"
            instance_id = reservations[0]["Instances"][0]["InstanceId"]

        volumes = ec2.describe_instances(InstanceIds=[instance_id])["Reservations"][0]["Instances"][0]["BlockDeviceMappings"]

        snapshot_ids = []
        for v in volumes:
            vol_id = v["Ebs"]["VolumeId"]
            desc = f"Snapshot of {vol_id} from {instance_id} at {datetime.datetime.utcnow()}"
            snap = ec2.create_snapshot(VolumeId=vol_id, Description=desc)
            ec2.create_tags(Resources=[snap["SnapshotId"]],
                            Tags=[{"Key": "Retention", "Value": str(retention)}])
            snapshot_ids.append(snap["SnapshotId"])

        snaps = ec2.describe_snapshots(SnapshotIds=snapshot_ids)["Snapshots"]

        output = """
        <h3>Created Snapshots</h3>
        <table border="1" cellpadding="5" cellspacing="0">
          <tr>
            <th>Snapshot ID</th>
            <th>Volume ID</th>
            <th>State</th>
            <th>Start Time</th>
            <th>Description</th>
          </tr>
        """
        for s in snaps:
            output += f"""
              <tr>
                <td>{s['SnapshotId']}</td>
                <td>{s['VolumeId']}</td>
                <td>{s['State']}</td>
                <td>{s['StartTime']}</td>
                <td>{s.get('Description','')}</td>
              </tr>
            """
        output += "</table>"
        return output

    except NoCredentialsError:
        return "Error: No AWS credentials found. Attach IAM role or configure ~/.aws/credentials."
    except ClientError as e:
        return f"AWS Error: {e}"

@app.route("/list", methods=["GET"])
@login_required
def list_snapshots():
    region = request.args.get("region", "us-east-1")
    ec2 = boto3.client("ec2", region_name=region)
    try:
        snaps = ec2.describe_snapshots(OwnerIds=["self"])["Snapshots"]

        output = """
        <h3>Snapshots</h3>
        <table border="1" cellpadding="5" cellspacing="0">
          <tr>
            <th>Snapshot ID</th>
            <th>Volume ID</th>
            <th>State</th>
            <th>Start Time</th>
            <th>Description</th>
          </tr>
        """
        for s in snaps:
            output += f"""
              <tr>
                <td>{s['SnapshotId']}</td>
                <td>{s['VolumeId']}</td>
                <td>{s['State']}</td>
                <td>{s['StartTime']}</td>
                <td>{s.get('Description','')}</td>
              </tr>
            """
        output += "</table>"
        return output

    except NoCredentialsError:
        return "Error: No AWS credentials found. Attach IAM role or configure ~/.aws/credentials."
    except ClientError as e:
        return f"AWS Error: {e}"

@app.route("/delete", methods=["POST"])
@login_required
def delete_snapshot():
    region = request.form["region"]
    snapshot_id = request.form["snapshot_id"]
    ec2 = boto3.client("ec2", region_name=region)
    try:
        ec2.delete_snapshot(SnapshotId=snapshot_id)
        return f"Deleted snapshot {snapshot_id}"
    except NoCredentialsError:
        return "Error: No AWS credentials found. Attach IAM role or configure ~/.aws/credentials."
    except ClientError as e:
        return f"AWS Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
