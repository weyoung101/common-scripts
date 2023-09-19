import os
from dotenv import load_dotenv

def load_env():
    # Load environment variables from .env file
    load_dotenv()

    # Get all environment variables
    env_vars = os.environ

    # Return environment variables as dictionary
    return dict(env_vars)

