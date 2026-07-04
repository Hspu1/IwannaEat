from uuid import UUID


class BaseAppError(Exception):
    message: str = "An unexpected error occurred"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.message
        super().__init__(self.message)


class SafeStartError(BaseAppError):
    message: str = "Application failed to start --> infrastructure is down"


class PostgresNotReachableError(BaseAppError):
    message: str = "PostgreSQL isn't reachable/initialized"


class WhyFuckingRaceConditionError(BaseAppError):
    message: str = """
        RACE CONDITION on REGISTRATION;
        Are yall kiding me?! UUIDv7 must be UNIQUE, how ts even possible?!
    """


class WalletNotFoundError(BaseAppError):
    def __init__(self, user_id: UUID) -> None:
        self.user_id = user_id  # not for everyone
        self.message = "Requested wallet not found"
        super().__init__(self.message)


class WalletBalanceOverflowError(BaseAppError):
    def __init__(self, user_id: UUID) -> None:
        self.user_id = user_id  # not for everyone
        self.message = "Wallet balance limit exceeded"
        super().__init__(self.message)
