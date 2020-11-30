class MissingTeachableError(Exception):
    pass

class NoThAuthMethodError(Exception):
    pass

class UnsuccessfulRequestError(Exception):
    def __init__(self, code, text, message):
        self.code = code
        self.text = text
        self.message = message
        super().__init__(self.message)

class UnauthorizedError(Exception):
    pass
