# generate_secret_key.py
import random
import string

def generate_secret_key(length=50):
    chars = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

if __name__ == "__main__":
    print("Your new SECRET_KEY:")
    print(generate_secret_key())
