from django import forms


class MyBaseForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(MyBaseForm, self).__init__(*args, **kwargs)

