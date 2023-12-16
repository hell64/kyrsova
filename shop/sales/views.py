from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

class GetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            user_data = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
        user_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk, format=None):
        user_data = Product.objects.get(pk=pk)
        serializer = ProductSerializer(user_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
