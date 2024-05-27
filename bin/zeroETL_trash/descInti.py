# import boto3

# # Create an API Gateway client
# client = boto3.client('apigateway')

# # Replace 'your_api_id' with the actual ID of your API
# response = client.get_integration(
#     restApiId='your_api_id',
#     resourceId='<resource_id>', # Replace with ID of the specific resource
#     httpMethod='<http_method>'  # Replace with the HTTP method (e.g., GET, POST)
# )

# # Get the IntegrationArn from the response
# integration_arn = response.get('uri')

# print(integration_arn)



import boto3
rds = boto3.client('rds')

response = rds.describe_integrations(
    MaxRecords=123
    # IntegrationIdentifier='b81fc9f5-dcfa-4b9a-89c4-7648f6ebbdf4',
    # Filters=[
    #     {
    #         'Name': 'string',
    #         'Values': [
    #             'string',
    #         ]
    #     },
    # ],
    # MaxRecords=10,
    # Marker='string'
)['Integrations']

# response = rds.describe_integrations(
#     MaxRecords=123,
#     IntegrationIdentifier='06e833e5-2e42-4cf9-b73e-02bb22d8c7e0'
#     # Filters=[
#     #     {
#     #         'Name': 'string',
#     #         'Values': [
#     #             'string',
#     #         ]
#     #     },
#     # ],
#     # MaxRecords=10,
#     # Marker='string'
# )['Integrations']

print(response)