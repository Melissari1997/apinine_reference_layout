class MissingDataError(Exception):
    pass


class QuerystringInputError(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

    def __repr__(self):
        return f"QuerystringInputError(code={self.code}, msg={self.msg})"
