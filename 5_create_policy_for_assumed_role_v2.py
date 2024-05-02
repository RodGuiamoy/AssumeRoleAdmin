import boto3
import json
import sys

policy_name_for_assumed_role = sys.argv[1]

def create_iam_policy(policy_name, policy_document):
    iam_client = boto3.client("iam")

    # Check if the policy already exists
    try:
        paginator = iam_client.get_paginator('list_policies')
        for response in paginator.paginate(Scope='Local'):
            for policy in response['Policies']:
                if policy['PolicyName'] == policy_name:
                    # print(f"Policy {policy_name} already exists.")
                    return policy['Arn']
    except Exception as e:
        print("Failed to list IAM policies:", str(e))
        exit(1)

    # Create the policy if it does not exist
    try:
        response = iam_client.create_policy(
            PolicyName=policy_name, PolicyDocument=policy_document
        )
        return response['Policy']['Arn']
    except Exception as e:
        print("Failed to create IAM policy:", str(e))
        exit(1)

policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:CreateTags",
                "ec2:CreateImage",
                "ec2:DescribeImages",
                "ec2:DescribeInstances",
            ],
            "Resource": "*",
        }
    ],
}

# Create or retrieve existing IAM policy
policy_arn = create_iam_policy(
    policy_name_for_assumed_role, json.dumps(policy_document)
)

print(policy_arn)
