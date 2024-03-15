import boto3
import sys

role_to_assume = sys.argv[1]
policy_arn_for_assumed_role = sys.argv[2]

iam_client = boto3.client('iam')

print(f"Attaching policy: {policy_arn_for_assumed_role}")
response = iam_client.attach_role_policy(
    PolicyArn=policy_arn_for_assumed_role,
    RoleName=role_to_assume
)

print(response)