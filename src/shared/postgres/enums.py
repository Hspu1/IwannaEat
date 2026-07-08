from enum import IntEnum


class TopUpStatus(IntEnum):
    PENDING = 1
    SUCCEEDED = 2
    FAILED = 3


class OrderStatus(IntEnum):
    CREATED = 1
    COOKING = 2
    DELIVERING = 3
    COMPLETED = 4
    CANCELLED = 5


class OutboxEventType(IntEnum):
    HOLD_FUNDS_REQUESTED = 1
