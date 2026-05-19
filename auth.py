from Database import get_user_by_username, get_user_by_email
from werkzeug.security import check_password_hash

def verify_login(username, pass_in):
    user_info = get_user_by_username(username)
    if user_info != False and check_password_hash(user_info[3], pass_in) is True:
        return True
    else:
        return False
    
def check_username_avaliable(username):
    if get_user_by_username(username) == False:
        return True
    else:
        return False
    
def check_email_avaliable(email):
    if get_user_by_email(email) == False:
        return True
    else:
        return False
