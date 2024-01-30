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
@click.option("--name", help="name of the api key", required=True)
@click.option("--org", help="name of organization owning the key", required=True)
def generate_key(name, org):
    apigwkey = ApiGwKeyGenerator()
    dynamodb_repository = DynamoDBKey()

    # "Sanitize input"
    name = name.lower()
    org = org.upper()

    Key().save_key_and_permission(
        api_key_gen=apigwkey,
        repository=dynamodb_repository,
        name=name,
        description=f"API Key {name} for {org}",
        permissions="*",
        organization=org,
    )

    click.echo("Done")


if __name__ == "__main__":
    cli()
