import boto3
import time

# Build the client using the default credential configuration.
# You can use the CLI and run 'aws configure' to set access key, secret
# key, and default Region.

rds = boto3.client('rds')
redshift = boto3.client('redshift')
sts = boto3.client('sts')

source_cluster_name = 'stage-extv-testAuroraDB' # A name for the source cluster
# source_param_group_name = 'stage-extv-testAuroraDB-parameterGroup' # A name for the source parameter group
source_param_group_name = 'stage-extv-testauroradb-parametergroup'
target_cluster_name = 'stage-extv-testRedshift' # A name for the target cluster
target_param_group_name = 'stage-extv-testRedshift-parameterGroup' # A name for the target parameter group

dbParameterGroupFamilyName='aurora-mysql8.0'

def create_source_cluster(*args):
    """Creates a source Aurora MySQL DB cluster"""

    response = rds.modify_db_cluster_parameter_group(
        DBClusterParameterGroupName=source_param_group_name,
        Parameters=[
            {
                'ParameterName': 'character_set_client',
                'ParameterValue': 'utf8',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'character_set_connection',
                'ParameterValue': 'utf8',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'character_set_database',
                'ParameterValue': 'utf8',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'character_set_filesystem',
                'ParameterValue': 'utf8',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'character_set_results',
                'ParameterValue': 'utf8',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'character_set_server',
                'ParameterValue': 'utf8',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'collation_connection',
                'ParameterValue': 'utf8_general_ci',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'collation_server',
                'ParameterValue': 'utf8_general_ci',
                'ApplyMethod': 'pending-reboot'
            }
        ]
    )
    print('Modified source parameter group: ' + response['DBClusterParameterGroupName'])
    

def main():
    """main function"""
    create_source_cluster(source_cluster_name, source_param_group_name)

if __name__ == "__main__":
    main()