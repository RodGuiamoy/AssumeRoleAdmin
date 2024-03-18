import boto3
import json
import sys
from botocore.exceptions import ClientError

role_assumption_policy_arn = sys.argv[1]
secondary_account_alias = sys.argv[2]
secondary_account_number = sys.argv[3]
role_to_assume = sys.argv[4]

# Initialize the IAM client
iam = boto3.client("iam")

def delete_oldest_policy_version_if_max(policy_arn):
    # Get all versions of the policy
    policy_versions = iam.list_policy_versions(PolicyArn=policy_arn)
    versions = policy_versions['Versions']

    # Check if the number of versions is already at the limit (5)
    if len(versions) < 5:
        print("The number of policy versions is less than the limit (5). No need to delete.")
        return
    # else:
    
    # Filter out the default version
    non_default_versions = [v for v in versions if not v['IsDefaultVersion']]

    # Check again in case all versions are default, which is unlikely but good for robustness
    if not non_default_versions:
        print("No non-default versions to delete.")
        return

    # Find the oldest non-default version
    oldest_version = sorted(non_default_versions, key=lambda x: x['CreateDate'])[0]

    # Delete the oldest version
    iam.delete_policy_version(
        PolicyArn=policy_arn,
        VersionId=oldest_version['VersionId']
    )
    print(f"Deleted the oldest policy version: {oldest_version['VersionId']} because the policy versions limit will be reached in the next update.")


# Assuming new_policy_statement is properly defined
new_policy_statement = {
    "Sid": secondary_account_alias,
    "Effect": "Allow",
    "Action": "sts:AssumeRole",
    "Resource": f"arn:aws:iam::{secondary_account_number}:role/{role_to_assume}",
}

try:
    
    delete_oldest_policy_version_if_max(role_assumption_policy_arn)
    
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
    exit(1)
except ClientError as e:
    # Check for the MalformedPolicyDocument error code
    if e.response['Error']['Code'] == 'MalformedPolicyDocument':
        print(f"WARNING: An account with the alias {secondary_account_alias} has already been added to this policy. No changes will be made.")
        # Handle this error specifically without exiting, perhaps log it or notify someone
    else:
        print(f"Unhandled client error: {e}")
        exit(1)
except Exception as e:
    print(f"Error updating policy: {e}")
    exit(1)
