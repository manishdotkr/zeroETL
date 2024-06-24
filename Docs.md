## Docs
### [Getting started with Aurora zero-ETL integrations with Amazon Redshift](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/zero-etl.setting-up.html)
### [Creating an Amazon Aurora DB cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.CreateInstance.html)
### [Managing clusters using the console](https://docs.aws.amazon.com/redshift/latest/mgmt/managing-clusters-console.html#create-cluster)
### [Working with Aurora zero-ETL integrations with Amazon Redshift](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/zero-etl.html)
### [Supported Regions and Aurora DB engines for zero-ETL integrations with Amazon Redshift](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.Aurora_Fea_Regions_DB-eng.Feature.Zero-ETL.html)
### [Zero-ETL Pricing](https://aws.amazon.com/rds/aurora/zero-etl/#:~:text=AWS%20does%20not%20charge%20an%20additional%20fee%20for%20Aurora%20zero%2DETL%20integration%20with%20Amazon%20Redshift.%20You%20pay%20for%20existing%20Aurora%20and%20Amazon%20Redshift%20resources%20used%20to%20create%20and%20process%20the%20change%20data%20generated%20as%20part%20of%20a%20zero%2DETL%20integration.%20These%20resources%20could%20include%3A)
### [Using change data capture](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.SQLServer.CommonDBATasks.CDC.html)
### [How Amazon Redshift uses AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/services-redshift.html)
### [redshift-cluster-kms-enabled](https://docs.aws.amazon.com/config/latest/developerguide/redshift-cluster-kms-enabled.html)


## ETL Working
### PPT [Getting Started with Amazon Aurora Zero-ETL Integration with Amazon Redshift](https://pages.awscloud.com/rs/112-TZM-766/images/2023_SN-1009-DAT_Slide-Deck.pdf)
### YT [Getting started with Amazon Aurora zero-ETL integration with Amazon Redshift - AWS Databases in 15] (https://www.youtube.com/watch?v=LAPojOGLXTM)
### YT [Change Data Capture (CDC) Explained (with examples)](https://www.youtube.com/watch?v=5KN_feUhtTM)
### YT [Amazon Aurora MySQL Zero-ETL Integration with Amazon Redshift Public Preview Demo](https://www.youtube.com/watch?v=FO3CbhTiMTU)
### YT [AWS Tutorial - Zero ETL - Overview](https://www.youtube.com/watch?v=ZgLWHrT5CGA)
### YT [How to Create Redshift Cluster and Load Data | Cloud series - Part 6](https://www.youtube.com/watch?v=tqXo-7lNguk)

## aws price calculate
### [Amazon Redshift pricing](https://aws.amazon.com/redshift/pricing/)
### [Create estimate: Configure Amazon Redshift](https://calculator.aws/#/createCalculator/Redshift)

## Cloudformations
### [AWS::RDS::Integration](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html)
### [AWS::Redshift::Cluster](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-namespaceresourcepolicy)
### [AWS::Redshift::ClusterSubnetGroup](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html)
### [AWS::KMS::Key](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keypolicy)
### [AWS::RDS::DBInstance](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbinstance.html)

## Boto3 client
### [describe_clusters](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift/client/describe_clusters.html)
### [describe_db_clusters](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/describe_db_clusters.html)
### [describe_integrations](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/describe_integrations.html)
### [get_key_policy](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_key_policy.html)


---
### Note -> for passing value from lambda. inside "responseBody" create an object named "Data" and add key Value Pair in it...
### Refer below Code Snippet
```
exports.handler = async (event, context) => {
    let sendresponse = async (event, context, status, secret) => {
        let responseBody = {
            "Status": status,
            "Reason": `See the details in CloudWatch Log Stream at ${context.logStreamName}`,
            "PhysicalResourceId": event.LogicalResourceId,
            "StackId": event.StackId,
            "RequestId": event.RequestId,
            "LogicalResourceId": event.LogicalResourceId,
            "Data": {
                "NAME" : "Manish"
            }
        };
        console.log("\n\nRESPONSE BODY:\n\n" + JSON.stringify(responseBody));
        let url = event.ResponseURL;
        let headers = {
            "Content-Type": "",
            "Content-Length": responseBody.length
        };
        return await web.put(url, headers, responseBody);
    };
}
```
```
Resources:
  MyCustomResource:
    Type: Custom::MyCustomResource
    Properties:
      ServiceToken: arn:aws:lambda:us-west-2:{AccountID}:function:{Lambda_fuction_name}
      InputParameter1: before
      InputParameter2: after

Outputs:
  MyCustomOutput:
    Value: !GetAtt MyCustomResource.NAME
```
