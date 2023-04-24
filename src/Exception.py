class videoBroken(Exception):
    def __str__(self):
        return "File is not online"
class linkBroken(Exception):
    def __str__(self):
        return "File is not online"
class botDetection(Exception):
    def __str__(self):
        return "bot is found"
class streamKisteSearchError(Exception):
    def __str__(self):
        return "bot is found"
class invalidImdb(Exception):
    def __str__(self):
        return "bot is found"    
class captchaLock(Exception):
    def __str__(self):
        return "To many request try again later"
class searchError(Exception):
    def __str__(self):
        return "bot is found"
class notAvailableError(Exception):
    def __str__(self):
        return "bot is found"