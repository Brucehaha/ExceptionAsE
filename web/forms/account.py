from .base import MyBaseForm
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.exceptions import ValidationError


class LoginForm(MyBaseForm):
    email = fields.EmailField()
    password = fields.CharField()
    check_code = fields.CharField()

    def clean_check_code(self):
        try:
            session_code = self.request.session.get('recapcha_code').upper()
            post_code = self.request.POST.get('check_code').upper
            if session_code != post_code:
                raise ValidationError(message="invalid code", code='invalid')