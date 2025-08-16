from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'app_website/index.html'


class AboutView(TemplateView):
    template_name = 'app_website/about.html'


class ContactView(TemplateView):
    template_name = 'app_website/contact.html'
