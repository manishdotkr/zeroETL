total = {
    "Integrations": [
        {
            "IntegrationName": "aurora-redshift-integration",
            "SourceArn": "arn:aws:rds:us-west-2:095767269209:cluster:stage-extv-aurora-auroradbcluster-uvxxjak8f3ah",
            "SourceIdentifier": "stage-extv-aurora-auroradbcluster-uvxxjak8f3ah"
        },
        {
            "IntegrationName": "aurora-redshift-integration-2",
            "SourceArn": "arn:aws:rds:us-west-2:095767269209:cluster:stage-extv-testauroradb3-cluster",
            "SourceIdentifier": "stage-extv-testauroradb3-cluster"
        }
    ]
}

old = {
    "Integrations": [
        {
            "IntegrationName": "aurora-redshift-integration",
            "SourceArn": "arn:aws:rds:us-west-2:095767269209:cluster:stage-extv-aurora-auroradbcluster-uvxxjak8f3ah",
            "SourceIdentifier": "stage-extv-aurora-auroradbcluster-uvxxjak8f3ah"
        }
    ]
}

# Find the difference
old_integrations = old["Integrations"]
total_integrations = total["Integrations"]

# Convert lists of dictionaries to sets of tuples for comparison
old_set = set(tuple(integration.items()) for integration in old_integrations)
total_set = set(tuple(integration.items()) for integration in total_integrations)

# Find the difference
difference_set = total_set - old_set

# Convert the set of tuples back to list of dictionaries
difference_list = [dict(integration) for integration in difference_set]

# Create the resulting dictionary
result = {
    "Integrations": difference_list
}

print(result)
