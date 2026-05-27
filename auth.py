from database import get_user_by_username, get_user_by_email
from werkzeug.security import check_password_hash

def verify_login(username, pass_in):
    """Verifies that the username and password are correct."""
    user_info = get_user_by_username(username)
    if user_info is not False and check_password_hash(user_info[3], pass_in) is True:
        return True
    else:
        return False
    
def check_username_avaliable(username):
    """Checks if the username is available."""
    if get_user_by_username(username) is False:
        return True
    else:
        return False
    
def check_email_avaliable(email):
    """Checks if the email is available."""
    if get_user_by_email(email) is False:
        return True
    else:
        return False
