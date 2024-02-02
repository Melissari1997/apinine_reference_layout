import boto3


def init_populated_dynamodb(create_table_query, create_write_batch_query):
    client = boto3.client("dynamodb")
    client.create_table(**create_table_query)
    client.batch_write_item(**create_write_batch_query)
