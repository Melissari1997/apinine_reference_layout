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
from permissions import Permissions


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option("--name", "-n", help="name of the api key", required=True)
@click.option("--org", "-o", help="name of organization owning the key", required=True)
@click.option(
    "--permission",
    "-p",
    help="specify which APIs the key is allowed to invoke. Default is allow all.",
    multiple=True,
    default=[permission.value for permission in Permissions],
    type=click.Choice(choices=[permission.value for permission in Permissions]),
)
@click.option("--description", "-d", help="Optional description", default="")
def generate_key(name: str, org: str, permission: list[str], description: str) -> None:
    """Generate key with provided name, organization, description and set of permissions.

    This creates both an API Gateway key, and an item in a backend DynamoDB table.

    Parameters
    ----------
    name : str
        Name of the API Gateway key to be generated.
    org : str
        Organization of the key to be generated.
    permission : list[str]
        List of resources the generated key will be allowed to access.
    description : str
        Description of the key to be generated.
    """
    apigwkey = ApiGwKeyGenerator()
    dynamodb_repository = DynamoDBKey()

    # "Sanitize input"
    name = name.lower()
    org = org.upper()

    if description is None or description == "":
        description = f"API Key {name} for {org}"

    Key().save_key_and_permission(
        api_key_gen=apigwkey,
        repository=dynamodb_repository,
        name=name,
        description=description,
        permissions=permission,
        organization=org,
    )

    click.echo("Done")


if __name__ == "__main__":
    cli()
