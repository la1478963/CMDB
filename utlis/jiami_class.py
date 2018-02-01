import hashlib

class jiami(object):
    def encrypt(self,pwd):
        obj=hashlib.md5()
        obj.update(pwd.encode('utf-8'))
        data=obj.hexdigest()
        return data


