import requests
import json
import jsonpath
import random
from .models import User

baseUrl = "http://127.0.0.1:8000/"

from django.test import TestCase


class UserTest(TestCase):

    def test_user_able_to_login(self) :
        path = "lms/login/"
        response = requests.request("POST",url=baseUrl+path,json=json.loads('{"email":"rames@gmail.com","password":"smit@123"}'))
        print(response)
        responseJson = json.loads(response.text)
        print(responseJson)
        self.assertEquals(response.status_code,200)
    


