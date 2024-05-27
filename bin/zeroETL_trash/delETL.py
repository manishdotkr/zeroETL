# import boto3

# # Replace with your Aurora cluster details
# client = boto3.client('rds')
# db_cluster_identifier = 'stage-extv-testauroradb3-cluster'


# describe_cluster_response = client.describe_db_clusters(
#     DBClusterIdentifier=db_cluster_identifier
# )
# aurora_cluster = describe_cluster_response['DBClusters'][0]
# print(aurora_cluster)
# integration_arn = aurora_cluster.get('ZeroETLConfiguration', {}).get('IntegrationARN')

# if integration_arn:
#   print(f"Integration ARN: {integration_arn}")
# else:
#   print("No zero-ETL integration found for this cluster.")


import json
import boto3
import time

# Build the client using the default credential configuration.
# You can use the CLI and run 'aws configure' to set access key, secret
# key, and default Region.

rds = boto3.client('rds')
redshift = boto3.client('redshift')
sts = boto3.client('sts')

# source_cluster_name = 'stage-extv-testauroradb3-cluster' # A name for the source cluster
# target_cluster_name = 'stage-extv-redshift-test' # A name for the target cluster

# RedshiftIntegrationName='8b65d40e-67a5-4377-a47a-a80bc1ea7ba9'
# RedshiftIntegrationName='Aurora-Redshift-integration'

def main():
    
    response = rds.delete_integration(
        IntegrationIdentifier="36211636-3ba2-4d95-8703-bfdab0e7209b"
    )

    print(response)

if __name__ == "__main__":
    main()