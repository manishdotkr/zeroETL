import boto3
import time

# Build the client using the default credential configuration.
# You can use the CLI and run 'aws configure' to set access key, secret
# key, and default Region.

rds = boto3.client('rds')
redshift = boto3.client('redshift')
sts = boto3.client('sts')

source_cluster_name = 'stage-extv-testauroradb3-cluster'   # A name for the source cluster
source_param_group_name = 'stage-extv-testAuroraDB-parameterGroup' # A name for the source parameter group
target_cluster_name = 'stage-extv-testRedshift3' # A name for the target cluster
target_param_group_name = 'stage-extv-testRedshift-parameterGroup' # A name for the target parameter group

dbParameterGroupFamilyName='aurora-mysql8.0'

dbEngineName='aurora-mysql'
dbEngineVersion='8.0.mysql_aurora.3.05.2'
databaseName='myauroradb'
databaseUserName='manish' #for both auroraDB and Redshift
databasePassword='Password0123' #for both auroraDB and Redshift

RedshiftIntegrationName='Aurora-Redshift-integration'

dbInstanceClassName='db.t3.medium'
redshiftNodeType='ra3.xlplus'



def create_target_cluster(target_cluster_name, target_param_group_name , source_arn ):
    """Creates a target Redshift cluster"""

    response = redshift.create_cluster(
        ClusterIdentifier=target_cluster_name,
        NodeType=redshiftNodeType,
        NumberOfNodes=2,
        Encrypted=True,
        MasterUsername=databaseUserName,
        MasterUserPassword=databasePassword,
        ClusterParameterGroupName=target_param_group_name
    )
    print('Creating target cluster: ' + response['Cluster']['ClusterIdentifier'])
    
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

    response = rds.describe_db_instances(
        # DBInstanceIdentifier=source_cluster_name + '-instance',
        DBInstanceIdentifier='stage-extv-testauroradb3',
    )
    source_instance_status = response['DBInstances'][0]['DBInstanceStatus']

    response = redshift.describe_clusters(
        ClusterIdentifier=target_cluster_name,
    )
    target_status = response['Clusters'][0]['ClusterStatus']
    target_arn = response['Clusters'][0]['ClusterNamespaceArn']

    # Every 60 seconds, check whether the clusters are available.
    if source_status != 'available' or target_status != 'available' or  source_instance_status != 'available':
        time.sleep(60)
        response = wait_for_cluster_availability(
            source_cluster_name, target_cluster_name)
    else:
        print('Clusters available. Ready to create zero-ETL integration.')
        create_integration(source_arn, target_arn)
        return

def create_integration(source_arn, target_arn):
    """Creates a zero-ETL integration using the source and target clusters"""

    response = rds.create_integration(
        SourceArn=source_arn,
        TargetArn=target_arn,
        IntegrationName=RedshiftIntegrationName
    )
    print('Creating integration: ' + response['IntegrationName'])
    
def main():
    """main function"""
    # sourceClusterARN='arn:aws:rds:us-west-2:095767269209:cluster:stage-extv-testauroradb3-cluster'
    create_target_cluster(target_cluster_name, target_param_group_name , sourceClusterARN)
    wait_for_cluster_availability(source_cluster_name, target_cluster_name)
    
    # source_arn='arn:aws:rds:us-west-2:095767269209:cluster:stage-extv-testauroradb3-cluster'
    # target_arn='arn:aws:redshift:us-west-2:095767269209:namespace:98d2b10c-aa08-48b1-bea6-d8e2b14e137a'
    # create_integration(source_arn, target_arn)

if __name__ == "__main__":
    main()