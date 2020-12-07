from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# 滑块验证码
from ater_end.libs.geetest import GeetestLib
from login.service import get_user_by_account

pc_geetest_id = "759d5436a6bfe1e0a94d222e9452097b"
pc_geetest_key = "2061a99f3c25e50989a0c04536132953"


class CaptchaAPIView(APIView):
    user_id = 1
    status = False

    def get(self, request):
        username = request.query_params.get("username")
        user = get_user_by_account(username)
        print(user)
        if user is None:
            return Response({'message': '该用户不存在'}, status.HTTP_400_BAD_REQUEST)
        self.user_id = user.id
        print(self.user_id,"*****************", user.id,"*************", 19,user)

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get("geetest_challenge")
        validate = request.data.get("geetest_validate")
        seccode = request.data.get("geetest_seccode")

        if self.user_id:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        print(result)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)
