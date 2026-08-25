import boto3
import datetime
import json

SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:123456789012:MyEBSSnapshots'
RETENTION_DAYS = 5

# Load config file
with open('backup_config.json') as f:
    config = json.load(f)

INSTANCE_IDS = config.get("instance_ids", [])
INSTANCE_NAMES = config.get("instance_names", [])

def get_instances_by_name(name):
    ec2 = boto3.client('ec2')
    reservations = ec2.describe_instances(Filters=[
        {'Name': 'tag:Name', 'Values': [name]}
    ])['Reservations']
    return [inst['InstanceId'] for r in reservations for inst in r['Instances']]

def create_snapshot_and_notify(instance_id, instance_name=None):
    ec2 = boto3.client('ec2')
    volumes = ec2.describe_volumes(Filters=[
        {'Name': 'attachment.instance-id', 'Values': [instance_id]}
    ])['Volumes']

    created_snapshots = []
    for vol in volumes:
        volume_id = vol['VolumeId']
        snapshot = ec2.create_snapshot(
            VolumeId=volume_id,
            Description=f'Snapshot of {volume_id} ({instance_name or instance_id}) on {datetime.datetime.now()}'
        )

        tags = [
            {'Key': 'CreatedOn', 'Value': datetime.datetime.now().strftime('%Y-%m-%d')},
            {'Key': 'InstanceId', 'Value': instance_id}
        ]
        if instance_name:
            tags.append({'Key': 'InstanceName', 'Value': instance_name})

        ec2.create_tags(Resources=[snapshot['SnapshotId']], Tags=tags)
        created_snapshots.append(snapshot['SnapshotId'])
        print(f"Snapshot {snapshot['SnapshotId']} created for {instance_name or instance_id}")

    return created_snapshots

def cleanup_old_snapshots(instance_id, instance_name=None):
    ec2 = boto3.client('ec2')
    filters = [{'Name': 'tag:InstanceId', 'Values': [instance_id]}, {'Name': 'tag-key', 'Values': ['CreatedOn']}]
    if instance_name:
        filters.append({'Name': 'tag:InstanceName', 'Values': [instance_name]})

    snapshots = ec2.describe_snapshots(Filters=filters)['Snapshots']
    now = datetime.datetime.now(datetime.timezone.utc)
    deleted_snapshots = []

    for snap in snapshots:
        created_on = snap['StartTime']
        age = (now - created_on).days
        if age > RETENTION_DAYS:
            ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])
            deleted_snapshots.append(snap['SnapshotId'])
            print(f"Deleted old snapshot {snap['SnapshotId']} (age {age} days)")
    return deleted_snapshots

def send_report(created, deleted):
    sns = boto3.client('sns')
    report = "Daily Snapshot Report\n\n"
    report += "Created Snapshots:\n" + "\n".join(created) if created else "No snapshots created today.\n"
    report += "\n\nDeleted Snapshots:\n" + "\n".join(deleted) if deleted else "No snapshots deleted today.\n"

    sns.publish(TopicArn=SNS_TOPIC_ARN, Message=report, Subject='Daily EBS Snapshot Report')
    print("Daily report sent via SNS.")

def main():
    all_created, all_deleted = [], []

    # Run for instance IDs
    for inst in INSTANCE_IDS:
        created = create_snapshot_and_notify(inst)
        deleted = cleanup_old_snapshots(inst)
        all_created.extend(created)
        all_deleted.extend(deleted)

    # Run for instance Names
    for name in INSTANCE_NAMES:
        ids = get_instances_by_name(name)
        for inst in ids:
            created = create_snapshot_and_notify(inst, name)
            deleted = cleanup_old_snapshots(inst, name)
            all_created.extend(created)
            all_deleted.extend(deleted)

    send_report(all_created, all_deleted)

if __name__ == "__main__":
    main()
