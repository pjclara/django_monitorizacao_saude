from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group

class ValoresSerializer(serializers.Serializer):
    valor = serializers.FloatField()
    data = serializers.DateTimeField()
    alerta = serializers.BooleanField(default=False)
    lida = serializers.BooleanField(default=False)
    dataLida = serializers.DateTimeField(default=None, required=False, allow_null=True)
    

class SinaisVitaisSerializer(serializers.Serializer):
    maximo = serializers.FloatField()
    minimo = serializers.FloatField()
    tipo = serializers.CharField(max_length=100)
    unidade = serializers.CharField(max_length=10)
    valores = ValoresSerializer(many=True)
    ativo = serializers.BooleanField(default=False)
    readingFrequency = serializers.IntegerField()

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    role = serializers.CharField(max_length=100)

class DispositivoSerializer(serializers.Serializer):
    profissionais = UserSerializer(many=True, required=False, allow_null=True)
    data_inicio = serializers.DateTimeField()
    data_fim = serializers.DateTimeField()
    ativo = serializers.BooleanField(default=False)
    modelo = serializers.CharField(max_length=100)
    fabricante = serializers.CharField(max_length=100)
    numeroSerie = serializers.IntegerField()
    descricao = serializers.CharField(max_length=255, allow_blank=True, allow_null=True, required=False)
    sinaisVitais = SinaisVitaisSerializer(many=True)

class DocumentoSerializer(serializers.Serializer):
    sns = serializers.IntegerField()
    nome = serializers.CharField(max_length=100)
    dataNascimento = serializers.DateTimeField()
    genero = serializers.CharField(max_length=10)
    telefone = serializers.CharField(max_length=9)
    peso = serializers.FloatField()
    altura = serializers.FloatField()
    dispositivos = DispositivoSerializer(many=True)
    
    def validate_sns(self, value):
        if not (100000000 <= value <= 999999999):
            raise serializers.ValidationError("O campo 'sns' deve ter exatamente 9 dígitos.")
        return value
    
class DocumentoSemDispositivosSerializer(serializers.Serializer):
    sns = serializers.IntegerField()
    nome = serializers.CharField(max_length=100)
    dataNascimento = serializers.DateTimeField()
    genero = serializers.CharField(max_length=10)
    telefone = serializers.CharField(max_length=9)
    peso = serializers.FloatField()
    altura = serializers.FloatField()
    
    def validate_sns(self, value):
        if not (100000000 <= value <= 999999999):
            raise serializers.ValidationError("O campo 'sns' deve ter exatamente 9 dígitos.")
        return value

    class Meta:
        fields = ['sns', 'nome', 'dataNascimento', 'genero', 'peso', 'altura']

from django.utils import timezone       
class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    message = serializers.CharField(max_length=100)
    utente = serializers.IntegerField()
    read = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(default=serializers.CreateOnlyDefault(timezone.now))
    updated_at = serializers.DateTimeField(required=False)
    
       

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):       
        token = super().get_token(user)
        # Add custom claims
        #token['name'] = user.name
        token['email'] = user.email,
        token['full_name'] = user.full_name,
        token['is_superuser'] = user.is_superuser,
        token['mobile_phone'] = user.mobile_phone,
        token['health_number'] = user.health_number,
        token['taxpayer_number'] = user.taxpayer_number,
        token['type_user'] = user.type_user,
        token['is_staff'] = user.is_staff,
        token['is_active'] = user.is_active,
        token['groups'] = [group.name for group in user.groups.all()]
        
        return token
    

class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
    full_name = serializers.CharField(max_length=255, default='', allow_blank=True,)
    is_active = serializers.BooleanField(default=True)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)
    mobile_phone = serializers.CharField(max_length=9, allow_blank=True, allow_null=True, required=False)
    health_number = serializers.CharField(max_length=9, allow_blank=True, allow_null=True, required=False)
    taxpayer_number = serializers.CharField(max_length=9, allow_blank=True, allow_null=True, required=False)
    type_user = serializers.CharField(max_length=100)  
    role = serializers.CharField(max_length=100, write_only=True)
    
    #updae
    def update(self, instance, validated_data):
        if not validated_data['health_number']:
            health_number=None
        else:
            health_number=validated_data['health_number']
            
        if not validated_data['taxpayer_number']:
            taxpayer_number=None
        else:
            taxpayer_number=validated_data['taxpayer_number']       
        
        customer = CustomUser.objects.get(email=validated_data['email'])
        customer.full_name = validated_data['full_name']
        customer.is_active = validated_data['is_active']
        customer.is_staff = validated_data['is_staff']
        customer.is_superuser = validated_data['is_superuser']
        customer.mobile_phone = validated_data['mobile_phone']
        customer.health_number = validated_data['health_number']
        customer.type_user = validated_data['type_user']
        customer.set_password(validated_data['password'])
        customer.save()
        return customer
    
    
    def create(self, validated_data):
        group =  Group.objects.filter(name=validated_data['role'])           
        if not group:
            group = Group.objects.create(name=validated_data['role'])
        else:
            group = group[0]
            
        if not validated_data['health_number']:
            health_number=None
        else:
            health_number=validated_data['health_number']
            
        if not validated_data['taxpayer_number']:
            taxpayer_number=None
        else:
            taxpayer_number=validated_data['taxpayer_number']
            
        customUser = CustomUser.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            is_active=validated_data['is_active'],
            is_staff=validated_data['is_staff'],
            is_superuser=validated_data['is_superuser'],
            mobile_phone=validated_data['mobile_phone'],
            health_number=health_number,
            taxpayer_number=taxpayer_number,
            password=validated_data['password'],
        )
        if customUser:
            customUser.groups.add(group)
            return customUser
        else:
            return None
        

        