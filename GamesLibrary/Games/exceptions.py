from rest_framework.exceptions import APIException
from rest_framework import status

# Custom exceptions (never used)

class PublisherIDNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Publisher with given ID not found.'
    default_code = 'not_found'


class GameIDNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Game with given ID not found.'
    default_code = 'not_found'
    