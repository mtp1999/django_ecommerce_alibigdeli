from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from app_website.forms import ContactForm, NewsletterForm


class IndexView(CreateView):
    template_name = 'app_website/index.html'
    form_class = NewsletterForm

    def get_success_url(self):
        messages.success(self.request, "ایمیل شما با موفقیت ثبت شد.")
        return reverse_lazy("app_website:index")

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return redirect("app_website:index")


class AboutView(TemplateView):
    template_name = 'app_website/about.html'


class ContactView(CreateView):
    template_name = 'app_website/contact.html'
    form_class = ContactForm

    def get_success_url(self):
        messages.success(self.request, "پیام شما ثبت و بزودی پاسخ آن برای شما ارسال میگردد!")
        return reverse_lazy("app_website:index")

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return redirect("app_website:contact")
