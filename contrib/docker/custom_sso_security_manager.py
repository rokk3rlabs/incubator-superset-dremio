from flask import redirect, g, flash, request
from superset.security import SupersetSecurityManager
import requests
import os

class CustomSecurityManager(SupersetSecurityManager):
    def oauth_user_info(self, provider, response=None):
        response = requests.get(os.environ.get("AUTH_ME_URL"), headers = {
            "Authorization": response["access_token"],
            "x-client-id": os.environ.get("AUTH_CLIENT_ID"),
            "x-client-secret": os.environ.get("AUTH_CLIENT_SECRET")
        })
        if response.status_code in 200: 
            user = response.json()["data"]
            return userSuperset
        return {}

    def auth_user_oauth (self, userInfo):
        userSuperset = self.appbuilder.sm.find_user(email=userInfo["email"])
        return userSuperset
    
    def load_user_from_request(self, header_val):  
        response = requests.get(os.environ.get("API_ME_URL"), headers = {
            "Authorization": header_val,
            "x-client-id": request.headers.get("x-client-id"),
            "x-client-secret": request.headers.get("x-client-secret")
        })
        if response.status_code is 200 :
            user = response.json()["data"]
            userSuperset = self.appbuilder.sm.find_user(email=user["email"])
            return userSuperset

    def __init__(self, appbuilder):
        super(CustomSecurityManager, self).__init__(appbuilder)
        self.lm.header_loader(self.load_user_from_request)