class UserBannedError(Exception):
    def __init__(self, action: str):
        super().__init__(f"Action '{action}' is not allowed for banned users")
