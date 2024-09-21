from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.exceptions import APIException,ValidationError
from django.http import Http404
from .responses import ResultResponse
from rest_framework.views import exception_handler
from utils.app_loggers import errorsLogger
import traceback
class ErrorResult(APIException):

    def __init__(self, message='error occurred', code="ERROR",status=400):
        self.default_detail=message
        self.default_code=code
        self.status_code=status
        super().__init__(message, code)

    @classmethod
    def serverError(cls):
        return cls('server error','SERVER_ERROR',500)

def exceptionsHandler(exc,context):
    if not exception_handler(exc,context) is None:
        if type(exc)==Http404:
            return ResultResponse(status=404,message='not found',code= 'NOT_FOUND',isSuccess=False)
        if not exc.status_code==500:
            if type(exc)==ValidationError:
                msg=exc.default_detail
                print(type(exc.detail))

                if type(exc.detail) is ReturnDict:
                    msg=list(exc.detail.values())[0][0]
                return ResultResponse(data=exc.detail,status=exc.status_code,message=msg,code= exc.default_code,isSuccess=False)
            return ResultResponse(status=exc.status_code,message=exc.default_detail,code= exc.default_code,isSuccess=False)

    print(f'{exc} {traceback.format_exception(exc)}')
    errorsLogger.error(f'{exc} {traceback.format_exception(exc)}')
    return ResultResponse(status=500,message='server error',code= "SERVER_ERROR",isSuccess=False)

    