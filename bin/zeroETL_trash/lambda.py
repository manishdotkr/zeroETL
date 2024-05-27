
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

def sendresponse(event, context, status, integrationID):
    try:
        url = event['ResponseURL']
        print(url)
        responseBody = {}
        responseBody['Status'] = status
        responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
        responseBody['PhysicalResourceId'] = event['LogicalResourceId']
        responseBody['StackId'] = event['StackId']
        responseBody['RequestId'] = event['RequestId']
        responseBody['LogicalResourceId'] = event['LogicalResourceId']
        responseBody['Data'] = {
            "integrationID": integrationID
        }

        jsonResponseBody = json.dumps(responseBody)
        print("Response body:\n" + jsonResponseBody)
        headers = {
        'content-type' : '',
        'content-length' : str(len(jsonResponseBody))
        }
        return requests.put(url, data=jsonResponseBody, headers=headers)
    except Exception as e:
        print("Web Request failed with the error ==> \n\n" + str(e))

def handler(event, context):
    try:
        print("\n\nREQUEST RECEIVED:\n\n  {}".format(json.dumps(event)))
        elbv2 = boto3.client('elbv2')
        print("\n\nELBV2 Client Initialized Successfully\n\n")
        listenerRuleArns=event['ResourceProperties']['listenerRuleArn']
        ruleArnsLength = len(event['ResourceProperties']['listenerRuleArn'])
        print("\n\nHere is the Length of Rule Count >> {}\n\n".format(ruleArnsLength))
        rules = elbv2.describe_rules(RuleArns=listenerRuleArns)['Rules'][0]
        print("\n\nThe Listener Rule was fetched successfully!!!!\n\n")           
        if event['RequestType'] == 'Create':
            greenTargetGroupConfig = {
                'TargetGroupArn': event['ResourceProperties']['targetGroupArn'],
                'Weight': int(event['ResourceProperties']['targetGroupWeight'])
            }
            forwardConfig = rules['Actions'][0]['ForwardConfig']
            forwardConfig['TargetGroups'].append(greenTargetGroupConfig.copy())
            print("\n\nRule Params created successfully and they are ==> {}\n\n".format(json.dumps(rules)))
            print("\n\nForwardConfig are ==> {}\n\n".format(forwardConfig))
            for count in range(ruleArnsLength):    
                createListenerRule=event['ResourceProperties']['listenerRuleArn'][count]
                print("\n\n listnerRule Value >> {}".format(createListenerRule))
                createResponse = elbv2.modify_rule(RuleArn=createListenerRule,Actions=[{'Type': 'forward', 'ForwardConfig': forwardConfig},])
                print("\n\nListener Rule Modified and here is the response:\n\n {}".format(json.dumps(createResponse)))
        elif event['RequestType'] == 'Delete':
            tgCount = len(rules['Actions'][0]['ForwardConfig']['TargetGroups'])
            if tgCount == 2:
                for i in range(tgCount):
                    if rules['Actions'][0]['ForwardConfig']['TargetGroups'][i]['TargetGroupArn'] != event['ResourceProperties']['targetGroupArn'] :
                        blueTargetGroupArn = rules['Actions'][0]['ForwardConfig']['TargetGroups'][i]['TargetGroupArn']
                blueTargetGroupConfig = {
                    'TargetGroupArn': blueTargetGroupArn,
                    'Weight': 100
                }
                print("\n\nThe Blue Target Group Arn Is ==> {}\n\n".format(json.dumps(blueTargetGroupArn)))
                forwardConfig = rules['Actions'][0]['ForwardConfig']
                rules['Actions'][0]['ForwardConfig']['TargetGroups'] = []
                forwardConfig['TargetGroups'].append(blueTargetGroupConfig.copy())
                print("\n\nForwardConfig are ==> {}\n\n".format(forwardConfig))
                for count in range(ruleArnsLength):
                    delListenerRule=event['ResourceProperties']['listenerRuleArn'][count]
                    modifiedRule = elbv2.modify_rule(RuleArn=delListenerRule, Actions=[{'Type': 'forward', 'ForwardConfig': forwardConfig},])
                    print("\n\nThe Blue Target Group Has Been Modified and the final config is ==> {}\n\n".format(json.dumps(rules['Actions'][0]['ForwardConfig']['TargetGroups'])))
            elif tgCount == 1:
                modifyRule = elbv2.modify_rule(
                    RuleArn=event['ResourceProperties']['listenerRuleArn'],
                    Actions=[
                        {
                            'Type': 'forward',
                            'ForwardConfig': {
                                'TargetGroups': [
                                    {
                                        'TargetGroupArn': event['ResourceProperties']['defaultTargetGroupArn'],
                                        'Weight': 100
                                    },
                                ]
                            }   
                        },
                    ]      
                )
                print("\n\nListener Rule Modified and here is the response: {}\n\n".format(json.dumps(modifyRule)))
        else:
            return print(f"\n\n Unrecognized event : {event['RequestType']}")
        status = "SUCCESS"; 
        response = sendresponse(event, context, status);
        print(f"\n\n Lambda Executed Successfully and here is the response: {response}\n\n ")
    except Exception as e:
        status = "FAILED";
        response = sendresponse(event, context, status);            
        print(f"\n\n Lambda Execution Failed and here is the response: {response}\n\n " + str(e))

