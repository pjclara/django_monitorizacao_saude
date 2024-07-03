from .models import CustomUser
from .serializers import CustomUserSerializer, DocumentoSerializer, NotificationSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .mongodb import db
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.response import Response
from rest_framework import status

from bson.objectid import ObjectId
from django.contrib.auth.models import Group,Permission

from django.conf import settings
from django.core.mail import send_mail
import secrets
import string

from datetime import datetime

# users crud
@api_view(['GET', 'POST', 'DELETE'])
def get_all_users(request):
    if request.method == 'GET':
        users =  db.healthData_customuser.find()
        serializer = CustomUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        # chek if the required fields are present
        
        if not 'full_name' in request.data:
            return JsonResponse({'error': 'Full name is required'}, status=400, safe=False)

        if not 'email' in request.data:
            return JsonResponse({'error': 'Email is required'}, status=400, safe=False)
        
        # if not 'password' in request.data:
        #     return JsonResponse({'error': 'Password is required'}, status=400, safe=False)
        
        if not 'type_user' in request.data:
            return JsonResponse({'error': 'Type user is required'}, status=400, safe=False)
        
        if not 'role' in request.data:
            return JsonResponse({'error': 'Role is required'}, status=400, safe=False)
        
        if not 'mobile_phone' in request.data:
            return JsonResponse({'error': 'Mobile phone is required'}, status=400, safe=False)
        
        if not request.data['type_user'] in ['profissional', 'paciente', 'admin']:
            return JsonResponse({'error': 'Type user must be profissional or paciente'}, status=400, safe=False)
        
        if (request.data['type_user'] == 'profissional') and not 'taxpayer_number' in request.data:
            return JsonResponse({'error': 'Taxpayer number is required'}, status=400, safe=False)
        
        # check if the taxpayer_number is unique except for 0
        if 'taxpayer_number' in request.data:
            if  request.data['taxpayer_number'] != 0 and (request.data['type_user'] == 'profissional'):
                if db.healthData_customuser.find_one({'taxpayer_number': request.data['taxpayer_number']}):
                    return JsonResponse({'error': 'Taxpayer number already exists'}, status=400, safe=False)
       
        if (request.data['type_user'] == 'paciente') and not 'health_number' in request.data:
            return JsonResponse({'error': 'Health number number is required'}, status=400, safe=False)
        
        # check if the health number is unique except for 0
        if  'health_number' in request.data:
            if  request.data['health_number'] != 0 and request.data['type_user'] == 'paciente':
                if db.healthData_customuser.find_one({'health_number': request.data['health_number']}):
                    return JsonResponse({'error': 'Health number already exists'}, status=400, safe=False)
                
        if db.healthData_customuser.find_one({'email': request.data['email']}):
            return JsonResponse({'error': 'Email already exists'}, status=400, safe=False)
        
        # phone number must be unique
        if db.healthData_customuser.find_one({'mobile_phone': request.data['mobile_phone']}):
            return JsonResponse({'error': 'Mobile phone already exists'}, status=400, safe=False)       
        
        random_password = generate_random_password()

        user_data = request.data.copy()
        user_data['password'] = random_password

        fullName = user_data['full_name']
        message = f'Hi { fullName }, welcome to the Health Monitor app. The password for your account is < {random_password} > .'
        send_email(user_data['email'], message)

        serializer = CustomUserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)
    
    elif request.method == 'DELETE':
        if 'email' not in request.data:
            return JsonResponse({'error': 'Email is required to delete a user'}, status=400, safe=False)
        
        result = db.healthData_customuser.delete_one({'email': request.data['email']})
        if result.deleted_count == 1:
            return JsonResponse({'message': 'User deleted successfully'}, status=200, safe=False)
        else:
            return JsonResponse({'error': 'User not found'}, status=404, safe=False)

