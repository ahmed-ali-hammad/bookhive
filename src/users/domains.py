from passlib.context import CryptContext


class UserDomain:
    myctx = CryptContext(schemes=["sha256_crypt"])

    def __init__(self, username, email, password, first_name=None, last_name=None):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def hash_password(self):
        
        password_hash = UserDomain.myctx.hash(self.password)
        return password_hash
    

    def verify_password(self, password_has):
        return UserDomain.myctx.verify(self.password, password_has)
