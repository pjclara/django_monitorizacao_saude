from .models import CustomUser
from .serializers import DocumentoSerializer, NotificationSerializer, CustomPostUserSerializer, CustomPutUserSerializer, CustomPutUserPasswordSerializer
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
@permission_classes([IsAuthenticated])
def get_all_users(request):
    if request.method == 'GET':
        users =  db.healthData_customuser.find()
        
        serializer = CustomPutUserSerializer(users, many=True)
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

        serializer = CustomPostUserSerializer(data=user_data)
        if serializer.is_valid():
            message = f'Hi { fullName }, welcome to the Health Monitor app. The password for your account is < {random_password} > .'
            send_email(user_data['email'], message)
            serializer.save()
            return JsonResponse(serializer.data, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)
    
    elif request.method == 'DELETE':
        if 'email' not in request.data:
            return JsonResponse({'error': 'Email is required to delete a user'}, status=400, safe=False)
        
        user_patient = db.healthData_customuser.find_one({"email": request.data['email']})

        print('user_patient: ', user_patient)

        result_patient = db.minha_colecao.delete_one({'sns': user_patient['health_number']})

        print('result_patient: ', result_patient)

        if result_patient.deleted_count == 0:
            return JsonResponse({'error': 'User not found'}, status=404, safe=False)

        result = db.healthData_customuser.delete_one({'email': request.data['email']})
        if result.deleted_count == 1:
            return JsonResponse({'message': 'User deleted successfully'}, status=200, safe=False)
        else:
            return JsonResponse({'error': 'User not found'}, status=404, safe=False)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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
           
        # TODO - password mudar ao editar perfil

        serializer = CustomPutUserSerializer(user, data=request.data)
        print('serializer: ', serializer)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=400, safe=False)

    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User was deleted successfully!'}, status=204, safe=False)

# crud for groups 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def get_groups(request):
    groups = Group.objects.all()
    groups = [{
        "id": group.id,
        "name": group.name,
        "permissions": [permission.name for permission in group.permissions.all()]
    } for group in groups]
    return JsonResponse(groups, status=status.HTTP_200_OK, safe=False)

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
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

