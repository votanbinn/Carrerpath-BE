from django.urls import path
from . import views

urlpatterns = [
    path('running/', views.running, name='running'),
    path('Account/', views.AccountViewSet.as_view({'get': 'list'}), name='check account'),
    path('Admin/', views.AdminUserViewSet.as_view({'get': 'list'}), name='check admin'),
    path('Article/', views.ArticleViewSet.as_view({'get': 'list'}), name='check article'),
    path('user/', views.UserViewSet.as_view({'get': 'list'}), name='check user'),
    path('Expert/', views.ExpertViewSet.as_view({'get': 'list'}), name='check expert'),
    path('Consultation/', views.ConsultationViewSet.as_view({'get': 'list'}), name='check consultation'),
    path('Test/', views.TestViewSet.as_view({'get': 'list'}), name='check test'),
    path('Result/', views.ResultViewSet.as_view({'get': 'list'}), name='check result'),
    path('Forum/', views.ForumViewSet.as_view({'get': 'list'}), name='check forum'),
    path('login/', views.LoginView.as_view(), name='check login'),
    path('logout/', views.LogoutView.as_view(), name='check logout'),
    path('AddAccount/', views.AddAccountView.as_view(), name='check add account'),
    path('UpdateAccount/<int:account_id>/', views.UpdateAccountView.as_view(), name='check update account'),
    path('DeleteAccount/<int:account_id>/', views.DeleteAccountView.as_view(), name='check delete account'),
    path('AddUser/', views.AddUserView.as_view(), name='check add user'),
    path('UpdateUser/<int:user_id>/', views.UpdateUserView.as_view(), name='check update user'),
    path('DeleteUser/<int:user_id>/', views.DeleteUserView.as_view(), name='check delete user'),
]