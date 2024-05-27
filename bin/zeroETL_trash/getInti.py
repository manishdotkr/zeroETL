import boto3

rds = boto3.client('rds')

integrations = rds.describe_integrations(
    MaxRecords=99
)['Integrations']

integrationArn = [integration['IntegrationArn'] for integration in integrations if integration['IntegrationName'] == 'aurora-redshift-integration' ][0]
print(integrationArn)

integrationId = integrationArn.split(':')[-1]

print(integrationId)