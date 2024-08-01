from src.backends.database import get_db_sess, Session
from src.backends.security import get_password_hash
from src.backends.users.models import User
from src.backends.config import Settings

def initialize_superuser():
    # db: Session = get_db_sess()
    # app_settings: Settings = Settings()
    # print("initiating super user")
    # existing_super_user = db.query(User).filter(User.user_name==app_settings.admin_username).first()
    # if existing_super_user:
    #     print("existing superuser found. skipping...")
    #     return
    # new_user = User(
    #     user_name = app_settings.admin_username,
    #     is_admin = True,
    #     hashed_password = get_password_hash(app_settings.admin_password)
    # )

    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    # print("Created admin user: ",new_user.user_name)
    pass