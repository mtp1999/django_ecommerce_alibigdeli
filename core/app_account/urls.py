from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app_account import views

app_name = "app_account"

urlpatterns = [
    path("login/", views.LogInView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # path('signup/', views.signup_view, name='signup'),

    # reset password
    path("reset-password-send-email/", views.ResetPasswordSendEmailView.as_view(), name="reset_password_send_email"),
    path("reset-password/<str:token>/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("reset-email-sent/", views.ResetPasswordSentEmailView.as_view(), name="reset_email_sent"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
