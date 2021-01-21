import time

class SessionObject:
    #in seconds
    LOGIN_EXPIRE_IN_SECONDS = 3600
    TOKEN_EXPIRE_IN_SECONDS = 600

    def __init__(self):
        self.created_at = time.time()
        self.login=''
        self.cookies_raw = None
        self.cookies=''
        self.token=''
        self.login_created_at=None
        self.token_created_at=None
        self.login_expires = self.LOGIN_EXPIRE_IN_SECONDS
        self.token_expires = self.TOKEN_EXPIRE_IN_SECONDS

    def to_array(self):
        arr=[]
        arr.append(self.created_at)
        arr.append(self.login)
        arr.append(self.cookies_raw)
        arr.append(self.cookies)
        arr.append(self.login_created_at)
        arr.append(self.login_expires)
        arr.append(self.token)
        arr.append(self.token_created_at)
        arr.append(self.token_expires)

        return arr

    def set_login(self, login):
        self.login = login

    def set_cookies_raw(self, cookies_raw):

        self.cookies_raw = cookies_raw

        cookie_list = []
        for cookie in cookies_raw:
            cookie_list.append(f"{cookie['name']}={cookie['value']}")
        cookie_str = '; '.join(cookie_list)

        self.cookies = cookie_str
        self.login_created_at = time.time()

    def set_token(self, token):
        self.token = token
        self.token_created_at = time.time()

    def to_string(self):
        return '!'.join(filter(None, self.to_array()))

    def is_active(self):
        if self.is_token_active() and self.is_login_active():
            return True
        return False

    def is_token_active(self):
        if self.cookies and self.token:
            current = time.time()
            elapsed = current - self.token_created_at
            if elapsed <= self.token_expires:
                return True
        return False

    def is_login_active(self):
        if self.cookies and self.token:
            current = time.time()
            elapsed = current - self.login_created_at
            if elapsed <= self.login_expires:
                return True
        return False

    @staticmethod
    def to_header_array():
        arr =[]
        arr.append('created_at')
        arr.append('login')
        arr.append('cookies_raw')
        arr.append('cookies')
        arr.append('login_created_at')
        arr.append('login_expires')
        arr.append('token')
        arr.append('token_created_at')
        arr.append('token_expires')

        return arr