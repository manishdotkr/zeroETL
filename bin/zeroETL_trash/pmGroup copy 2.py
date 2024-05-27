import boto3
import time

# Build the client using the default credential configuration.
# You can use the CLI and run 'aws configure' to set access key, secret
# key, and default Region.

rds = boto3.client('rds')
redshift = boto3.client('redshift')
sts = boto3.client('sts')

source_cluster_name = 'stage-extv-testAuroraDB' # A name for the source cluster
source_param_group_name = 'stage-extv-testauroradb-instance-parametergroup' # A name for the source parameter group
target_cluster_name = 'stage-extv-testRedshift' # A name for the target cluster
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

def create_source_cluster(*args):
    """Creates a source Aurora MySQL DB cluster"""

    response = rds.modify_db_parameter_group(
        DBParameterGroupName=source_param_group_name,
        Parameters=[
            {
                'ParameterName': 'aurora_enhanced_binlog',
                'ParameterValue': '1',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'binlog_backup',
                'ParameterValue': '0',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'binlog_format',
                'ParameterValue': 'ROW',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'binlog_replication_globaldb',
                'ParameterValue': '0',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'binlog_row_image',
                'ParameterValue': 'full',
                'ApplyMethod': 'pending-reboot'
            },
            {
                'ParameterName': 'binlog_row_metadata',
                'ParameterValue': 'full',
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