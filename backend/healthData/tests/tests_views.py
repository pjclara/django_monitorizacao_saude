from healthData.tests.tests_setup import TestSetup
from rest_framework.test import APITestCase

class TestViews(TestSetup):
    #get_all_users
    def test_get_all_users(self):
        response = self.client.get(self.get_all_users)
        self.assertEquals(response.status_code, 200)
    
    # get a user by id    

    def test_create_user(self):
        data = {
                    "full_name":"medico",
                    "email":"asdasd@sadsd.pt",
                    "type_user":"profissional",
                    "role":"medico",
                    "mobile_phone":965883163,
                    "health_number":123456784,
                    "taxpayer_number":123456785
        }
        response = self.client.post(self.get_all_users, data, format='json')
        self.assertEquals(response.status_code, 201)