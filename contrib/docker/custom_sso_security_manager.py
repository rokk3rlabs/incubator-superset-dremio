from flask import redirect, g, flash, request
from superset.security import SupersetSecurityManager
from flask_login import UserMixin
import requests
import os

class User(UserMixin):
    def __init__(self, user):
        self.email = user["email"]
        self.firstName = user["firstName"]
        self.lastName = user["lastName"]
        self.id = 1
        self.roles = [{"name": "Admin", "id": 1}]

class CustomSecurityManager(SupersetSecurityManager):
    # GRAPHPATH FLOW
    def oauth_user_info(self, provider, response=None):
        return {"email": "luisa.gonzalez@rokk3rlabs.com", "firstName": "luisa", "lastName": "gonzalez"}
    def auth_user_oauth (self, userinfo):
        return User(userinfo)
    
    
    def load_user_from_request(self, header_val):  
        response = requests.get(os.environ.get("API_ME_URL"), headers = {
            "Authorization": header_val,
            "x-client-id": request.headers.get("x-client-id"),
            "x-client-secret": request.headers.get("x-client-secret")
        })
        if response.status_code is 200 :
            return User(response.json()["data"])

    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)
        self.lm.header_loader(self.load_user_from_request)