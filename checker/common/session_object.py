import time

class SessionObject:
    #in seconds
    SESSION_TIMEOUT_IN_SECONDS = 590

    def __init__(self):
        self.login=''
        self.cookies=''
        self.token=''
        self.created_at=time.time()
        self.session_timeout = self.SESSION_TIMEOUT_IN_SECONDS
        self.is_good = False

    def to_array(self):
        arr=[]
        arr.append(self.login)
        arr.append(self.cookies)
        arr.append(self.token)
        arr.append(self.created_at)
        arr.append(self.session_timeout)

        return arr

    def to_string(self):
        return '!'.join(filter(None, self.to_array()))

    def is_good(self):
        return self.is_good()

    def is_active(self):
        if self.cookies and self.token:
            current = time.time()
            elapsed = current - self.created_at
            if elapsed <= self.session_timeout:
                return True
        return False

    @staticmethod
    def to_header_array():
        arr =[]
        arr.append('login')
        arr.append('cookies')
        arr.append('token')
        arr.append('created_at')
        arr.append('session_timeout')

        return arr