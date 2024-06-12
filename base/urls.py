from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('scanne/<str:code>/', views.scanner, name="scanne"),
    path('add_student/', views.add_student, name="add_student"),
    path('scan/', views.scan),
    path('process_qr_code/', views.process_qr_code, name='process_qr_code'),
    path('api/register_user', views.user_registration),   
    path('api/login', views.user_login),
    path('api/logout', views.logout_view, name='logout'),
    path('api/signup', views.signup), # Use this as login
    path('api/login2', views.login_),
    path('api/get_current_user/', views.get_current_user),
    path('api/parent_detail/<int:pk>/', views.parent_detail),
    path('api/parent_detail_by_name/<str:name>/', views.parent_detail_by_name),
    path('api/parent_list/', views.parent_list),
    path('api/transactionHistory/<str:pk>/', views.transactionHistory),
    path('api/deposit/<str:student_id>/', views.update_balance_parent),
    path('api/add_students/', views.StudentListCreateView.as_view(), name='student-list-create'),
    path('api/students/', views.student_list),
    path('add_child_to_parent/<int:parent_id>/', views.add_child_to_parent, name='add_child_to_parent'),
    path('api/add_student_api/', views.add_student_api, name='add_student'),

    path('api2/register/', views.RegisterAPIView.as_view(), name='register'),
    path('api2/login/', views.LoginAPIView.as_view(), name='login'),



    path('receive_qr_code/', views.receive_qr_code, name='receive_qr_code'),
    path('api/get_student_data/<str:student_id>/', views.get_student_data, name='get_student_data'),
    path('api/update_balance/<str:student_id>/', views.update_balance_agent, name="update_balance"),
    path('api/user_login/', views.user_login),
    path('stk/', views.stk),

    path('accesstoken/', views.get_access_token, name='get_access_token'),
    path('stkpush/', views.initiate_stk_push, name='initiate_stk_push'),
    path('api/trans/', views.TransactionInit.as_view(), name='transact'),

    path("ws/some_path/", views.websocket_path),

    path('initiate_payment/', views.initiate_payment, name='initiate_payment'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),
    # path('camera_feed/', views.camera_feed, name='camera_feed'),
    # path('qr_code_scanner/', views.qr_code_scanner, name='qr_code_scanner'),
]

