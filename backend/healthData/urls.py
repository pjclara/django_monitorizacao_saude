from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('users/', views.get_all_users, name='get_all_users'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    
    # login
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # groups
    path('get_groups/', views.get_groups, name='get_groups'),
    path('get_group/<int:id>/', views.get_group, name='get_group'),
    path("create_group/", views.create_group, name="create_group"),
    
    # permissões
    path('get_permissions/', views.get_permissions, name='get_permissions'),
    path('get_permission/<int:id>/', views.get_permission, name='get_permission'),
    path('create_permission/', views.create_permission, name='create_permission'),
    
    # documents
    path('documentos/', views.criar_documento, name='criar_documento'),
    path('documentos/listar/', views.get_all_documents, name='get_all_documents'),
    path('patients/listar_documentos_com_profissionais/<int:id>/', views.listar_documentos_com_profissionais, name='listar_documentos_com_profissionais'),
    path('documentos/atualizar_documento_por_sns/<int:sns>/', views.atualizar_documento_por_sns, name='atualizar_documento_por_sns'),
    path('documentos/buscar_por_sns/<int:sns>/', views.buscar_por_sns, name='buscar_por_sns'),
    path('documentos/atualizar_dados_paciente_por_sns/<int:sns>/', views.atualizar_dados_paciente_por_sns, name='atualizar_dados_paciente_por_sns'),
    
    # ativar/desativar sinal vital
    path('documentos/ativar_sinal_vital/<int:sns>/', views.ativar_sinal_vital, name='ativar_sinal_vital'),
    path('documentos/desativar_sinal_vital/<int:sns>/', views.desativar_sinal_vital, name='desativar_sinal_vital'),
    #delete sinais vitais
    path('documentos/delete_sinal_vital/<int:sns>/', views.delete_sinal_vital, name='delete_sinal_vital'),
    #delete device 
    path('documentos/delete_device/<int:sns>/', views.delete_device, name='delete_device'),

    #notifications
    path('listar_notificacoes/<int:sns>/', views.listar_notificacoes_por_sns, name='listar_notificacoes_por_sns'),
    path('update_notificacao/<str:notificacao_id>/', views.update_notificacao, name='update_notificacao'),

    #Password Recovery
    path('password_recovery/<str:email>/', views.recover_password, name='password_recovery')
]

