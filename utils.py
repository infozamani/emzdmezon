
def create_random_code(count):
    import random
    count -=1
    return random.randint(10**count,10**(count+1)-1)
#-----------------------------------------------------------
# from kavenegar import *
def send_sms (mobile_number,message):
    pass
    # try:
    #     api = KavenegarAPI('30444D474A55744A6C3771636450346767742B766F565A41476B74573242707849497268444B315A5448773D')
    #     params = { 'sender' : '1000689696', 'receptor': mobile_number, 'message' :message }
    #     response = api.sms_send( params)
    #     response = api.sms_sendarray(params)
    #     print(response)
    # except APIException as error: 
    #     print(f"error1:{error}")
    # except HTTPException as error: 
    #     print(f"error2:{error}")
#-----------------------------------------------------------
## creat class for image upload_to all models
import os
from uuid import uuid4#یرای جلوگیری از تکرار فایل های مشابه UUID4
class FileUpload :
    def __init__(self, dir, prefix) -> None:
        self.dir = dir
        self.prefix = prefix
    def upload_to(self, instance, filename) :
        filename, ext = os.path.splitext(filename)
        return f"{self.dir}/{self.prefix}/{uuid4()}{ext}"