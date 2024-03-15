import boto3
import sys

# Initialize a boto3 client
iam_client = boto3.client("iam")

# User details
# user_name = 'rod_test_031124_00'  # Update this to the desired new user name
# policy_arn = 'arn:aws:iam::554249804926:policy/AMICreationAssumeRole'  # Update this to your policy ARN

user_name = sys.argv[1]
role_assumption_policy_arn = sys.argv[2]


# Check if the user already exists
def check_user_exists(user_name):
    try:
        iam_client.get_user(UserName=user_name)
        print(f"User {user_name} already exists.")
        return True
    except iam_client.exceptions.NoSuchEntityException:
        print(f"User {user_name} does not exist.")
        return False
    except Exception as e:
        print(f"Error checking user existence: {e}")
        return False


# Create a new IAM user
def create_user(user_name):
    try:
        response = iam_client.create_user(UserName=user_name)
        print(f"User {user_name} created successfully.")
        return response
    except Exception as e:
        print(f"Error creating user: {e}")


# Attach a policy to the user
def attach_user_policy(user_name, policy_arn):
    try:
        iam_client.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
        print(f"Policy {policy_arn} attached to user {user_name} successfully.")
    except Exception as e:
        print(f"Error attaching policy: {e}")


# Main function
# Check if the user already exists
user_exists = check_user_exists(user_name)

# If the user does not exist, create the user and attach the policy
if not user_exists:
    create_user_response = create_user(user_name)
    # If the user was created successfully, attach the policy

attach_user_policy(user_name, role_assumption_policy_arn)