@api_view(['GET', 'PUT', 'DELETE'])
#@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        user = db.healthData_customuser.find_one({'id': pk})
        # get the user groups
        user['groups'] = [group['group_id'] for group in db.healthData_customuser_groups.find({'customuser_id': user['id']})]
        # get name of the groups
        user['groups'] = [group['name'] for group in db.auth_group.find({'id': {'$in': user['groups']}})]
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404, safe=False)

    if request.method == 'GET':
        return JsonResponse({
            'id': user['id'],
            'email': user['email'],
            'full_name': user['full_name'],
            'is_active': user['is_active'],
            'is_staff': user['is_staff'],
            'is_superuser': user['is_superuser'],
            'mobile_phone': user['mobile_phone'],
            'health_number': user['health_number'],
            'taxpayer_number': user['taxpayer_number'],
            'type_user': user['type_user'],
            'groups': user['groups'] 
            
        })

    elif request.method == 'PUT':
        # check if the user exists
        # chek if the required fields are present
        
        if not 'full_name' in request.data:
            return JsonResponse({'error': 'Full name is required'}, status=400, safe=False)

        if not 'email' in request.data:
            return JsonResponse({'error': 'Email is required'}, status=400, safe=False)
        
        if not 'password' in request.data:
            return JsonResponse({'error': 'Password is required'}, status=400, safe=False)
        
        if not 'type_user' in request.data:
            return JsonResponse({'error': 'Type user is required'}, status=400, safe=False)
        
        if not 'role' in request.data:
            return JsonResponse({'error': 'Role is required'}, status=400, safe=False)
        
        if not 'mobile_phone' in request.data:
            return JsonResponse({'error': 'Mobile phone is required'}, status=400, safe=False)
        
        if not request.data['type_user'] in ['profissional', 'paciente', 'admin']:
            return JsonResponse({'error': 'Type user must be profissional or paciente'}, status=400, safe=False)
        
        if (request.data['type_user'] == 'profissional') and not 'taxpayer_number' in request.data:
            return JsonResponse({'error': 'Taxpayer number is required'}, status=400, safe=False)
        
        # check if the taxpayer_number is unique except for 0
        if 'taxpayer_number' in request.data:
            if  request.data['taxpayer_number'] != 0 and (request.data['type_user'] == 'profissional'):
                if db.healthData_customuser.find_one({'taxpayer_number': request.data['taxpayer_number'], 'id': pk}):
                    pass
                elif db.healthData_customuser.find_one({'taxpayer_number': request.data['taxpayer_number']}):
                    return JsonResponse({'error': 'Taxpayer number already exists'}, status=400, safe=False)
       
        if (request.data['type_user'] == 'paciente') and not 'health_number' in request.data:
            return JsonResponse({'error': 'Health number number is required'}, status=400, safe=False)
        
        # check if the health number is unique except for 0
        if  'health_number' in request.data:
            if  request.data['health_number'] != 0 and request.data['type_user'] == 'paciente':
                if db.healthData_customuser.find_one({'health_number': request.data['health_number'], 'id': pk}):
                    pass
                elif db.healthData_customuser.find_one({'health_number': request.data['health_number']}):
                    return JsonResponse({'error': 'Health number already exists'}, status=400, safe=False)
        
        # check if the user email already exists except for the same user
        if db.healthData_customuser.find_one({'email': request.data['email'], 'id': pk}):
            pass
        elif db.healthData_customuser.find_one({'email': request.data['email']}):
            return JsonResponse({'error': 'Email already exists'}, status=400, safe=False)       
        
        
        # phone number must be unique except for the same user
        if db.healthData_customuser.find_one({'mobile_phone': request.data['mobile_phone'], 'id': pk}):
            pass
        elif db.healthData_customuser.find_one({'mobile_phone': request.data['mobile_phone']}):
            return JsonResponse({'error': 'Mobile phone already exists'}, status=400, safe=False)
        
           
        if request.data.get('password') == "":
            # get the user password
            password = db.healthData_customuser.find_one({'id': pk})['password']
            request.data['password'] = password
            
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)

    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User was deleted successfully!'}, status=204, safe=False)
    
