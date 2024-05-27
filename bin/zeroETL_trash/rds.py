
import boto3

rds = boto3.client('rds')

clusters = rds.describe_db_clusters(
    MaxRecords=99
)['DBClusters']

cluster = [cluster['DBClusterIdentifier'] for cluster in clusters if cluster['DBClusterIdentifier'].startswith("stage-extv-aurora")][0]
print(cluster)