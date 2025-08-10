import random
import uuid

def generate_random_otp():
  return str(random.randint(100000, 999999))

def create_token():
  return str(uuid.uuid4())