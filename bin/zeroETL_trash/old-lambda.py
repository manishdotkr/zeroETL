
import os
import boto3
import json
import requests
import string
import random
import boto3
import time

rds = boto3.client('rds')
redshift = boto3.client('redshift')
sts = boto3.client('sts')
kms = boto3.client('kms')

def lambda_handler(event, context):
    try:
        print("\n\nREQUEST RECEIVED FOR ZERO ETL:\n\n  {}".format(json.dumps(event)))
        
        # Extract necessary parameters from the event
        request_type = event['RequestType']
        resource_properties = event['ResourceProperties']
        
        if request_type == 'Create':
            print("Creating Integration")
            
            sourceClusterIdentifier = event['ResourceProperties']['source']
            targetClusterName = event['ResourceProperties']['target']
            redshiftIntegrationName = event['ResourceProperties']['integrationName']
            kmsKey = event['ResourceProperties']['kmsKey']
            [sourceClusterName , sourceClusterArn] = getRds(sourceClusterIdentifier)
            target_arn = redshift.describe_clusters( ClusterIdentifier=targetClusterName )['Clusters'][0]['ClusterNamespaceArn']
            
            print(f"sourceClusterIdentifier: {sourceClusterIdentifier}")
            print(f"source_name: {sourceClusterName}")
            print(f"source_arn: {sourceClusterArn}")
            print(f"targetClusterName: {targetClusterName}")
            print(f"target_arn: {target_arn}")
            print(f"redshiftIntegrationName: {redshiftIntegrationName}")
            print(f"kmsKey: {kmsKey}")
            
            target_cluster_verifier(source_arn=sourceClusterArn, target_arn=target_arn)
            wait_for_cluster_availability(source_cluster_name=sourceClusterName , target_cluster_name=targetClusterName)
            create_integration(source_arn=sourceClusterArn, target_arn=target_arn, RedshiftIntegrationName=redshiftIntegrationName , kmsKey=kmsKey)
            
            sendresponse(event, context, "SUCCESS")
        
        elif request_type == 'Delete':
            print("Deleting Integration Integration")
            
            # sourceClusterName = event['ResourceProperties']['source']
            # print(f"sourceClusterName: {sourceClusterName}")
            
            # targetClusterName = event['ResourceProperties']['target']
            # print(f"targetClusterName: {targetClusterName}")
            
            # redshiftIntegrationName = event['ResourceProperties']['integrationName']
            # print(f"redshiftIntegrationName: {redshiftIntegrationName}")
            
            # kmsAlias = event['ResourceProperties']['kmsAlias']
            # print(f"kmsAlias: {kmsAlias}")
    
            # kmsKeyId = getKmsKeyId(kmsAlias)
            # print(f"kmsKeyId: {kmsKeyId}")
            
            # source_arn = rds.describe_db_clusters( DBClusterIdentifier=sourceClusterName )['DBClusters'][0]['DBClusterArn']
            # print(f"source_arn: {source_arn}")
            
            # target_arn = redshift.describe_clusters( ClusterIdentifier=targetClusterName )['Clusters'][0]['ClusterNamespaceArn']
            # print(f"target_arn: {target_arn}")
            delete_integration()
            sendresponse(event, context, "SUCCESS")
        
        else:
            error_message = 'Unexpected RequestType: {}'.format(request_type)
            sendresponse(event, context, "FAILED")
    except Exception as e:
        print("Web Request failed with the error ==> \n\n" + str(e))
        sendresponse(event, context, "SUCCESS")
        # sendresponse(event, context, "FAILED")

def sendresponse(event, context, status):
    try:
        url = event['ResponseURL']
        print(f"ResponseURL : {url}")
        responseBody = {}
        responseBody['Status'] = status
        responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
        responseBody['PhysicalResourceId'] = event['LogicalResourceId']
        responseBody['StackId'] = event['StackId']
        responseBody['RequestId'] = event['RequestId']
        responseBody['LogicalResourceId'] = event['LogicalResourceId']

        jsonResponseBody = json.dumps(responseBody)
        print("Response body:\n" + jsonResponseBody)
        headers = {
        'content-type' : '',
        'content-length' : str(len(jsonResponseBody))
        }
        return requests.put(url, data=jsonResponseBody, headers=headers)
    except Exception as e:
        print("Web Request failed with the error ==> \n\n" + str(e))
    
    
def delete_integration():
    print("deleting the zero ETL integration")
    
    integrations = rds.describe_integrations( MaxRecords=99 )['Integrations']

    integrationArn = [integration['IntegrationArn'] for integration in integrations if integration['IntegrationName'] == 'aurora-redshift-integration' ][0]
    integrationId = integrationArn.split(':')[-1]
    print(f"Integration ID : {integrationId}")
    response = rds.delete_integration( IntegrationIdentifier=integrationId)
    print(f"integration delete response: {response}")
    
def create_integration(source_arn, target_arn, RedshiftIntegrationName , kmsKey):
    """Creates a zero-ETL integration using the source and target clusters"""

    response = rds.create_integration(
        SourceArn=source_arn,
        TargetArn=target_arn,
        # KMSKeyId=kmsKey,
        IntegrationName=RedshiftIntegrationName
    )
    
    integrationID = response['IntegrationArn'].split(':')[-1]
    
    print(f'Integration Response: {response}')
    print(f"Integration ID : {integrationID}")
    return response

def target_cluster_verifier(source_arn, target_arn):
    """Creates a target Redshift cluster"""

    # response = rds.describe_db_clusters(
    #     DBClusterIdentifier=source_cluster_name,
    # )
    # source_arn = response['DBClusters'][0]['DBClusterArn']

    # # Retrieve the target cluster ARN
    # response = redshift.describe_clusters(
    #     ClusterIdentifier=target_cluster_name
    # )
    # target_arn = response['Clusters'][0]['ClusterNamespaceArn']

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

def wait_for_cluster_availability(source_cluster_name , target_cluster_name):
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
        print("Either Source or Target Cluster is not in 'Available' Status. Waiting for 60 Seconds")
        time.sleep(60)
        response = wait_for_cluster_availability(
            source_cluster_name, target_cluster_name)
    else:
        print('\nClusters available. Ready to create zero-ETL integration.\n')
        return


def getRds(rdsIdentifier):
    clusters = rds.describe_db_clusters( MaxRecords=99 )['DBClusters']
    clusterName = [cluster['DBClusterIdentifier'] for cluster in clusters if cluster['DBClusterIdentifier'].startswith(rdsIdentifier)][0]
    clusterArn = [cluster['DBClusterArn'] for cluster in clusters if cluster['DBClusterIdentifier'].startswith(rdsIdentifier)][0]
    return [clusterName , clusterArn]
