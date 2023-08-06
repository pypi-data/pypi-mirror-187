import enum


class MethodName(str, enum.Enum):
    AUTHENTICATE = "public/auth"
    CREATE_ORDER = "private/create-order"
    CLOSE_POSITION = "private/close-position"
    GET_POSITIONS = "private/get-positions"
    CANCEL_ORDER = "private/cancel-order-list"
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"
    GET_OPEN_ORDERS = "private/get-open-orders"
    GET_DEPOSIT_ADDRESS = "private/get-deposit-address"
    USER_BALANCE = "private/user-balance"
    CANCEL_ALL = "private/cancel-all-orders"


__all__ = [
    "MethodName",
]