# login view
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        user = db.healthData_customuser.find_one({'email': request.data['email']})  
        if user:
            if user['password'] == request.data['password']:
                return JsonResponse({'message': 'Login successful!'}, status=200, safe=False)
            return JsonResponse({'error': 'Invalid password'}, status=400, safe=False)
        return JsonResponse({'error': 'User does not exist'}, status=404, safe=False)


# create a document
@api_view(['POST'])
def criar_documento(request):
    # verifica se o sns já existe
    sns = request.data.get('sns')
    if db.minha_colecao.find_one({"sns": sns}):
        return JsonResponse({"error": "Já existe um documento com esse sns"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = DocumentoSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        resultado = db.minha_colecao.insert_one(data)
        return Response({"_id": str(resultado.inserted_id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get all documents
@api_view(['GET'])
def get_all_documents(request):
    documents = db.minha_colecao.find()
    serializer = DocumentoSerializer(documents, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def document_detail(request, pk):
    try:
        document = db.minha_colecao.find_one({'_id': ObjectId(pk)})
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Document does not exist'}, status=404, safe=False)

    if request.method == 'GET':
        serializer = DocumentoSerializer(document)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        serializer = DocumentoSerializer(document, data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            db.minha_colecao.update_one({'_id': ObjectId(pk)}, {'$set': data})
            data_serialized = DocumentoSerializer(data).data
            return JsonResponse(data_serialized, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)

    elif request.method == 'DELETE':
        document.delete()
        return JsonResponse({'message': 'Document was deleted successfully!'}, status=204, safe=False)
    
    
# get all documentos with dispositivos com profissionais com id
@api_view(['GET'])
def listar_documentos_com_profissionais(request, id):
    documentos = db.minha_colecao.find({"dispositivos.profissionais.id": id})
    documentos = [{**doc, "_id": str(doc["_id"])} for doc in documentos]
    return JsonResponse(documentos, status=status.HTTP_200_OK, safe=False)

@api_view(['GET'])
def buscar_por_sns(request, sns):
    try:
        documentos = db.minha_colecao.find({"sns": sns})
        if documentos.count() == 0:
            return JsonResponse({}, status=status.HTTP_200_OK, safe=False)
        else:
            documentos_serializados = [DocumentoSerializer(doc).data for doc in documentos]
            return JsonResponse(documentos_serializados[0], status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def atualizar_dados_paciente_por_sns(request, sns):
    try:
        # Verificar se o documento existe
        documento = db.minha_colecao.find_one({"sns": sns})
        if not documento:
            return Response({"error": "Documento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        # Serializar os dados recebidos da requisição
        serializer = DocumentoSerializer(data=request.data) 
        if serializer.is_valid():
            data = serializer.validated_data
            # Atualizar o documento com base no _id
            db.minha_colecao.update_one({"sns": sns}, {"$set": data})
            documento_serializado = DocumentoSerializer(data).data
            return Response({
                "message": "Documento atualizado com sucesso.", 
                "data": documento_serializado}, 
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def atualizar_documento_por_sns(request, sns):
    try:
        # Verificar se o documento existe
        documento = db.minha_colecao.find_one({"sns": sns})
        if not documento:
            return Response({"error": "Documento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        # Serializar os dados recebidos da requisição
        serializer = DocumentoSerializer(data=request.data) 
        
        # alerta
        for dispositivo_idx, dispositivo in enumerate(request.data['dispositivos']):
            for sinal_idx, sinal in enumerate(dispositivo['sinaisVitais']):
                for valor_idx, valor in enumerate(sinal['valores']):
                    if valor['valor'] > sinal['maximo'] or valor['valor'] < sinal['minimo']:
                        valor['alerta'] = True
                        # confirmar se a notificação ja existe
                        if db.notificacoes.find_one({
                            "utente": sns,
                            "message": f"dispositivo_idx: {dispositivo_idx}, sinal_idx: {sinal_idx}, valor_idx: {valor_idx}, valor: {valor['valor']}"}):
                            pass
                        else:
                            notificacaoSerializado = NotificationSerializer(data={
                                "title": "Alerta",
                                "message": f"dispositivo_idx: {dispositivo_idx}, sinal_idx: {sinal_idx}, valor_idx: {valor_idx}, valor: {valor['valor']}",
                                "utente": documento['sns'],
                                "read": False,
                            })
                            if notificacaoSerializado.is_valid():
                                notificacao = notificacaoSerializado.validated_data
                                profissional = dispositivo.get('profissionais', [])[0].get('id')
                                latest_notification = db.notificacoes.find_one(
                                    {
                                        "utente": sns,
                                        "message": {
                                            "$regex": f"dispositivo_idx: {dispositivo_idx}, sinal_idx: {sinal_idx}"
                                        }
                                    }, sort=[("_id", -1)])
                                
                                db.notificacoes.insert_one(notificacao)

                                if latest_notification and not latest_notification.get('read', True):
                                    # If the latest notification is unread, skip sending a new notification
                                    pass
                                else:
                                    try:
                                        send_notification(
                                            documento['sns'],
                                            sinal['tipo'],
                                            f"room{profissional}")
                                    except Exception as e:
                                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                            else:
                                return Response(notificacaoSerializado.errors, status=status.HTTP_400_BAD_REQUEST)
        # Fim alerta                                            
        if serializer.is_valid():
            data = serializer.validated_data
            # Atualizar o documento com base no _id
            db.minha_colecao.update_one({"sns": sns}, {"$set": data})
            documento_serializado = DocumentoSerializer(data).data
            send_update(sns, "documento_serializado", f"room{sns}")
            return Response({
                "message": "Documento atualizado com sucesso.", 
                "data": documento_serializado}, 
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification(sns,message, room_name):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_name,
        {
            'type': 'send_notification',
            'message': message,
            'sns': sns
        }
    )

def send_update(sns, message, room_name):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_name,
        {
            'type': 'send_update',
            'message': message,
        }
    )
    

    
# crud for roles
@api_view(['POST'])
def create_group(request):
    if not request.data.get('name'):
        return Response({"error": "Name is required."}, status=status.HTTP_400_BAD_REQUEST)
    group = Group.objects.create(name=request.data.get('name'))
    if request.data.get('permissions'):
        for permission in request.data.get('permissions'):
            permission = Permission.objects.get(name=permission)
            group.permissions.add(permission)
    return JsonResponse({
        "id": group.id,
        "name": group.name,
        "permissions": [permission.name for permission in group.permissions.all()]
    }, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def get_groups(request):
    groups = Group.objects.all()
    groups = [{
        "id": group.id,
        "name": group.name,
        "permissions": [permission.name for permission in group.permissions.all()]
    } for group in groups]
    return JsonResponse(groups, status=status.HTTP_200_OK, safe=False)
    
@api_view(['GET','PUT','DELETE'])
def get_group(request, id):
    group = Group.objects.get(id=id)
    if request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PUT':
        group.name = request.data.get('name')
        group.permissions.clear()
        if request.data.get('permissions'):
            for permission in request.data.get('permissions'):
                permission = Permission.objects.get(name=permission)
                group.permissions.add(permission)
        group.save()
        return JsonResponse({
            "id": group.id,
            "name": group.name,
            "permissions": [permission.name for permission in group.permissions.all()]
        }, status=status.HTTP_200_OK)
    if request.method == 'GET':
        return JsonResponse({
            "id": group.id,
            "name": group.name,
            "permissions": [permission.name for permission in group.permissions.all()]
        }, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
# get all permissions
@api_view(['GET'])
def get_permissions(request):
    permissions = Permission.objects.all()
    permissions = [{
        "id": permission.id,
        "name": permission.name
    } for permission in permissions]
    return JsonResponse(permissions, status=status.HTTP_200_OK, safe=False)

# crud for permissions
@api_view(['POST'])
def create_permission(request):
    if not request.data.get('name'):
        return Response({"error": "Name is required."}, status=status.HTTP_400_BAD_REQUEST)
    permission = Permission.objects.create(name=request.data.get('name'))
    return JsonResponse({
        "id": permission.id,
        "name": permission.name
    }, status=status.HTTP_201_CREATED)
    
@api_view(['GET','PUT','DELETE'])
def get_permission(request, id):
    permission = Permission.objects.get(id=id)
    if request.method == 'DELETE':
        permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PUT':
        permission.name = request.data.get('name')
        permission.save()
        return JsonResponse({
            "id": permission.id,
            "name": permission.name
        }, status=status.HTTP_200_OK)
    if request.method == 'GET':
        return JsonResponse({
            "id": permission.id,
            "name": permission.name
        }, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
@api_view(['GET'])
def listar_notificacoes(request):
    notificacoes = db.notificacoes.find()
    notificacoesSerializer = [NotificationSerializer(notificacao).data for notificacao in notificacoes]    
    return Response(notificacoesSerializer, status=status.HTTP_200_OK)

@api_view(['GET'])
def listar_notificacoes_por_sns(request, sns):
    notificacoes = db.notificacoes.find({"utente": sns})
    notificacoes = [{**notificacao, "_id": str(notificacao["_id"])} for notificacao in notificacoes]
    return Response(notificacoes, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_notificacao(request, notificacao_id):
    notificacao = db.notificacoes.find_one({"_id": ObjectId(notificacao_id)})   
    if not notificacao:
        return Response({"error": "Notificação não encontrada."}, status=status.HTTP_404_NOT_FOUND)
    
    # explode message dispositivo_idx: 0, sinal_idx: 0, valor_idx: 0, valor: 0.0 para notificar o profissional
    message = notificacao['message']
    if message:
        dispositivo_idx = int(message.split(",")[0].split(":")[1].strip())
        sinal_idx = int(message.split(",")[1].split(":")[1].strip())
        valor_idx = int(message.split(",")[2].split(":")[1].strip())
        documento = db.minha_colecao.find_one({"sns": notificacao['utente']})
        #valor passa a lido
        documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['valores'][valor_idx]['lida'] = True
        documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['valores'][valor_idx]['dataLida'] = datetime.now()
        #save   
        db.minha_colecao.update_one({"sns": notificacao['utente']}, {"$set": documento})
        
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        # add field updated_at to data
        data['updated_at'] = datetime.now()
        if data.get('read') and not notificacao['read']:
            data['read'] = True
        else:
            data['read'] = False
        db.notificacoes.update_one({"_id": ObjectId(notificacao_id)}, {"$set": data})
        return Response({"_id": notificacao_id}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# desativar sinal vital por dispositivo, sinais vitais e sns
@api_view(['PUT'])
def desativar_sinal_vital(request, sns):
    try:
        documento = db.minha_colecao.find_one({"sns": sns})
        if not documento:
            return Response({"error": "Documento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        dispositivo_idx = request.data.get('dispositivo_idx')
        sinal_idx = request.data.get('sinal_idx')
        documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['ativo'] = False
        # se todos os sinais vitais do dispositivo estiverem desativados, o dispositivo também será desativado
        if all([not sinal['ativo'] for sinal in documento['dispositivos'][dispositivo_idx]['sinaisVitais']]):
            documento['dispositivos'][dispositivo_idx]['ativo'] = False
        db.minha_colecao.update_one({"sns": sns}, {"$set": documento})
        return Response({"message": "Sinal vital desativado com sucesso."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# ativar sinal vital por dispositivo, sinais vitais e sns

@api_view(['PUT'])
def ativar_sinal_vital(request, sns):
    try:
        documento = db.minha_colecao.find_one({"sns": sns})
        if not documento:
            return Response({"error": "Documento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        dispositivo_idx = request.data.get('dispositivo_idx')
        sinal_idx = request.data.get('sinal_idx')
        documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['ativo'] = True
        documento['dispositivos'][dispositivo_idx]['ativo'] = True
        if request.data.get('valor') < documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['minimo'] or request.data.get('valor') > documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['maximo']:
            alert = True
        else:
            alert = False
        documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['valores'].append(
            {
                "valor": request.data.get('valor'),
                "alerta": alert,
                "data": datetime.now(),
                "dataLida": None,
                "lida": False
                
            }
        )
        db.minha_colecao.update_one({"sns": sns}, {"$set": documento})
        send_update(sns, "sinal_vital_ativado", f"room{sns}")
       
       #notificação
        if request.data.get('valor') > documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['maximo'] or request.data.get('valor') < documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['minimo']:
            #last valor index
            valor_idx = len(documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['valores']) - 1
            notificacaoSerializado = NotificationSerializer(data={
                "title": "Alerta",
                "message": f"dispositivo_idx: {dispositivo_idx}, sinal_idx: {sinal_idx}, valor_idx: {valor_idx}, valor: {request.data.get('valor')}",
                "utente": documento['sns'],
                "read": False,
            })
            if notificacaoSerializado.is_valid():
                notificacao = notificacaoSerializado.validated_data
                profissional = documento['dispositivos'][dispositivo_idx].get('profissionais', [])[0].get('id')
                latest_notification = db.notificacoes.find_one(
                    {
                        "utente": sns,
                        "message": {
                            "$regex": f"dispositivo_idx: {dispositivo_idx}, sinal_idx: {sinal_idx}"
                        }
                    }, sort=[("_id", -1)])
                db.notificacoes.insert_one(notificacao)
                if latest_notification and not latest_notification.get('read', True):
                    # If the latest notification is unread, skip sending a new notification
                    pass
                else:
                    try:
                        send_notification(
                            documento['sns'],
                            documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['tipo'],
                            f"room{profissional}")
                    except Exception as e:
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(notificacaoSerializado.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Sinal vital ativado com sucesso."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# delete sinal vital por dispositivo, sinais vitais e sns
@api_view(['PUT'])
def delete_sinal_vital(request, sns):
    try:
        documento = db.minha_colecao.find_one({"sns": sns})
        if not documento:
            return Response({"error": "Documento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        dispositivo_idx = request.data.get('dispositivo_idx')
        sinal_idx = request.data.get('sinal_idx')
        del documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]
        db.minha_colecao.update_one({"sns": sns}, {"$set": documento})
        return Response({"message": "Sinal vital eleminado com sucesso."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# delete device por sns
@api_view(['PUT'])
def delete_device(request, sns):
    try:
        documento = db.minha_colecao.find_one({"sns": sns})
        if not documento:
            return Response({"error": "Documento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        dispositivo_idx = request.data.get('dispositivo_idx')
        del documento['dispositivos'][dispositivo_idx]
        db.minha_colecao.update_one({"sns": sns}, {"$set": documento})
        return Response({"message": "Dispositivo eleminado com sucesso."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def recover_password(request, email):
    user = db.healthData_customuser.find_one({'email': email})

    if user is not None:
        fullName = user['full_name']
        random_password = generate_random_password()
        
        user_data = {}
        user_data['email'] = user['email']
        user_data['full_name'] = fullName
        user_data['health_number'] = user['health_number']
        user_data['is_active'] = user['is_active']
        user_data['is_staff'] = user['is_staff']
        user_data['mobile_phone'] = user['mobile_phone']
        user_data['role'] = user['type_user']
        user_data['taxpayer_number'] = user['taxpayer_number']
        user_data['type_user'] = user['type_user']
        user_data['password'] = random_password

        serializer = CustomUserSerializer(user, data=user_data)
        if serializer.is_valid():
            serializer.save()
            message = f'Hi { fullName }. Your password was resetted as requested, the new password is < {random_password} >.'
            send_email(email, message)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    else: 
        return Response(status=status.HTTP_404_NOT_FOUND)
    
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_password = ''.join(secrets.choice(characters) for i in range(length))
    return random_password

def send_email(email, message):
    subject = 'Access to the Health Monitor App'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list )
    
@api_view(['GET'])
def procurar_por_sns(request, sns):
    try:
        documento = db.minha_colecao.find_one({"sns": sns})
        if documento:
            documento_serializado = DocumentoSerializer(documento).data
            return JsonResponse(documento_serializado, status=status.HTTP_200_OK, safe=False)
        else:
            return Response({"error": "Documento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)