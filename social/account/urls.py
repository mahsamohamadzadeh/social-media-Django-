from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user-profile'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset-password'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='reset-password-done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('confirm/complete/', views.UserPasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='user-follow'),
    path('unfollow/<int:user_id>/', views.UserUnfollowView.as_view(), name='user-unfollow'),
    path('edit-user/', views.UserEditView.as_view(), name='user-edit'),
    ]
