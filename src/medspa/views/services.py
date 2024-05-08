from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from medspa.models import Medspa
from medspa.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    medspa_id = serializers.IntegerField(write_only=True)
    name = serializers.CharField(max_length=64)
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    price = serializers.DecimalField(decimal_places=2, max_digits=8)
    duration = serializers.DurationField()

    class Meta:
        model = Service
        fields = ("id", "medspa_id", "name", "description", "price", "duration")


class ServicesView(APIView):
    def get(self, request, medspa_pk, pk=None, format=None):
        medspa = Medspa.objects.filter(pk=medspa_pk).first()
        if not medspa:
            return Response({"error": "Medspa not found."}, status=status.HTTP_404_NOT_FOUND)

        services = medspa.services.filter(pk=pk) if pk else medspa.services.all()
        if pk:
            serializer = ServiceSerializer(services.get(pk=pk))
        else:
            serializer = ServiceSerializer(services, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, medspa_pk, pk=None, format=None):
        medspa = Medspa.objects.filter(pk=medspa_pk).first()
        if not medspa:
            return Response({"error": "Medspa not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.dict()
        serializer = ServiceSerializer(data={**data, "medspa_id": medspa_pk})
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Invalid request.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, medspa_pk, pk=None, format=None):
        medspa = Medspa.objects.filter(pk=medspa_pk).first()
        if not medspa:
            return Response({"error": "Medspa not found."}, status=status.HTTP_404_NOT_FOUND)

        service = medspa.services.filter(pk=pk).first()
        if not pk or not service:
            return Response({"error": "Service not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.dict()
        serializer = ServiceSerializer(service, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid request.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
