import dotenv
import os
import jwt

dotenv.load_dotenv()

secret = os.getenv("secret")
algorithm = os.getenv("algorithm")

def encode(payload):
	return jwt.encode(payload, secret, algorithm)


def decode(jwt_token):
	return jwt.decode(jwt_token, secret, algorithm)