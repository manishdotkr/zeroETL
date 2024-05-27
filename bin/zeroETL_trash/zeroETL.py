import boto3
import time

# Build the client using the default credential configuration.
# You can use the CLI and run 'aws configure' to set access key, secret
# key, and default Region.

rds = boto3.client('rds')
redshift = boto3.client('redshift')
sts = boto3.client('sts')

source_cluster_name = 'stage-extv-testauroradb3-cluster' # A name for the source cluster
target_cluster_name = 'stage-extv-redshift-test' # A name for the target cluster
kmsKey = 'b306f45e-e1a8-4794-aaf4-f91911fa9ba2'

RedshiftIntegrationName='Aurora-Redshift-integration-test'

def target_cluster_verifier(target_cluster_name):
    """Creates a target Redshift cluster"""

    response = rds.describe_db_clusters(
        DBClusterIdentifier=source_cluster_name,
    )
    source_arn = response['DBClusters'][0]['DBClusterArn']

    # Retrieve the target cluster ARN
    response = redshift.describe_clusters(
        ClusterIdentifier=target_cluster_name
    )
    target_arn = response['Clusters'][0]['ClusterNamespaceArn']

    # Retrieve the current user's account ID
    response = sts.get_caller_identity()
    account_id = response['Account']

    # Create a resource policy specifying cluster ARN and account ID
    response = redshift.put_resource_policy(
        ResourceArn=target_arn,
        Policy='''
        {
            \"Version\":\"2012-10-17\",
            \"Statement\":[
                {\"Effect\":\"Allow\",
                \"Principal\":{
                    \"Service\":\"redshift.amazonaws.com\"
                },
                \"Action\":[\"redshift:AuthorizeInboundIntegration\"],
                \"Condition\":{
                    \"StringEquals\":{
                        \"aws:SourceArn\":\"%s\"}
                    }
                },
                {\"Effect\":\"Allow\",
                \"Principal\":{
                    \"AWS\":\"arn:aws:iam::%s:root\"},
                \"Action\":\"redshift:CreateInboundIntegration\"}
            ]
        }
        ''' % (source_arn, account_id)
    )
    return(response)

def wait_for_cluster_availability(*args):
    """Waits for both clusters to be available"""

    print('Waiting for clusters to be available...')

    response = rds.describe_db_clusters(
        DBClusterIdentifier=source_cluster_name,
    )
    source_status = response['DBClusters'][0]['Status']
    source_arn = response['DBClusters'][0]['DBClusterArn']

    response = redshift.describe_clusters(
        ClusterIdentifier=target_cluster_name,
    )
    target_status = response['Clusters'][0]['ClusterStatus']
    target_arn = response['Clusters'][0]['ClusterNamespaceArn']

    # Every 60 seconds, check whether the clusters are available.
    if source_status != 'available' or target_status != 'available':
        time.sleep(60)
        response = wait_for_cluster_availability(
            source_cluster_name, target_cluster_name)
    else:
        print('\nClusters available. Ready to create zero-ETL integration.\n')
        create_integration(source_arn, target_arn, kmsKey)
        return

def create_integration(source_arn, target_arn, kmsKey):
    """Creates a zero-ETL integration using the source and target clusters"""

    response = rds.create_integration(
        SourceArn=source_arn,
        TargetArn=target_arn,
        # KMSKeyId=kmsKey,
        IntegrationName=RedshiftIntegrationName
    )
    print(f'Integration---------------> {response}')
    print('Creating integration: ' + response['IntegrationArn'])
    print(f" integration ID : {response['IntegrationArn'].split(':')[-1]}")
    
def main():
    """main function"""
    target_cluster_verifier(target_cluster_name)
    wait_for_cluster_availability(source_cluster_name, target_cluster_name)

if __name__ == "__main__":
    main()