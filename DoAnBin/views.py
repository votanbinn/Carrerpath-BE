from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from . import models
from . import serializers
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def running(request):
    return HttpResponse("App is running")

class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = models.AdminUser.objects.all()
    serializer_class = serializers.AdminUserSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    
class ExpertViewSet(viewsets.ModelViewSet):
    queryset = models.Expert.objects.all()
    serializer_class = serializers.ExpertSerializer
    
class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = models.Consultation.objects.all()
    serializer_class = serializers.ConsultationSerializer
    
class TestViewSet(viewsets.ModelViewSet):
    queryset = models.Test.objects.all()
    serializer_class = serializers.TestSerializer
    
class ResultViewSet(viewsets.ModelViewSet):
    queryset = models.Result.objects.all()
    serializer_class = serializers.ResultSerializer
    
class ForumViewSet(viewsets.ModelViewSet):
    queryset = models.Forum.objects.all()
    serializer_class = serializers.ForumSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                # Tìm kiếm người dùng bằng username
                user = models.Account.objects.get(username=username)

                # Sử dụng check_password để xác minh mật khẩu đã mã hóa
                if check_password(password, user.password):
                    # Đăng nhập thành công
                    return Response({"message": "Đăng nhập thành công!"}, status=status.HTTP_200_OK)
                else:
                    # Sai mật khẩu
                    return Response({"error": "Tên đăng nhập hoặc mật khẩu không chính xác."}, status=status.HTTP_401_UNAUTHORIZED)
            except models.Account.DoesNotExist:
                # Sai tên đăng nhập
                return Response({"error": "Tên đăng nhập hoặc mật khẩu không chính xác."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Đăng xuất thành công!"}, status=status.HTTP_200_OK)
    

class AddAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')
        admin_id = request.data.get('admin_id')

        if not username or not password or not admin_id:
            return Response({"error": "Thiếu thông tin cần thiết"}, status=status.HTTP_400_BAD_REQUEST)
        
        if models.Account.objects.filter(username=username).exists():
            return Response({"error": "Username đã tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
        
        account = models.Account.objects.create(
            username=username,
            password=make_password(password),
            admin_id=admin_id
        )
        account.save()
        return Response({"message": "Account đã được thêm thành công"}, status=status.HTTP_201_CREATED)
    


class UpdateAccountView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, account_id):
        try:
            account = models.Account.objects.get(id=account_id)
        except models.Account.DoesNotExist:
            return Response({"error": "Account không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        username = request.data.get('username')
        password = request.data.get('password')
        admin_id = request.data.get('admin_id')

        if username:
            if models.Account.objects.filter(username=username).exclude(id=account_id).exists():
                return Response({"error": "Username đã tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
            account.username = username

        if password:
            account.password = make_password(password)

        if admin_id:
            account.admin_id = admin_id

        account.save()
        return Response({"message": "Account đã được cập nhật thành công"}, status=status.HTTP_200_OK)

class DeleteAccountView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, account_id):
        try:
            account = models.Account.objects.get(id=account_id)
        except models.Account.DoesNotExist:
            return Response({"error": "Account không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        account.delete()

        return Response({"message": "Account đã được xóa thành công"}, status=status.HTTP_200_OK)
    
class AddUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        name = request.data.get('name')
        dob = request.data.get('dob')
        score = request.data.get('score', 0)
        preferences = request.data.get('preferences', '')
        account_id = request.data.get('account_id')

        if not email or not name or not dob or not account_id:
            return Response({"error": "Thiếu thông tin cần thiết"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            account = models.Account.objects.get(id=account_id)
        except models.Account.DoesNotExist:
            return Response({"error": "Tài khoản không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        user = models.User.objects.create(
            email=email,
            name=name,
            dob=dob,
            score=score,
            preferences=preferences,
            account=account
        )
        
        user.save()

        return Response({"message": "User đã được thêm thành công"}, status=status.HTTP_201_CREATED)
    
class UpdateUserView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, user_id):
        # Tìm người dùng theo user_id
        try:
            user = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response({"error": "User không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        # Lấy dữ liệu từ request
        email = request.data.get('email', user.email)  # Nếu không có thì giữ giá trị cũ
        name = request.data.get('name', user.name)  # Nếu không có thì giữ giá trị cũ
        dob = request.data.get('dob', user.dob)  # Nếu không có thì giữ giá trị cũ
        score = request.data.get('score', user.score)  # Nếu không có thì giữ giá trị cũ
        preferences = request.data.get('preferences', user.preferences)  # Nếu không có thì giữ giá trị cũ
        account_id = request.data.get('account_id', user.account.id)  # Nếu không có thì giữ giá trị cũ

        # Kiểm tra xem tài khoản có tồn tại không
        try:
            account = models.Account.objects.get(id=account_id)
        except models.Account.DoesNotExist:
            return Response({"error": "Tài khoản không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        # Cập nhật thông tin người dùng
        user.email = email
        user.name = name
        user.dob = dob
        user.score = score
        user.preferences = preferences
        user.account = account  # Cập nhật tài khoản mới

        # Lưu thay đổi
        user.save()

        return Response({"message": "User đã được cập nhật thành công"}, status=status.HTTP_200_OK)
    
class DeleteUserView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, user_id):
        # Tìm người dùng theo user_id
        try:
            user = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response({"error": "User không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        # Xóa người dùng
        user.delete()

        return Response({"message": "User đã được xóa thành công"}, status=status.HTTP_200_OK)