# crud for permissions
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_permissions(request):
    permissions = Permission.objects.all()
    permissions = [{
        "id": permission.id,
        "name": permission.name
    } for permission in permissions]
    return JsonResponse(permissions, status=status.HTTP_200_OK, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_permission(request):
    if not request.data.get('name'):
        return Response({"error": "Name is required."}, status=status.HTTP_400_BAD_REQUEST)
    permission = Permission.objects.create(name=request.data.get('name'))
    return JsonResponse({
        "id": permission.id,
        "name": permission.name
    }, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
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
    
    
# get all documentos with dispositivos com profissionais com id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_documentos_com_profissionais(request, id):
    documentos = db.minha_colecao.find({"dispositivos.profissionais.id": id})
    documentos = [{**doc, "_id": str(doc["_id"])} for doc in documentos]
    return JsonResponse(documentos, status=status.HTTP_200_OK, safe=False)

# create a document
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def criar_documento(request):
    # verifica se o sns já existe
    sns = request.data.get('sns')
    if db.minha_colecao.find_one({"sns": sns}):
        return JsonResponse({"error": "Já existe um documento com esse sns"}, status=status.HTTP_400_BAD_REQUEST)
    
    if db.healthData_customuser.find_one({'email': request.data['email']}):
        return JsonResponse({'error': 'Email already exists'}, status=400, safe=False)
    
    serializer = DocumentoSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        resultado = db.minha_colecao.insert_one(data)

        fullName = data['nome']
        random_password = generate_random_password()
        
        # criar um user com o email e password
        user_data = {
            "email": data['email'],
            "password": random_password,
            "full_name": data['nome'],
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
            "mobile_phone": data['telefone'],
            "health_number": data['sns'],
            "taxpayer_number": "",
            "type_user": "paciente",
            "role": "paciente"
        }
        
        user_serializer = CustomPostUserSerializer(data=user_data)
        print('user_serializer post: ', user_serializer)

        if user_serializer.is_valid():
            print('user_serializer.is_valid(): ', user_serializer.is_valid())
            message = f'Hi { fullName }. Your password was resetted as requested, the new password is < {random_password} >.'
            #send_email(data['email'], message)
            user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"_id": str(resultado.inserted_id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get all documents
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_documents(request):
    documents = db.minha_colecao.find()
    serializer = DocumentoSerializer(documents, many=True)
    return Response(serializer.data)

# get a document by sns
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

# update a document by sns
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def atualizar_dados_paciente_por_sns(request, sns):
    try:
        # Verificar se o documento existe
        documento = db.minha_colecao.find_one({"sns": sns})
        if not documento:
            return Response({"error": "Documento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        # email unique menos para o mesmo documento
        if db.minha_colecao.find_one({"email": request.data['email'], "sns": {"$ne": sns}}):
            return JsonResponse({"error": "Já existe um documento com esse email"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Serializar os dados recebidos da requisição
        serializer = DocumentoSerializer(data=request.data) 
        if serializer.is_valid():
            data = serializer.validated_data
            # Atualizar o documento com base no _id
            
            db.minha_colecao.update_one({"sns": sns}, {"$set": data})
            
            # Atualizar o usuário com base no email
            user = db.healthData_customuser.find_one({"email": documento['email']})
            if not user:
                # criar um user com o email e password
                # random_password = generate_random_password()
                random_password = data['nome'].replace(" ", "_") + "123"
                
                user_data = {
                    "email": data['email'],
                    "password": random_password,
                    "full_name": data['nome'],
                    "is_active": True,
                    "is_staff": False,
                    "is_superuser": False,
                    "mobile_phone": data['telefone'],
                    "health_number": data['sns'],
                    "taxpayer_number": "",
                    "type_user": "paciente",
                    "role": "paciente"
                }
                user_serializer = CustomPutUserSerializer(data=user_data)
                if user_serializer.is_valid():
                    user_serializer.save()
                else:
                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:              
                user['email'] = data['email']
                user['full_name'] = data['nome']
                user['mobile_phone'] = data['telefone']
                user['health_number'] = data['sns']
                db.healthData_customuser.update_one({"email":documento['email']}, {"$set": user})            
            
            documento_serializado = DocumentoSerializer(data).data
            return Response({
                "message": "Documento atualizado com sucesso.", 
                "data": documento_serializado}, 
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# activate a vital signal
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
            
        dataToApend = {
            "valor": request.data.get('valor'),
            "alerta": alert,
            "data": datetime.now(),
            "dataLida": None,
            "lida": False
        }
        documento['dispositivos'][dispositivo_idx]['sinaisVitais'][sinal_idx]['valores'].append(dataToApend)
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
       
        return JsonResponse({"message": "Sinal vital ativado com sucesso.","data": dataToApend}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# desativar sinal vital por dispositivo, sinais vitais e sns
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
   
   
# delete sinal vital por dispositivo, sinais vitais e sns
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def listar_notificacoes_por_sns(request, sns):
    notificacoes = db.notificacoes.find({"utente": sns})
    notificacoes = [{**notificacao, "_id": str(notificacao["_id"])} for notificacao in notificacoes]
    return Response(notificacoes, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
        # user_data = user.copy()
        user_data['password'] = random_password


        serializer = CustomPutUserPasswordSerializer(user, data=user_data)

        # TODO - Verificar o porque do serializer não ser valido
        print('serializer: ', serializer)

        if serializer.is_valid():
            print('serializer.is_valid(): ', serializer.is_valid())
            serializer.save()
            message = f'Hi { fullName }. Your password was resetted as requested, the new password is < {random_password} >.'
            send_email(email, message)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    else: 
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
            teste = "room" + sns
            send_update(sns, "documento_serializado", teste, documento_serializado)
            return Response({
                "message": "Documento atualizado com sucesso.", 
                "data": documento_serializado}, 
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

######################################
# auxiliar functions

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
    print(f"send_update {sns} {message} {room_name}")
    async_to_sync(channel_layer.group_send)(
        room_name,
        {
            'type': 'send_update',
            'message': message            
        }
    ) 

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_password = ''.join(secrets.choice(characters) for i in range(length))
    return random_password

def send_email(email, message):
    subject = 'Access to the Health Monitor App'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list )