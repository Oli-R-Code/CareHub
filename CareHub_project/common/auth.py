import re

def password_check(password):
    if len(password) < 6:
        return False
    
    if not re.search(r'[a-z]', password):
        return False
    
    if not re.search(r'[A-Z]', password):
        return False
    
    if not re.search(r'[-_+*?!$%#<>]', password):
        return False

    if not re.search(r'[0123456789]', password):
        return False

    return True