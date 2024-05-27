import os
import boto3
import json
import requests
import time

rds = boto3.client('rds')
redshift = boto3.client('redshift')
sts = boto3.client('sts')

def lambda_handler(event, context):
    try:
        print("\n\nREQUEST RECEIVED FOR ZERO ETL:\n\n  {}".format(json.dumps(event)))
        
        # Extract necessary parameters from the event
        action = event['RequestType']
        
        if action == 'Create':
            print("Creating zero-ETL Integration")
            
            sourceClusterIdentifier = event['ResourceProperties']['source']
            targetClusterName = event['ResourceProperties']['target']
            redshiftIntegrationName = event['ResourceProperties']['integrationName']
            [sourceClusterName , sourceClusterArn] = getRds(sourceClusterIdentifier)
            targetClusterArn = getRedshiftArn(targetClusterName)
            
            print(f"sourceClusterIdentifier: {sourceClusterIdentifier}")
            print(f"source_name: {sourceClusterName}")
            print(f"sourceClusterArn: {sourceClusterArn}")
            print(f"targetClusterName: {targetClusterName}")
            print(f"targetClusterArn: {targetClusterArn}")
            print(f"redshiftIntegrationName: {redshiftIntegrationName}")
            
            targetClusterVerifier(sourceClusterArn=sourceClusterArn, targetClusterArn=targetClusterArn)
            waitForClusterAvailability(sourceClusterName=sourceClusterName , targetClusterName=targetClusterName)
            createIntegration(sourceClusterArn=sourceClusterArn, targetClusterArn=targetClusterArn, redshiftIntegrationName=redshiftIntegrationName)
            
            sendresponse(event, context, "SUCCESS")
        
        elif action == 'Delete':
            print("Deleting zero-ETL Integration")

            redshiftIntegrationName = event['ResourceProperties']['integrationName']
            print(f"deleting Integration: {redshiftIntegrationName}")
            deleteIntegration(redshiftIntegrationName=redshiftIntegrationName)
            sendresponse(event, context, "SUCCESS")
        
        else:
            error_message = 'Unexpected RequestType: {}'.format(action)
            print(error_message)
            sendresponse(event, context, "SUCCESS")
    except Exception as e:
        print("Web Request failed with the error ==> \n\n" + str(e))
        sendresponse(event, context, "FAILED")

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
    
    
def deleteIntegration(redshiftIntegrationName):
    print("Deleting zero ETL Integration")
    
    integrations = rds.describe_integrations( MaxRecords=99 )['Integrations']
    integrationArn = [integration['IntegrationArn'] for integration in integrations if integration['IntegrationName'] == redshiftIntegrationName][0]
    integrationId = integrationArn.split(':')[-1]
    print(f"Integration ID : {integrationId}")
    response = rds.delete_integration( 
        IntegrationIdentifier=integrationId
    )
    print(f"integration delete response: {response}")
    
def createIntegration(sourceClusterArn, targetClusterArn, redshiftIntegrationName):
    """Creates a zero-ETL integration using the source and target clusters"""
    response = rds.create_integration(
        SourceArn=sourceClusterArn,
        TargetArn=targetClusterArn,
        IntegrationName=redshiftIntegrationName
    )
    integrationID = response['IntegrationArn'].split(':')[-1]
    print(f"Zero ETL Integration Created with Integration ID : {integrationID}")
    return response

def targetClusterVerifier(sourceClusterArn, targetClusterArn):
    # Create a resource policy specifying cluster ARN and account ID
    response = sts.get_caller_identity()
    account_id = response['Account']
    response = redshift.put_resource_policy(
        ResourceArn=targetClusterArn,
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
        ''' % (sourceClusterArn, account_id)
    )
    return(response)

def waitForClusterAvailability(sourceClusterName , targetClusterName):
    """Waits for both clusters to be available"""
    print('Waiting for clusters to be available...')
    response = rds.describe_db_clusters(
        DBClusterIdentifier=sourceClusterName,
    )
    sourceStatus = response['DBClusters'][0]['Status']
    response = redshift.describe_clusters(
        ClusterIdentifier=targetClusterName,
    )
    targetStatus = response['Clusters'][0]['ClusterStatus']

    # Every 60 seconds, check whether the clusters are available.
    if sourceStatus != 'available' or targetStatus != 'available':
        print("Either Source or Target Cluster is not in 'Available' Status. Waiting for 60 Seconds")
        time.sleep(60)
        response = waitForClusterAvailability(
            sourceClusterName, targetClusterName)
    else:
        print('\nClusters available. Ready to create zero-ETL integration.\n')
        return

def getRds(rdsIdentifier):
    clusters = rds.describe_db_clusters( MaxRecords=99 )['DBClusters']
    clusterName = [cluster['DBClusterIdentifier'] for cluster in clusters if cluster['DBClusterIdentifier'].startswith(rdsIdentifier)][0]
    clusterArn = [cluster['DBClusterArn'] for cluster in clusters if cluster['DBClusterIdentifier'].startswith(rdsIdentifier)][0]
    return [clusterName , clusterArn]

def getRedshiftArn(targetClusterName):
    response = redshift.describe_clusters( ClusterIdentifier=targetClusterName )
    targetClusterArn = response['Clusters'][0]['ClusterNamespaceArn']
    return targetClusterArn