from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from medspa.models import Medspa
from medspa.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    medspa_id = serializers.IntegerField(write_only=True)
    start_time = serializers.DateTimeField()
    total_price = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=8)
    total_duration = serializers.DurationField(read_only=True)
    status = serializers.ChoiceField(choices=Appointment.STATUS)

    class Meta:
        model = Appointment
        fields = ("id", "medspa_id", "start_time", "total_price", "total_duration", "status")


class AppointmentsView(APIView):
    def get(self, request, medspa_pk, pk=None, format=None):
        medspa = Medspa.objects.filter(pk=medspa_pk).first()
        if not medspa:
            return Response({"error": "Medspa not found."}, status=status.HTTP_404_NOT_FOUND)

        appointments = medspa.appointments.filter(pk=pk) if pk else medspa.appointments.all()
        if pk:
            serializer = AppointmentSerializer(appointments.get(pk=pk))
        else:
            serializer = AppointmentSerializer(appointments, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, medspa_pk, pk=None, format=None):
        medspa = Medspa.objects.filter(pk=medspa_pk).first()
        if not medspa:
            return Response({"error": "Medspa not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.dict()
        serializer = AppointmentSerializer(data={**data, "medspa_id": medspa_pk})
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

        appointment = medspa.appointments.filter(pk=pk).first()
        if not pk or not appointment:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.dict()
        serializer = AppointmentSerializer(appointment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid request.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
