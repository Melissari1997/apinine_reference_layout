"""
1 - Generate API key in API Gateway
2 - Get API key and hash it
3 - Store it in DynamoDB with all the timestamps
4 - Store Permissions
"""
import click
from adapter.api_gw_key import ApiGwKeyGenerator
from adapter.dynamodb import DynamoDBKey
from domain.key import Key


@click.group()
def cli():
    pass


@cli.command()
# @click.option("--hello", default=1, help="number of greetings")
def generate_key():
    apigwkey = ApiGwKeyGenerator()
    dynamodb_repository = DynamoDBKey()

    Key().save_key_and_permission(
        api_key_gen=apigwkey,
        repository=dynamodb_repository,
        name="test-to-be-deleted",
        description="Just testing the code",
        permissions="*",
        organization="TERNA",
    )

    click.echo("Done")


if __name__ == "__main__":
    cli()
