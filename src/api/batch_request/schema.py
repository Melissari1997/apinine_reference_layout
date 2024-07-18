from common.input_schema import QueryParameterSchema, RiskInputSchema
from common.status_codes import StatusCodes
from pydantic import BaseModel, conlist

BATCH_MAX_SIZE = 50


class BatchRequestLinksSchema(BaseModel):
    status: str
    # cancel: HttpUrl


class BatchRequestOutputSchema(BaseModel):
    id: str
    links: BatchRequestLinksSchema


class BatchRequestBodySchema(QueryParameterSchema):
    locations: conlist(RiskInputSchema, min_length=1, max_length=BATCH_MAX_SIZE)

    @staticmethod
    def get_error_msg() -> str:
        return StatusCodes.BATCH_REQUEST_INVALID_BODY[1]


# TODO: add this as refactoring

# class BatchRequestSchema(RequestSchema):
#     body: Json[BatchBodySchema]

#     @staticmethod
#     def get_error_msg() -> str:
#         return StatusCodes.BATCH_REQUEST_INVALID_BODY[1]
