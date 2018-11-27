from django.test import TestCase
from . import models

# Create your tests here.

class ArticleTestCase(TestCase):
    def setUp(self):
        models.Article.create()
