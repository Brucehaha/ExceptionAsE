from django.db import models
from repository.models import UserInfo


#  user to role: user, role
# role: caption( customer, admin, manager, ceo)
# Permission: caption, url, menu
# menu: caption, self(FK)
# action:  caption, method(GET POST PUT DELETE)
# Permission2action: p, a,
# Permission2action2role: p2a(FK), r(FK)


class Role(models.Model):
    caption = models.CharField(max_length=32)

    def __str__(self):
        return self.caption


class User2Role(models.Model):
    u = models.ForeignKey(to=UserInfo, to_field='nid', on_delete=models.CASCADE)
    r = models.ForeignKey(to=Role, on_delete=models.CASCADE)

    def __str__(self):
        return '%s-%s' %(self.u, self.r)


class Menu(models.Model):
    caption = models.CharField(max_length=32)
    parent = models.ForeignKey('self', related_name='p', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s-%s' %(self.caption, self.parent)


class Permission(models.Model):
    caption = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    menu = models.ForeignKey(to=Menu, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Permission URL"

    def __str__(self):
        return str(self.url)


class Action(models.Model):
    caption = models.CharField(max_length=32)
    method = models.CharField(max_length=32)

    def __str__(self):
        return str(self.caption)


class Permission2Action(models.Model):
    p = models.ForeignKey(Permission, on_delete=models.CASCADE)
    a = models.ForeignKey(Action, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Permission List"
        unique_together = [
            ('p', 'a'),
        ]

    def __str__(self):
        return '%s-%s' %(self.p, self.a)


class Permission2Action2Role(models.Model):
    p2a = models.ForeignKey(Permission2Action, on_delete=models.CASCADE)
    r = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Role's Permission"

    def __str__(self):
        return '%s-%s' %(self.r, self.p2a)




