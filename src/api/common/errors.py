class MissingDataError(Exception):
    pass


class QuerystringInputError(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

    def __repr__(self):
        return f"QuerystringInputError(code={self.code}, msg={self.msg})"


class InvalidYearError(Exception):
    def __init__(self, valid_years: list):
        self.msg = self.__format_years_list__(valid_years)

    def __format_years_list__(self, years: list):
        if not years:
            return "No years available"
        if len(years) == 1:
            return f"year must be {years[0]}"
        return f"year must be one of {', '.join(map(str, years[:-1]))}, or {years[-1]}"


class BandNotFoundError(Exception):
    pass
