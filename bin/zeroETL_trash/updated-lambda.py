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
            
            integrations = event['ResourceProperties']['Integrations']
            targetClusterIdentifier = event['ResourceProperties']['TargetIdentifier']
            targetClusterArn = event['ResourceProperties']['TargetArn']
            print(f"targetClusterName: {targetClusterIdentifier}")
            print(f"targetClusterArn: {targetClusterArn}")

            for integration in integrations:
                sourceClusterIdentifier = integration['SourceIdentifier']
                sourceClusterArn = integration['SourceArn']
                redshiftIntegrationName = integration['IntegrationName']
            
                print(f"Creating Zero-ETL integration: {redshiftIntegrationName}")
                print(f"sourceClusterIdentifier: {sourceClusterIdentifier}")
                print(f"sourceClusterArn: {sourceClusterArn}")
            
                targetClusterVerifier(sourceClusterArn=sourceClusterArn, targetClusterArn=targetClusterArn)
                waitForClusterAvailability(sourceClusterName=sourceClusterIdentifier , targetClusterName=targetClusterIdentifier, noOfTry=1)
                createIntegration(sourceClusterArn=sourceClusterArn, targetClusterArn=targetClusterArn, redshiftIntegrationName=redshiftIntegrationName)
                print(f"Zero ETL Integration Created Successfully with Name: {redshiftIntegrationName}")
            
            sendresponse(event, context, "SUCCESS")
        
        elif action == 'Delete':
            print("Deleting zero-ETL Integration")

            integrations = event['ResourceProperties']['Integrations']
            integrationList = [integration['IntegrationName'] for integration in integrations]

            for redshiftIntegrationName in integrationList:
                print(f"deleting Integration: {redshiftIntegrationName}")
                deleteIntegration(redshiftIntegrationName=redshiftIntegrationName)

            sendresponse(event, context, "SUCCESS")
            print("All Zero ETL Integrations Deleted Successfully")
        elif action == 'Update':
            print("Updating zero-ETL Integration")
            
            targetClusterIdentifier = event['ResourceProperties']['TargetIdentifier']
            targetClusterArn = event['ResourceProperties']['TargetArn']
            print(f"targetClusterName: {targetClusterIdentifier}")
            print(f"targetClusterArn: {targetClusterArn}")

            # Getting list of updated Integrations
            integrations = event['ResourceProperties']['Integrations']
            oldIntegrations = event['OldResourceProperties']['Integrations']
            print(f"total integrations: {integrations}")
            print(f"old integrations: {oldIntegrations}")
            integrationSet = set(tuple(integration.items()) for integration in integrations)
            oldIntegrationSet = set(tuple(integration.items()) for integration in oldIntegrations)
            newIntegrationSet = integrationSet - oldIntegrationSet
            newIntegrations = [dict(integration) for integration in newIntegrationSet]

            for integration in newIntegrations:
                sourceClusterIdentifier = integration['SourceIdentifier']
                sourceClusterArn = integration['SourceArn']
                redshiftIntegrationName = integration['IntegrationName']
            
                print(f"Creating Zero-ETL integration: {redshiftIntegrationName}")
                print(f"sourceClusterIdentifier: {sourceClusterIdentifier}")
                print(f"sourceClusterArn: {sourceClusterArn}")

                targetClusterVerifier(sourceClusterArn=sourceClusterArn, targetClusterArn=targetClusterArn)
                waitForClusterAvailability(sourceClusterName=sourceClusterIdentifier , targetClusterName=targetClusterIdentifier, noOfTry=1)
                createIntegration(sourceClusterArn=sourceClusterArn, targetClusterArn=targetClusterArn, redshiftIntegrationName=redshiftIntegrationName)
                print(f"Zero ETL Integration Created Successfully with Name: {redshiftIntegrationName}")
            
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
    integrationArn = [integration['IntegrationArn'] for integration in integrations if integration['IntegrationName'] == redshiftIntegrationName]
    integrationArn = integrationArn[0] if len(integrationArn) > 0 else None

    if not integrationArn:
        print(f"No Integrations Found with Integration Name:{redshiftIntegrationName}")
        return
    
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

def waitForClusterAvailability(sourceClusterName , targetClusterName, noOfTry):
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
    if ((sourceStatus != 'available' or targetStatus != 'available') and noOfTry<=4):
        print(f"Either Source or Target Cluster is not in 'Available' Status. Waiting for 30 Seconds.\tNumber of Try:{noOfTry}")
        time.sleep(30)
        waitForClusterAvailability(sourceClusterName, targetClusterName, noOfTry+1)
    elif sourceStatus == 'available' and targetStatus == 'available':
        print('\nClusters available. Ready to create zero-ETL integration.\n')
        return
    else:
        raise Exception("Either Source or Target Cluster is not in 'Available' Status and noOftry is Over")

