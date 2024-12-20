class AccountAlreadyExistsException(Exception):
    def __init__(self, message="Account already exists"):
        self.message = message
        super().__init__(self.message)


class AccountNotFoundException(Exception):
    def __init__(self, message="Account not found"):
        self.message = message
        super().__init__(self.message)