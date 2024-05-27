import boto3

client = boto3.client('rds')

# Replace 'your_api_id' with the actual ID of your API
response = client.add_tags_to_resource(
    ResourceName='arn:aws:rds:us-west-2:095767269209:cluster:stage-extv-testauroradb3-cluster',
    Tags=[
        {
            'Key': 'IntegrationArn',
            'Value': 'arn:aws:rds:us-west-2:095767269209:integration:ca0fbac7-706c-4488-880f-b557df30556e'
        }
    ]
)

# Get the IntegrationArn from the response
print(f"tags added------------>{response}")


