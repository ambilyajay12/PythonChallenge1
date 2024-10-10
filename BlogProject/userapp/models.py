from django.db import models
from django.utils import timezone


# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.CharField(max_length=300)
    contactno = models.IntegerField()
    password = models.CharField(max_length=200)
    confpassword = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.username)

class loginTable(models.Model):
    username = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.CharField(max_length=300)
    contactno = models.IntegerField()
    password = models.CharField(max_length=200)
    confpassword = models.CharField(max_length=200)
    type=models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.username)

class BlogPost(models.Model):
    title=models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to='post.media')
    content=models.CharField(max_length=500)
    def __str__(self):
        return '{}'.format(self.title)

class UserPosts(models.Model):
    username = models.CharField(max_length=100,null=True)
    title = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='post.media')
    content = models.CharField(max_length=500)

    def __str__(self):
        return '{}'.format(self.username)

# class BlogComment(models.Model):
#     blogpost_connected = models.ForeignKey(
#         BlogPost, related_name='comments', on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = TextField()
#     date_posted = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return str(self.author) + ', ' + self.blogpost_connected.title[:40]
class BlogComment(models.Model):
    blogid = models.IntegerField()
    username = models.CharField(max_length=100, null=True)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    postedby_username= models.CharField(max_length=100, null=True)
    comment= models.CharField(max_length=600,null=True)
    date_cmnt_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}'.format(self.blogid)

class BlockedUsers(models.Model):
    username = models.CharField(max_length=100, null=True)
    adminname = models.CharField(max_length=100, null=True)
    blocked_status= models.CharField(max_length=100, null=True)

    def __str__(self):
        return '{}'.format(self.username)