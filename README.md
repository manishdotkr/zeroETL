
---

# CloudFormation Template for Redshift Cluster and Zero ETL Integration

This CloudFormation template (`redsfhift.yaml`) automates the creation of a Redshift cluster along with other necessary resources and triggers a Lambda function to create a zero ETL integration between clusters.

## Template Details:

### Parameters:

- **environment**: Type of environment (e.g., development, production).
- **product**: Type of product or application.
- **service**: Type of service.
- **databaseName**: Name of the Redshift cluster database.
- **nodeType**: Type of node to be provisioned.
- **masterUserName**: Master user account associated with the Redshift cluster.
- **clusterType**: Type of cluster (single-node or multi-node).
- **integrationName**: Name for the zero ETL integration.

### Resources:

- **kmsKey**: AWS KMS Key for Redshift Cluster encryption.
- **kmsAlias**: Alias for the KMS Key.
- **redshiftClusterSubnetGroup**: Subnet group for Redshift cluster.
- **redshiftClusterParameterGroup**: Parameter group for Redshift cluster.
- **redshiftCluster**: Redshift cluster creation.
- **zeroEtlIntegration**: RDS integration resource.

### Outputs:

- **redshiftCluster**: Identifier of the Redshift Cluster.
- **redshiftClusterParameterGroup**: Identifier of Redshift Cluster Parameter Group.
- **redshiftClusterSubnetGroup**: Identifier of Redshift Cluster Subnet Group.
- **kmsKey**: Identifier of KMS Key.

## Reference:

- [AWS::RDS::Integration](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-integration.html)
- []()

---

You can use this template to easily provision Redshift clusters and set up zero ETL integrations in your AWS environment. For detailed instructions on usage and customization, refer to the respective CloudFormation and Lambda function code files.

Feel free to reach out if you have any questions or need further assistance!
