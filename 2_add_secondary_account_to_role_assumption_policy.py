import boto3
import json
import sys

role_assumption_policy_arn = sys.argv[1]
secondary_account_alias = sys.argv[2]
secondary_account_number = sys.argv[3]
role_to_assume = sys.argv[4]

# Initialize the IAM client
iam = boto3.client("iam")

# Assuming new_policy_statement is properly defined
new_policy_statement = {
    "Sid": secondary_account_alias,
    "Effect": "Allow",
    "Action": "sts:AssumeRole",
    "Resource": f"arn:aws:iam::{secondary_account_number}:role/{role_to_assume}",
}

try:
    # Fetch current policy version
    policy = iam.get_policy(PolicyArn=role_assumption_policy_arn)
    default_version_id = policy["Policy"]["DefaultVersionId"]
    policy_version = iam.get_policy_version(
        PolicyArn=role_assumption_policy_arn, VersionId=default_version_id
    )

    # Extract and modify the policy document
    policy_document = policy_version["PolicyVersion"][
        "Document"
    ]  # This should be a dict

    if "Statement" in policy_document:
        policy_document["Statement"].append(new_policy_statement)
    else:
        policy_document["Statement"] = [new_policy_statement]

    # Serialize the updated document to JSON
    policy_document_str = json.dumps(policy_document)  # Ensure it's a string here

    # Create a new version of the policy
    response = iam.create_policy_version(
        PolicyArn=role_assumption_policy_arn,
        PolicyDocument=policy_document_str,  # Pass the string, not the dict
        SetAsDefault=True,
    )
    print("Policy updated successfully:", response)
except TypeError as e:
    print(f"TypeError: {e}")
except Exception as e:
    print(f"Error updating policy: {e}")
