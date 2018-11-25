from django.db import models

# Create your models here.


class UserInfo(models.model):
    """
    user table
    """
    nid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    nickname = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    avatar = models.ImageField()
    ctime = models.DateTimeField(verbose_name='Created time')
    fans = models.ManyToManyField(to='UserInfo',
                                  related_name='f',
                                  through_fields=('user', 'follower'))


class UserFans(models.model):
    """
    user to user
    """
    user = models.ForeignKey(to='UserInfo',
                             verbose_name='blogger',
                             to_fields='uid',
                             related_name='users')
    followers = models.ForeignKey(to='UserInfo',
                                  verbose_name='followers',
                                  to_fields='uid',
                                  related_name='followers')

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]

class Blog
class Category(models.Model):
    """
    user's personal categories
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    blog = models.ForeignKey(to='Blog', to_fields='nid')

class IsLike(models.model):
    Ar



