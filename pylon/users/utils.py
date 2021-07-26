from .models import User

def user_exists(email):
    temp_user = User.objects.filter(email=email).first()
    if temp_user:
        return True
    return False