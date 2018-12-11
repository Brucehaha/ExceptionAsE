from django.forms import Form
from django.forms import widgets
from django.forms import fields
from repository import models
from django.core.exceptions import ValidationError


class ArticleForm(Form):
    title = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'TITLE'})
    )
    summary = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'SUMMARY'})
    )
    content = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 'kind-editor'})
    )
    type_id = fields.IntegerField(
        widget=widgets.RadioSelect(choices=models.Article.type_choices, attrs={'class': "form-radio"}),
        label="Type"
    )
    category_id = fields.ChoiceField(
        choices=[],
        widget=widgets.RadioSelect(attrs={'class': "form-radio"}),
        label="Category",
    )
    tags = fields.MultipleChoiceField(
        choices=[],
        widget=widgets.CheckboxSelectMultiple(attrs={'class': "form-radio"})
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        blog_id = request.session['user_info']['blog__nid']
        self.fields['category_id'].choices = models.Category.objects.filter(blog_id=blog_id).values_list('nid', 'title')
        self.fields['tags'].choices = models.Tag.objects.filter(blog_id=blog_id).values_list('nid', 'title')
