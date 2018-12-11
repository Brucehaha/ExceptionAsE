from django.db import models

# Create your models here.


class UserInfo(models.Model):
    """ user table """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    nickname = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    avatar = models.ImageField()
    ctime = models.DateTimeField(verbose_name='created time', auto_now_add=True)
    fans = models.ManyToManyField(to='UserInfo',
                                  related_name='f',
                                  through='UserFans',
                                  through_fields=('user', 'follower'))

    def __str__(self):
        return self.username


class UserFans(models.Model):
    """ user to user """
    user = models.ForeignKey(to='UserInfo',
                             verbose_name='blogger',
                             to_field='nid',
                             related_name='users',
                             on_delete=models.CASCADE)
    follower = models.ForeignKey(to='UserInfo',
                                  to_field='nid',
                                  related_name='followers',
                                  on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Fan'
        verbose_name_plural = 'Fans'
        unique_together = [
            ('user', 'follower'),
        ]


class Blog(models.Model):
    """ Blog info """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    site = models.CharField(max_length=32, unique=True)
    theme = models.CharField(max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Category(models.Model):
    """user's personal categories"""
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=32)
    blog = models.ForeignKey(to='Blog', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=32)
    summary = models.CharField(verbose_name="Article Summary", max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(to='Category',
                                 to_field='nid',
                                 null=True,
                                 on_delete=models.CASCADE)
    blog = models.ForeignKey(to='Blog',
                             to_field='nid',
                             on_delete=models.CASCADE)
    type_choices =[
        (1, "Python"),
        (2, "Linux"),
        (3, "OpenStack"),
        (4, "Golang"),
    ]
    type_id = models.IntegerField(choices=type_choices, default=None)
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    """
    detail content of article
    """
    content = models.TextField()
    article = models.OneToOneField(to='Article', to_field='nid', on_delete=models.CASCADE)


class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.CASCADE)
    tag = models.ForeignKey(to='Tag', to_field='nid', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]


class Tag(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='tag name', max_length=32)
    blog = models.ForeignKey(to='Blog', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UpDown(models.Model):
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(to='Userinfo', to_field='nid', on_delete=models.CASCADE)
    islike = models.BooleanField()

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]


class Comment(models.Model):
    nid = models.BigAutoField(primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey(to='self', to_field='nid', default=None, null=True, blank=True, on_delete=models.SET_NULL)
    article = models.ForeignKey(to='Article', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(to='Userinfo', to_field='nid', on_delete=models.CASCADE)
    content = models.TextField()




