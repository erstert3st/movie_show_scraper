class videoBroken(Exception):
    def __str__(self):
        return "File is not online"
class botDetection(Exception):
    def __str__(self):
        return "File is not online"
class captchaLock(Exception):
    def __str__(self):
        return "To many request try again later"
