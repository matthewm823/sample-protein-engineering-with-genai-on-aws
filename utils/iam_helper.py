import boto3

class IamHelper:

    def __init__(self):
        self.iam_client = boto3.client('iam')

    def find_role_by_pattern(self, pattern):
        try:
            paginator = self.iam_client.get_paginator('list_roles')
            
            for page in paginator.paginate():
                for role in page['Roles']:
                    if pattern.lower() in role['RoleName'].lower():
                        return role['RoleName']
            return
        except Exception as e:
            print(f"Error: {e}")
            return
        
    def find_role_arn_by_pattern(self, pattern):
        try:
            paginator = self.iam_client.get_paginator('list_roles')
            
            for page in paginator.paginate():
                for role in page['Roles']:
                    if pattern.lower() in role['RoleName'].lower():
                        return role['Arn']
            return
        except Exception as e:
            print(f"Error: {e}")
            return