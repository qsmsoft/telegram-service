import bcrypt


def get_password_hash(password: str) -> str:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    h_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return h_password.decode('utf-8')


def verify_password(plain_password: str, h_password: str) -> bool:
    # Compare the plain password with the hashed one
    return bcrypt.checkpw(plain_password.encode('utf-8'), h_password.encode('utf-8'))
