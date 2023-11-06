import random
import datetime
from fastapi import Request
from loguru import logger
from utils.tools import Tools
from kavenegar import *
from config.configs import config



EXPIRED_TIME = 120  # second


class OtpError(Exception):
    pass


class OtpService:
    def __init__(self, request:Request):
        self.request = request
        self.time_now = Tools.now()

    async def verify_otp(self, mobile, code):
        redis =  self.request.app.state.redis
        sent_code = await redis.get(mobile)
        if str(sent_code) == code:
            Tools.green(text="code verified")
            return True
        Tools.red(text="code mismatch")
        return False
        #raise OtpError("incorrect otp")


    async def send(self, mobile):
        redis =  self.request.app.state.redis
        code = str(random.randint(100000, 999999))
        Tools.red(text=f'{code}')
        # todo : send to automation
        try:
            api = KavenegarAPI(config.KAVENEGAR_ACCESS_KEY)
            params = {
                'receptor': mobile,
                'sender': 2000500666,
                'message': f"{code} \nکد ورود \nکیو پی \(o.O)/",
            }
            response = api.sms_send(params)
            await redis.set(mobile,code,ex=120)
            Tools.green(text="otp sent")
            return True
        except Exception as e:
            logger.exception(e)
            Tools.red(text="otp failed")
            return False

            #
            # api = KavenegarAPI('70544A3264624F757569322B31356144464C34364D4F3643722F6C33416A3243')
            # params = {
            #     'receptor': otp.mobile,
            #     'template': 'loginOTP',
            #     'token': otp.code,
            #     'type': 'sms',  # sms vs call
            # }
            # response = api.verify_lookup(params)
            # cls.update_status(otp, OtpStatus.SEND_TO_USER)