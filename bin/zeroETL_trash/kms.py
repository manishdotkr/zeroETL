import boto3

kmsKey = '06e833e5-2e42-4cf9-b73e-02bb22d8c7e0'

# def get_kms_key_id(alias_name):
#     # Create a KMS client
#     client = boto3.client('kms')

#     aliases = client.list_aliases(
#         Limit=123,
#     )['Aliases']

#     # id = [alias['TargetKeyId'] for alias in aliases if alias['AliasName'] == f'alias/{alias_name}'][0]

#     print(aliases)

def get_kms_key_id(alias_name):
    # Create a KMS client
    client = boto3.client('kms')

    response = client.list_aliases(
        Limit=123,
    )
    print(response)


def get_kms_policy():
    # Create a KMS client
    client = boto3.client('kms')

    response = client.get_key_policy(
        KeyId=kmsKey
    )

    # id = [alias['TargetKeyId'] for alias in aliases if alias['AliasName'] == f'alias/{alias_name}'][0]

    print(response)


# Replace 'your_alias_name' with the alias you want to get the key ID for
alias_name = "stage-extv-redshift-kms"
# key_id = get_kms_key_id(alias_name)
get_kms_key_id(alias_name)
# get_kms_policy()
# print("Key ID:", key_id)
