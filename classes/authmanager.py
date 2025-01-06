class AuthManager:
    admin_username = os.getenv('ADMIN_USERNAME')
    admin_password = os.getenv('ADMIN_PASSWORD')

    @classmethod
    def check_auth(cls, username, password):
        # """
        # 관리자 인증을 확인합니다.
        
        # :param username: 입력된 사용자 이름
        # :param password: 입력된 비밀번호
        # :return: 인증 성공 여부
        # """
        return username == cls.admin_username and password == cls.admin_password
    @staticmethod
    def authenticate():
        """
        인증 실패 시 401 응답을 반환합니다.
        """
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials.', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Decorator for Authentication
def requires_auth(f):
    """
    기본 인증을 요구하는 데코레이터입니다.
    
    :param f: 보호할 함수
    :return: 보호된 함수
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not AuthManager.check_auth(auth.username, auth.password):
            return AuthManager.authenticate()
        return f(*args, **kwargs)
    return decorated