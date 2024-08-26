from django.urls import resolve, reverse
from healthData.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from .tests_setup import TestSetup

class TestsUrls(TestSetup):

    def test_get_all_users_url_resolves(self):
        self.assertEquals(resolve(self.get_all_users).func, get_all_users)
        
    def test_user_detail_url_resolves(self):
        self.assertEquals(resolve(self.user_detail).func, user_detail)
        
    def test_token_obtain_pair_url_resolves(self):
        self.assertEquals(resolve(self.token_obtain_pair).func.view_class, TokenObtainPairView)
        
    def test_token_refresh_url_resolves(self):
        self.assertEquals(resolve(self.token_refresh).func.view_class, TokenRefreshView)
        
    def test_token_verify_url_resolves(self):
        self.assertEquals(resolve(self.token_verify).func.view_class, TokenVerifyView)
        
    def test_get_groups_url_resolves(self):
        self.assertEquals(resolve(self.get_groups).func, get_groups)
        
    def test_get_group_url_resolves(self):
        self.assertEquals(resolve(self.get_group).func, get_group)
        
    def test_create_group_url_resolves(self):
        self.assertEquals(resolve(self.create_group).func, create_group)
        
    def test_get_permissions_url_resolves(self):
        self.assertEquals(resolve(self.get_permissions).func, get_permissions)
        
    def test_get_permission_url_resolves(self):
        self.assertEquals(resolve(self.get_permission).func, get_permission)
        
    def test_criar_documento_url_resolves(self):
        self.assertEquals(resolve(self.criar_documento).func, criar_documento)
        
    def test_get_all_documents_url_resolves(self):
        self.assertEquals(resolve(self.get_all_documents).func, get_all_documents)
        
    def test_listar_documentos_com_profissionais_url_resolves(self):
        self.assertEquals(resolve(self.listar_documentos_com_profissionais).func, listar_documentos_com_profissionais)
        
    def test_atualizar_documento_por_sns_url_resolves(self):
        self.assertEquals(resolve(self.atualizar_documento_por_sns).func, atualizar_documento_por_sns)
        
    def test_buscar_por_sns_url_resolves(self):
        self.assertEquals(resolve(self.buscar_por_sns).func, buscar_por_sns)
        
    def test_atualizar_dados_paciente_por_sns_url_resolves(self):
        self.assertEquals(resolve(self.atualizar_dados_paciente_por_sns).func, atualizar_dados_paciente_por_sns)
        
    def test_ativar_sinal_vital_url_resolves(self):
        self.assertEquals(resolve(self.ativar_sinal_vital).func, ativar_sinal_vital)
        
    def test_desativar_sinal_vital_url_resolves(self):
        self.assertEquals(resolve(self.desativar_sinal_vital).func, desativar_sinal_vital)
        
    def test_delete_sinal_vital_url_resolves(self):
        self.assertEquals(resolve(self.delete_sinal_vital).func, delete_sinal_vital)
        
    def test_delete_device_url_resolves(self):
        self.assertEquals(resolve(self.delete_device).func, delete_device)
        
    def test_listar_notificacoes_por_sns_url_resolves(self):
        self.assertEquals(resolve(self.listar_notificacoes_por_sns).func, listar_notificacoes_por_sns)
        
    def test_update_notificacao_url_resolves(self):
        self.assertEquals(resolve(self.update_notificacao).func, update_notificacao)
        
    def test_recover_password_url_resolves(self):
        self.assertEquals(resolve(self.recover_password).func, recover_password)    