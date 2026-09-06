#Snapshot#
**Using instance IDs**
python snapshot.py create_snap --file instances.txt

**Using Name tags**
python snapshot.py create_snap --file instances.txt --use-names

**List snapshots**
python snapshot.py list_snap

**Delete snapshots**
python snapshot.py delete_snap


**Multi-environment run with terraform**

*terraform init

*terraform plan -var-file=prod.tfvars

*terraform apply -var-file=prod.tfvars

**Deploy QA:**

terraform apply -var-file=qa.tfvars

**Deploy DEV:**

terraform apply -var-file=qa.tfvars



