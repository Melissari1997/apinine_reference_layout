import json

from interface import UserDB


class ParamStoreDB(UserDB):
    def __init__(self, client: object, parameter_name: str):
        """Initialize a Parameter Store DB

        Parameters
        ----------
        client : object
            SSM client
        parameter_name : str
            Parameter to fetch, containing the user db
        """
        self.client = client
        self.parameter_name = parameter_name

    @property
    def parameter_value(self) -> str:
        return json.loads(
            self.client.get_parameter(Name=self.parameter_name)["Parameter"]["Value"]
        )

    def query_user(self, id: str) -> dict:
        """Get user information from a parameter in AWS SSM Parameter Store

        Parameters
        ----------
        id : str
            Email of the user to look up

        Returns
        -------
        dict
            User found in the db
        """
        user = next(filter(lambda x: x["email"] == id, self.parameter_value), None)
        return user
