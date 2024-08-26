from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework.test import APIClient
from healthData.models import CustomUser
from django.urls import reverse

class TestSetup(APITestCase):
    def setUp(self):
        # Create a new user
        self.client = APIClient()
        self.get_all_users = reverse('get_all_users')
        self.user_detail =  reverse('user_detail', args=[115])
        self.token_obtain_pair = reverse('token_obtain_pair')
        self.token_refresh = reverse('token_refresh')
        self.token_verify = reverse('token_verify')
        self.get_groups = reverse('get_groups')
        self.get_group = reverse('get_group', args=[1])
        self.create_group = reverse('create_group')
        self.get_permissions = reverse('get_permissions')
        self.get_permission = reverse('get_permission', args=[1])
        self.criar_documento = reverse('criar_documento')
        self.get_all_documents = reverse('get_all_documents')
        self.listar_documentos_com_profissionais = reverse('listar_documentos_com_profissionais', args=[1])
        self.atualizar_documento_por_sns = reverse('atualizar_documento_por_sns', args=[1])
        self.buscar_por_sns = reverse('buscar_por_sns', args=[1])
        self.atualizar_dados_paciente_por_sns = reverse('atualizar_dados_paciente_por_sns', args=[1])
        self.ativar_sinal_vital = reverse('ativar_sinal_vital', args=[1])
        self.desativar_sinal_vital = reverse('desativar_sinal_vital', args=[1])
        self.delete_sinal_vital = reverse('delete_sinal_vital', args=[1])
        self.delete_device = reverse('delete_device', args=[1])
        self.listar_notificacoes_por_sns = reverse('listar_notificacoes_por_sns', args=[1])
        self.update_notificacao = reverse('update_notificacao', args=['1'])
        self.recover_password = reverse('password_recovery', args=['email'])
        
        self.data = {
                    "full_name":"medico",
                    "email":"medico@gmail.com",
                    "type_user":"profissional",
                    "role":"medico",
                    "mobile_phone":965883163,
                    "health_number":123456784,
                    "taxpayer_number":123456785
        }
        self.client.post(self.get_all_users, self.data, format='json')
        
        self.client.force_authenticate(user=CustomUser.objects.all().last())

        return super().setUp()
        
    def tearDown(self):
        return super().tearDown()
    
    #database
    