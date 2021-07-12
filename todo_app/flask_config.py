import os

class Config:
    def __init__(self):
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
# class Config:
#     """Base configuration variables."""
#     SECRET_KEY = os.environ.get('SECRET_KEY')
#     if not SECRET_KEY:
#         raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
