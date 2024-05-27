import requests

url = "https://cloudformation-custom-resource-response-uswest2.s3-us-west-2.amazonaws.com/arn%3Aaws%3Acloudformation%3Aus-west-2%3A095767269209%3Astack/redshift-etl-7/7c1d9810-0c61-11ef-b749-0636901bb73b%7CzeroEtlIntegration%7Cbae1fd46-659d-4921-8341-2b064b0c78f5?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240507T111010Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7199&X-Amz-Credential=AKIA54RCMT6SBOSO7FUF%2F20240507%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Signature=c8cbd55b1c98838bd166c47c7ba4f6d2e0f7494ff45d2bd4466fc44b77b9db0e"
jsonResponseBody = {
    "Status": "SUCCESS",
    "Reason": "See the details in CloudWatch Log Stream: 2024/05/07/[$LATEST]71bc2800840448f49d526fe8f539cfcc",
    "PhysicalResourceId": "zeroEtlIntegration",
    "StackId": "arn:aws:cloudformation:us-west-2:095767269209:stack/redshift-etl-7/7c1d9810-0c61-11ef-b749-0636901bb73b",
    "RequestId": "bae1fd46-659d-4921-8341-2b064b0c78f5",
    "LogicalResourceId": "zeroEtlIntegration"
}
headers = {
        'content-type' : '',
        'content-length' : str(len(jsonResponseBody))
        }
response = requests.put(url, data=jsonResponseBody, headers=headers)

print(response)