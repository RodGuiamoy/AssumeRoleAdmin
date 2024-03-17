import boto3
import json
import sys

policy_name_for_assumed_role = sys.argv[1]


def create_iam_policy(policy_name, policy_document):

    iam_client = boto3.client("iam")

    try:
        response = iam_client.create_policy(
            PolicyName=policy_name, PolicyDocument=policy_document
        )
        return response["Policy"]["Arn"]
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

# Create IAM policy
policy_arn = create_iam_policy(
    policy_name_for_assumed_role, json.dumps(policy_document)
)

print(policy_arn)
