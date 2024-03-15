import boto3
import json
import sys

role_assumption_policy_name = sys.argv[1]
primary_account_alias = sys.argv[2]
primary_account_number = sys.argv[3]
role_to_assume = sys.argv[4]

# Check if the policy already exists
def policy_exists(role_assumption_policy_name):
    paginator = iam.get_paginator('list_policies')
    for response in paginator.paginate(Scope='Local'):
        for policy in response['Policies']:
            if policy['PolicyName'] == role_assumption_policy_name:
                return policy['Arn']
    return None

# Set up IAM client
iam = boto3.client('iam')


policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": f"{primary_account_alias}",
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Reprimary": f"arn:aws:iam::{primary_account_number}:role/{role_to_assume}"
        }
    ]
}

existing_policy_arn = policy_exists(role_assumption_policy_name)

if existing_policy_arn:
    # print(f"Policy {policy_name} already exists with ARN {existing_policy_arn}.")
    print(existing_policy_arn)
    exit ()

# Create the policy if it does not exist
try:
    response = iam.create_policy(
        PolicyName=role_assumption_policy_name,
        PolicyDocument=json.dumps(policy_document)
    )
    # print(f"Successfully created policy {policy_name} with ARN {response['Policy']['Arn']}.")
    print(response['Policy']['Arn'])
except Exception as e:
    print("Error creating policy:", e)
