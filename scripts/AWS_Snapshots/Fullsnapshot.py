import boto3
import argparse
import datetime

REGION = "us-east-1"
AWS_CONN = boto3.session.Session(region_name=REGION)
EC2_CLIENT = AWS_CONN.client("ec2", region_name=REGION)
EC2_RESOURCE = AWS_CONN.resource("ec2", region_name=REGION)

def load_targets(filename="instances.txt"):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def create_snapshot(targets, use_names=False):
    if use_names:
        reservations = EC2_CLIENT.describe_instances(
            Filters=[{"Name": "tag:Name", "Values": targets}]
        )["Reservations"]
    else:
        reservations = EC2_CLIENT.describe_instances(InstanceIds=targets)["Reservations"]

    snapshot_group_id = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            for bd in instance["BlockDeviceMappings"]:
                if "Ebs" in bd:
                    volume_id = bd["Ebs"]["VolumeId"]

                    snapshot = EC2_RESOURCE.create_snapshot(
                        VolumeId=volume_id,
                        TagSpecifications=[
                            {
                                "ResourceType": "snapshot",
                                "Tags": [
                                    {"Key": "Name", "Value": f"Snapshot-{instance_id}-{volume_id}"},
                                    {"Key": "InstanceId", "Value": instance_id},
                                    {"Key": "SnapshotGroup", "Value": snapshot_group_id},
                                ],
                            },
                        ],
                    )
                    print(f"Snapshot captured for EC2 {instance_id}, Volume {volume_id}: {snapshot.id}")

def listing_snapshot():
    snapshots = EC2_CLIENT.describe_snapshots(OwnerIds=["self"])["Snapshots"]
    print("SnapshotID | StartTime | State | VolumeId | SnapshotGroup")
    for snap in snapshots:
        group = next((t["Value"] for t in snap.get("Tags", []) if t["Key"] == "SnapshotGroup"), "-")
        print(f"{snap['SnapshotId']} | {snap['StartTime']} | {snap['State']} | {snap['VolumeId']} | {group}")

def delete_snapshots():
    snapshots = EC2_CLIENT.describe_snapshots(OwnerIds=["self"])["Snapshots"]
    for snap in snapshots:
        print(f"Deleting snapshot: {snap['SnapshotId']}")
        EC2_CLIENT.delete_snapshot(SnapshotId=snap["SnapshotId"])

parser = argparse.ArgumentParser(description="Multi-volume snapshot script")
parser.add_argument("action", choices=["create_snap", "list_snap", "delete_snap"], help="Action to perform")
parser.add_argument("--file", default="instances.txt", help="File with instance IDs or Names")
parser.add_argument("--use-names", action="store_true", help="Treat file entries as Name tags instead of IDs")
args = parser.parse_args()

targets = load_targets(args.file)

if args.action == "create_snap":
    create_snapshot(targets, use_names=args.use_names)
elif args.action == "list_snap":
    listing_snapshot()
elif args.action == "delete_snap":
    delete_snapshots()


