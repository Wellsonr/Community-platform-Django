# To change the Python Object data into Json objects data so the we can render the results into views
from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta :
        model = Room
        fields = '__all__'