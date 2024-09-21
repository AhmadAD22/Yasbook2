from rest_framework.response import Response

class ResultResponse(Response):

    def __init__(self, data={}, status=200,isSuccess=True,code='',message='',**kwargs):
        data={'data':data}
        data['isSuccess']=isSuccess
        data['code']=code
        data['status']=status
        data['message']=message
        super().__init__(data, status, **kwargs)


    @staticmethod
    def fromResponse(response:Response,isSuccess=True,code='',message='',**kwargs):
        return ResultResponse(response.data,response.status_code,isSuccess,code,message)