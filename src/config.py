import os


class Settings:
    def __init__(self):
        self.db_name = os.getenv('db_name')
        self.db_user = os.getenv('db_user')
        self.db_host = os.getenv('db_host')
        self.db_port = os.getenv('db_port')
        self.db_password = os.getenv('db_password')
    
        self.access_code_expiring_minutes = int(os.getenv('ACCESS_CODE_EXPIRING_MINUTES', 3000))
        self.algorithm  = os.getenv('ALGORITHM','HS256')
        self.secret_key  = os.getenv('SECRET_KEY','mysecretkey')
        self.admin_secret_key = os.getenv('ADMIN_SECRET_KEY','fake_secret')

    def get_full_db_url(self):
        return f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'