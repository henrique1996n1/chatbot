from rest_framework import status


class Error():
    '''Class used to mapping all possible errors returned by the API endpoints'''
    INVALID_REQUEST_PARAMETER = {"status_code": status.HTTP_400_BAD_REQUEST,
                               "error": "bad_request",
                               "reason": ""
                               }

    USER_NOT_FOUND = {"status_code": status.HTTP_404_NOT_FOUND,
                      "error": "not_found",
                      "message": "Users not found"
                     }

    COUPON_NOT_FOUND = {"status_code": status.HTTP_404_NOT_FOUND,
                      "error": "not_found",
                      "message": "Promotional coupon id not found"
                     }

    MESSAGE_NOT_FOUND = {"status_code": status.HTTP_404_NOT_FOUND,
                      "error": "not_found",
                      "message": "Message id not found"
                     }

    INTERNAL_SERVER_ERROR = {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                             "error": "internal_server_error",
                             "message": "Sorry, there was an error while processing your request. Please try again later."
                             }