import json
import boto3
import sys

role_to_assume = sys.argv[1]
primary_account_number = sys.argv[2]
primary_account_user = sys.argv[3]


# Principal has to exist else this would error
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": f"arn:aws:iam::{primary_account_number}:user/{primary_account_user}"
            },
            "Action": "sts:AssumeRole",
            "Condition": {}
        }
    ]
}



client = boto3.client("iam")

try:
    # Try to get the role. If it exists, this call will succeed.
    response = client.get_role(RoleName=role_to_assume)
    print(f"Role '{role_to_assume}' already exists. Updating AssumeRolePolicyDocument.")
    
    # Update the AssumeRolePolicyDocument
    client.update_assume_role_policy(
        RoleName=role_to_assume,
        PolicyDocument=json.dumps(trust_policy)
    )
    print("AssumeRolePolicyDocument updated successfully.")

except client.exceptions.NoSuchEntityException:
    # If the role does not exist, create it.
    response = client.create_role(
        RoleName=role_to_assume,
        AssumeRolePolicyDocument=json.dumps(trust_policy)
    )
    print(response)

except Exception as e:
    # Catch any other exceptions and print the error
    print(f"An error occurred: {e}")