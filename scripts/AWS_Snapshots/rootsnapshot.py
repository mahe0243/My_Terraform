import boto3
import argparse

# Use the correct region for your VMs
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

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            root_volume = instance["BlockDeviceMappings"][0]["Ebs"]["VolumeId"]

            snapshot = EC2_RESOURCE.create_snapshot(
                VolumeId=root_volume,
                TagSpecifications=[
                    {
                        "ResourceType": "snapshot",
                        "Tags": [
                            {
                                "Key": "Name",
                                "Value": f"Snapshot-{instance_id}-{root_volume}",
                            },
                        ],
                    },
                ],
            )
            print(f"Snapshot captured for EC2 {instance_id}: {snapshot.id}")

def listing_snapshot():
    snapshots = EC2_CLIENT.describe_snapshots(OwnerIds=["self"])["Snapshots"]
    print("SnapshotID\t\t StartTime\t\t\t State\t\t VolumeId")
    for snap in snapshots:
        print(
            f"{snap['SnapshotId']} | {snap['StartTime']} | {snap['State']} | {snap['VolumeId']}"
        )

def delete_snapshots():
    snapshots = EC2_CLIENT.describe_snapshots(OwnerIds=["self"])["Snapshots"]
    for snap in snapshots:
        print(f"Deleting snapshot: {snap['SnapshotId']}")
        EC2_CLIENT.delete_snapshot(SnapshotId=snap["SnapshotId"])

parser = argparse.ArgumentParser(description="Snapshot management script")
parser.add_argument("action", choices=["create_snap", "list_snap", "delete_snap"], help="Action to perform")
parser.add_argument("--file", default="instances.txt", help="File with instance IDs or Names")
parser.add_argument("--use-names", action="store_true", help="Treat file entries as Name tags instead of IDs")
args = parser.parse_args()

targets = load_targets(args.file)

if args.action == "create_snap":
    create_snapshot(targets, use_names=args.use_names)
    listing_snapshot()
elif args.action == "list_snap":
    listing_snapshot()
elif args.action == "delete_snap":
    delete_snapshots()
