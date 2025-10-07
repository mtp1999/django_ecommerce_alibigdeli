from django.contrib import messages


class MessageMixin:
    """
    Mixin to add success/error/info messages in CBVs
    """

    success_message = None
    error_message = None

    def form_valid(self, form):
        """Called when a form is valid"""
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        """Called when a form is invalid"""
        response = super().form_invalid(form)
        messages.error(self.request, form.errors)
        return response
