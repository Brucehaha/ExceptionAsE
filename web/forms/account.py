from .base import MyBaseForm
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.exceptions import ValidationError


class LoginForm(MyBaseForm):
    email = fields.EmailField()
    password = fields.CharField()
    check_code = fields.CharField(
        error_messages={'required': "code could not be empty"}
    )
    month = fields.IntegerField(required=False)

    def clean_check_code(self):
        session_code = self.request.session.get('recapcha_code').upper()
        post_code = self.cleaned_data['check_code'].upper()
        print('test', post_code)
        if session_code != post_code:
            raise ValidationError(message="invalid code", code='invalid')
        return post_code
