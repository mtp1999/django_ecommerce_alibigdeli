from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app_account.forms import CostumeUserCreationForm, LoginForm
from django.views import View
from django.views.generic import TemplateView
from app_account.models import User
from app_account.tasks import generate_password_reset_token, send_email_reset_password
from django.contrib.auth.mixins import LoginRequiredMixin
import jwt
from django.conf import settings
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class LogInView(LoginView):
    redirect_authenticated_user = True
    template_name = "app_account/login.html"

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, "welcome!")
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return redirect("app_website:index")
            else:
                messages.error(request, "wrong information")
                return redirect("app_account:login")
        else:
            messages.error(request, "wrong information")
            return redirect("app_account:login")


class LogoutView(View):
    def get(self, request):
        try:
            logout(request)
            messages.success(request, "logout successfully!")
            return redirect("app_account:login")
        except:
            messages.error(request, "logout failed!")
            return redirect("app_account:home")


class ResetPasswordSendEmailView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        token = generate_password_reset_token(user)
        reset_url = request.build_absolute_uri(f"/accounts/reset-password/{token}/")
        send_email_reset_password.delay(email=user.email, reset_url=reset_url)
        return redirect("app_account:reset_email_sent")


class ResetPasswordSentEmailView(LoginRequiredMixin, TemplateView):
    template_name = 'app_account/password_reset_email_sent.html'


class ResetPasswordView(LoginRequiredMixin, View):
    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])

            # extra security check
            if user.password != payload["pwd_hash"]:
                return render(request, "app_account/password_reset_invalid.html")

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return render(request, "app_account/password_reset_invalid.html")

        return render(request, "app_account/password_reset_form.html", {"token": token})

    def post(self, request, token):
        user = request.user
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('app_account:reset_password', token=token)

        try:
            password_validation.validate_password(new_password, user)
            user.set_password(new_password)
            user.save()
        except ValidationError as e:
            messages.error(request, e.messages)
            return redirect('app_account:reset_password', token=token)

        return render(request, "app_account/password_reset_done.html")


# def reset_password(request, token):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         user = User.objects.get(id=payload["user_id"])
#
#         # extra security check
#         if user.password != payload["pwd_hash"]:
#             return render(request, "app_account/password_reset_invalid.html")
#
#     except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
#         return render(request, "app_account/password_reset_invalid.html")
#
#     if request.method == "POST":
#         new_password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")
#
#         if new_password != confirm_password:
#             return render(request, "app_account/password_reset_form.html", {
#                 "error": "Passwords do not match.",
#                 "token": token
#             })
#
#         try:
#             password_validation.validate_password(new_password, user)
#             user.set_password(new_password)
#             user.save()
#         except ValidationError as e:
#             return render(request, "app_account/password_reset_form.html", {
#                 "error": e.messages,
#             })
#
#         return render(request, "app_account/password_reset_done.html")
#
#     return render(request, "app_account/password_reset_form.html", {"token": token})


# def signup_view(request):
#     if request.user.is_authenticated:
#         return redirect('app_blog:home')
#     if request.method == 'POST':
#         form = CostumeUserCreationForm(request.POST)
#         if form.is_valid():
#             user = User.objects.filter(email=form.cleaned_data['email'])
#             if user:
#                 messages.error(request, 'Account exists,Try Again')
#                 return redirect('app_account:signup')
#             form.save()
#             messages.success(request, 'Sign Up Successfully')
#             return redirect('app_account:login')
#         else:
#             messages.error(request, 'Wrong Information,Try Again')
#             return redirect('app_account:signup')
#
#     return render(request, 'app_account/signup.html', {'form': CostumeUserCreationForm()})
