from main import handler
from moto import mock_aws
from tests.common import init_populated_dynamodb


class ContextMock:
    def __init__(self) -> None:
        self.function_name = "lambda_handler"
        self.memory_limit_in_mb = 512
        self.invoked_function_arn = "ARN"
        self.aws_request_id = "111111111111"


class TestMain:
    def test_handler_valid_permission(
        self, create_table_query, create_write_batch_query
    ):
        with mock_aws():
            init_populated_dynamodb(create_table_query, create_write_batch_query)
            ctx = ContextMock()
            path = "/drought"
            method_arn = f"arn:aws:execute-api:eu-central-1:accountid:apigwid/apigwstage/GET{path}"
            event = {
                "headers": {"x-api-key": "user:secret"},
                "httpMethod": "GET",
                "methodArn": method_arn,
                "requestContext": {"path": path},
            }

            want = {
                "principalId": "user",
                "policyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Action": "execute-api:Invoke",
                            "Effect": "Allow",
                            "Resource": [method_arn],
                        }
                    ],
                },
            }

            got = handler(event=event, context=ctx)
            assert got == want

    def test_handler_invalid_permission_path(
        self, create_table_query, create_write_batch_query
    ):
        with mock_aws():
            init_populated_dynamodb(create_table_query, create_write_batch_query)
            ctx = ContextMock()
            path = "/random/path"
            method_arn = f"arn:aws:execute-api:eu-central-1:accountid:apigwid/apigwstage/GET{path}"
            event = {
                "headers": {"x-api-key": "user:secret"},
                "httpMethod": "GET",
                "methodArn": method_arn,
                "requestContext": {"path": path},
            }

            want = {
                "principalId": "user",
                "policyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Action": "execute-api:Invoke",
                            "Effect": "Allow",
                            "Resource": [],
                        }
                    ],
                },
            }

            got = handler(event=event, context=ctx)
            assert got == want

    def test_handler_wrong_key(self):
        assert 1 == 3
