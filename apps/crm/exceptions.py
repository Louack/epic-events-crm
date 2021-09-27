from rest_framework import status
from rest_framework.exceptions import APIException


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found'


class EventAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'An event already exists for this contract'
