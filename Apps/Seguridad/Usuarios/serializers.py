from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    # Se Define el campo de contraseña como de solo escritura.
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        # Especificamos solo los campos que el usuario debe llenar.
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        """
        Este método se llama cuando .save() es invocado en la vista.
        Se encarga de crear el usuario con la contraseña hasheada.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'], # create_user se encarga del hasheo
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user