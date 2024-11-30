from enum import Enum

class MessageType(Enum):
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    REGISTRATION_SUCCESS = "REGISTRATION_SUCCESS"
    MESSAGE_SUCCESS = "MESSAGE_SUCCESS"
    MESSAGE = "MESSAGE"
    ERROR = "ERROR"
    LOGIN = "LOGIN"
    REGISTER = "REGISTER"
    SUCCESS = "SUCCESS"