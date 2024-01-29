from django.shortcuts import render
from django.http import HttpResponse
from . qr import Qr
from . camerastream import CameraStream
from django.http import StreamingHttpResponse
import cv2
from pyzbar.pyzbar import decode
from django.http import JsonResponse
from . serializers import UserSerializer
from django.shortcuts import get_object_or_404


import requests
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import QRCodeScan, Student, TransactionHistory
from .serializers import QRCodeScanSerializer, StudentSerializer, UserRegistrationSerializer

from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, logout

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
import json
from .genrateAcesstoken import get_access_token
from .stkpush import initiate_stk_push
from . import stkpush
# Create your views here.  

class TransactionInit(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            phone_number = data.get('phone_number', '')
            amount = data.get('amount', '')

            # Perform any necessary processing with the data
            # For simplicity, we are just printing the data here
            stkpush.initiate_stk_push(phone_number, amount)
            print(f'Phone Number: {phone_number}, Amount: {amount}')

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
def home(request):
    return render(request, 'base/detect.html')
def scanner(request, code): 
    return HttpResponse(f"<h1>{code}</h1>")
def scan(request):
    return render(request, 'base/scanne.html')

# views.py

def process_qr_code(request):
    if request.method == 'POST':
        qr_code_data = request.POST.get('qr_code_data')
        print('QR Code Data:', qr_code_data)
        return JsonResponse({ 'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def genarate(request):
    return HttpResponse("Genarate page")

# @api_view(['POST'])
# @permission_classes([AllowAny])
def add_student(request):
    if request.method == 'POST' :
        name = request.POST['name']
        _class = request.POST['_class']
        adm = request.POST['adm']
        balance = request.POST['balance']
        img = request.FILES['img']
        print(img)
        # upload = request.FILES['img']
        # upload = img
        # fss = FileSystemStorage()
        # file = fss.save(upload, content=upload)
        # file_url = fss.url(file)
        counter = 0
        adm = adm.replace('/','_')
        # for x in adm:
        #     if x == '/':
        #         adm[counter] = '-'
        #     counter += 1
            
            
        student = Student(name=name, class_name=_class, student_adm=adm, balance=balance, image=img)
        student.save()
        
        Qr(f"{student.student_adm}", f'{name}').gen()
        return Response({'status': 'Child added successfully'})

        # return HttpResponse(f"It's working{img}")
    return render(request, 'base/add_student.html')

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
import base64
from django.core.files.base import ContentFile

class AddStudentAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Get data from request
            name = request.data.get('name')
            student_adm = request.data.get('student_adm')
            class_name = request.data.get('class_name')
            image_base64 = request.data.get('image')

            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            student_adm = student_adm.replace('/','_')
            
            # Save the image to the media folder
            student = Student(name=name, student_adm=student_adm, class_name=class_name)
            student.image.save(f"{student_adm}_image.jpg", ContentFile(image_data), save=True)
            Qr(f"{student.student_adm}", f'{name}').gen()


            # Return success response
            return Response({'message': 'Student added successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle errors
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def _add_student_api(request):
    if request.method == 'POST' :
        # name = request.POST['name']
        # _class = request.POST['_class']
        # adm = request.POST['adm']
        # balance = request.POST['balance']
        # img = request.FILES['img']

        name = request.data.get('name')
        adm = request.data.get('student.adm')
        _class = request.data.get('class_name')
        img = request.FILES['img']

        '''
        'name': nameController.text,
        'student_adm': admController.text,
        'class_name': classController.text,
        'image': imageBase64,
        '''
        print(img)
        # upload = request.FILES['img']
        # upload = img
        # fss = FileSystemStorage()
        # file = fss.save(upload, content=upload)
        # file_url = fss.url(file)
        counter = 0
        adm = adm.replace('/','_')
        # for x in adm:
        #     if x == '/':
        #         adm[counter] = '-'
        #     counter += 1
            
            
        student = Student(name=name, class_name=_class, student_adm=adm, image=img)
        student.save()
        
        Qr(f"{student.student_adm}", f'{name}').gen()
        return HttpResponse(f"It's working{img}")
    return Response({'status': 'Error adding child'}, status=400)
    # return render(request, 'base/add_student.html')
@api_view(['POST'])
@permission_classes([AllowAny])
def add_student_api(request):
    # print(request.data)

    try:
        # Get data from request
        name = request.data.get('name')
        student_adm = request.data.get('student_adm')
        class_name = request.data.get('class_name')
        image_base64 = request.data.get('image')

        # Decode base64 image
        image_data = base64.b64decode(image_base64)

        # student_ = Student.objects.get(name=)
        # Save the image to the media folder
        student = Student(name=name, student_adm=student_adm, class_name=class_name, balance=0, cumilative_deposit=0, cumilative_withdraw=0)
       
        student.image.save(f"{student_adm}_image.jpg", ContentFile(image_data), save=True)
        Qr(f"{student.student_adm}", f'{name}').gen()


        # Return success response
        return Response({'message': 'Student added successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle errors
        print(str(e))
        # print(request.data)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def add_bulk_students(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        # Open file and read data 
        data_from_open_file = []
        
        for data in data_from_open_file:
            student = Student(
                name = data['name'],
                class_name = data['class'],
                student_adm = data['adm'],
                balance=data['balance'],
                image = data['image'],
            )
            student.save()
            # data['name'] 

# API Views

@api_view(['POST'])
@permission_classes([AllowAny])
def receive_qr_code(request):
    data = request.data.get('data')

    if data:
        qr_code_scan = QRCodeScan.objects.create(data=data)
        serializer = QRCodeScanSerializer(qr_code_scan)
        return Response(serializer.data, status=201)

    return Response({'error': 'Invalid data'}, status=400)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_student_data(request, student_id):
    try:
        student = Student.objects.get(student_adm=student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def update_balance_agent(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
        withdraw_amount = int(request.data.get('balance'))
        new_balance = student.balance - int(request.data.get('balance'))
        transactionHist = TransactionHistory(
            student=student,
            init_balance=student.balance,
            new_balance=new_balance, 
            transaction_type="Withdraw",
            transacted_amount=int(request.data.get('balance')),
            )
        print(transactionHist.time)

        if new_balance is not None:
            student.balance = new_balance
            student.cumilative_withdraw  += withdraw_amount
            student.save()
            transactionHist.save()
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid data'}, status=400)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def update_balance_parent(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
        deposit_amount = int(request.data.get('balance'))
        new_balance = student.balance + int(request.data.get('balance'))
        transactionHist = TransactionHistory(
            student=student,
            init_balance=student.balance,
            new_balance=new_balance, 
            transaction_type="Deposit",
            transacted_amount=int(request.data.get('balance')),
            )
        print(transactionHist.time)

        if new_balance is not None:
            student.balance = new_balance
            student.cumilative_deposit += deposit_amount
            student.save()
            transactionHist.save()
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid data'}, status=400)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)
    
    

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            user = authenticate(request=request, email=email, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user_id': user.pk, 'email': user.email}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': 'Must include "email" and "password".'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({"token":token.key, 'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


from django_daraja.mpesa.core import MpesaClient

def stk(request):
    cl = MpesaClient()
    phone_number = '254746727592'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://c7d4-41-210-143-183.ngrok-free.app'
    # callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
  
    return HttpResponse(response)
def stk_push_callback(request):
    data = request.body
    return HttpResponse("This is an stk push")

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f'email {email} password {password}')
        # Simple authentication logic, replace it with your actual authentication logic
        user = authenticate(email=email, password=password)

        if user is not None:
            # Authentication successful
            return JsonResponse({'message': 'Login successful'})
        else:
            # Authentication failed
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    # Method not allowed for other request types
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def logout_view(request):
    # Assuming you are using Django's built-in authentication
    logout(request)

    # You can add additional logic or messages here if needed
    return JsonResponse({'message': 'Logout successful'})


from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


# @permission_classes([AllowAny])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token":token.key, "user":serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def login_(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not fount"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user) 
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user":serializer.data})



@api_view(['GET'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def get_current_user(request):
    user_data = {
        'username': request.user.username,
        'email': request.user.email,
        # Add other user-related fields as needed
    }
    return Response(user_data)

from .models import Parent
from .serializers import ParentSerializer
from rest_framework.parsers import JSONParser


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])

def parent_list(request):
    if request.method == 'GET':
        parents = Parent.objects.all()
        serializer = ParentSerializer(parents, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def parent_detail_by_name(request, name):
    try:
            parent = Parent.objects.get(name=name)
    except Parent.DoesNotExist:
            return Response({'error': 'Parent not found'}, status=404)

    if request.method == 'GET':
            serializer = ParentSerializer(parent)
            return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def parent_detail(request, pk):
    try:
        parent = Parent.objects.get(pk=pk)
    except Parent.DoesNotExist:
        return Response({'error': 'Parent not found'}, status=404)

    if request.method == 'GET':
        serializer = ParentSerializer(parent)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ParentSerializer(parent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        parent.delete()
        return Response({'message': 'Parent deleted successfully'}, status=204)
    
from . serializers import TransactionHistorySerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def transactionHistory(request, pk):
    student = Student.objects.get(id=pk)
    transactionHistory = TransactionHistory.objects.filter(student__id=pk).order_by('-id')
    # transactionHistory = TransactionHistory.objects.()
    if request.method == 'GET':
        serializer = TransactionHistorySerializer(transactionHistory, many=True)
        return Response(serializer.data)

from rest_framework import generics
from .models import Student
from .serializers import StudentSerializer

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def student_list(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)
      
def websocket_path(request):
    return HttpResponse("WebSocket path")

from . serializers import ChildSerializer
@api_view(['POST'])
@permission_classes([AllowAny])
# @api_view(['POST'])
def add_child_to_parent(request, parent_id):
    # Retrieve the parent instance
    parent = get_object_or_404(Parent, id=parent_id)

    if request.method == 'POST':
        # Get the child ID from the request data
        child_id = request.data.get('child_id')

        # Retrieve the child instance
        child = get_object_or_404(Student, student_adm=child_id)

        # Add the existing child to the parent's children field
        parent.students.add(child)


        return Response({'status': 'Child added successfully'})

    return Response({'status': 'Error adding child'}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_child_to_parent_by_name(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    if request.method == 'POST':
        child_name = request.data.get('child_name')
        child = get_object_or_404(Student, student_name=child_name)
        parent.students.add(child)






from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    # def perform_create(self, serializer):
    #     serializer.save()

    def perform_create(self, serializer):
        user_instance = serializer.save()

        # Create an instance of the Parent model with the same username, email, and user (foreign key)
        user = User.objects.get(username=user_instance.username)
        parent = Parent(user=user, name=user_instance.username)
        parent.save()
        # parent_data = {
        #     'username': user_instance.username,
        #     'email': user_instance.email,
        #     'user': user_instance.id,  # Assuming the foreign key is named 'user'
        #     # Add other fields if needed
        # }

        # parent_serializer = ParentSerializer(data=parent_data)
        # if parent_serializer.is_valid():
        #     parent_serializer.save()
        # else:
        #     # Handle validation errors for the Parent model data
        #     print(f"Parent Model Validation Errors: {parent_serializer.errors}")
    def post(self, request, *args, **kwargs):
        print(f"Request data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        print(f"Serializer data: {serializer.initial_data}")
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
# class RegisterAPIView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]

from . serializers import LoginSerializer
# class LoginAPIView(TokenObtainPairView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']

#         user = authenticate(username=username, password=password)

#         if user is not None:
#             response = super().post(request, *args, **kwargs)
            
#             return response
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        user = User.objects.filter(username=username).first()

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=400)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=400)

        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data)
# class LoginAPIView(TokenObtainPairView):
#     # permission_classes = [permissions.AllowAny]
#     permission_classes = [permissions.AllowAny]
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username', None)
#         password = request.data.get('password', None)

#         user = User.objects.filter(username=username).first()

#         if user is None:
#             return Response({'error': 'Invalid credentials'}, status=400)

#         if not user.check_password(password):
#             return Response({'error': 'Invalid credentials'}, status=400)

#         refresh = RefreshToken.for_user(user)
#         data = {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }
#         return Response(data)
# def login_user(request):
#     try:
#         user_name = request.data.get('username')
#         password = request.data.get('password')

#         user = login()




    # return HttpResponse("This page")
# def qr_code_scanner(request):
#     # Open the camera
#     cap = cv2.VideoCapture(0)

#     while True:
#         # Read a frame from the camera
#         ret, frame = cap.read()

#         # Decode QR codes in the frame
#         decoded_objects = decode(frame)

#         for obj in decoded_objects:
#             # Extract QR code data
#             qr_data = obj.data.decode('utf-8')
#             print('QR Code Data:', qr_data)

#             # You can do further processing with the QR code data

#         # Display the frame
#         cv2.imshow('QR Code Scanner', frame)

#         # Break the loop if 'q' key is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Release the camera and close the window
#     cap.release()
#     cv2.destroyAllWindows()

#     return render(request,"base/detect.html")