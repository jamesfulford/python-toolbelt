# login.py
# by James Fulford
# for Joyful Love


class Login():
    """
    A Login is the means by which an Account accesses Buffer
    A Login usually brings up to 3 queues
    """

    def __init__(self, authentication):
        self.oath(authentication)
        from buffpy.user import User
        self.user = User(api=self.api)  # useless?

    def dictionary(self):
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "token": self.token,
        }

    def oath(self, authentication):
        from buffpy.api import API
        self.client_id = authentication["client_id"]
        self.client_secret = authentication["client_secret"]
        if "token" not in authentication.keys():
            self.get_token()
        self.token = authentication["token"]
        self.api = API(client_id=self.client_id, client_secret=self.client_secret, access_token=self.token)

    def get_token(self):
        from buffpy import AuthService
        import webbrowser
        redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
        service = AuthService(self.client_id, self.client_secret, redirect_uri)
        url = service.authorize_url
        webbrowser.open(url)
        raise Exception("Add token to authentication argument.")

    def profiles(self):
        from buffpy.profiles import Profiles
        return Profiles(api=self.api).all()

