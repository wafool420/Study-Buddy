from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    
    CPE = 'CPE'
    CS = 'CS'
    IT = 'IT'

    COURSE_CHOICES = [
        (CPE, 'Computer Engineering'),
        (CS, 'Computer Science'),
        (IT, 'Information Technology'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,   
        related_name='profile'      
    )
    pf_picture = models.ImageField(
        upload_to='profile_pics/',  
        blank=True,
        null=True,    
    )
    bio = models.TextField(
        blank=True,
        null=True
    )
    course_tag = models.CharField(
        max_length=3,
        choices=COURSE_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s profile"

class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    text = models.CharField(max_length=280, blank=True)  
    image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True
    )
    reactions = models.IntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        short = self.text[:30] if self.text else '[image only]'
        return f"{self.user.username}'s post: {short}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.CharField(max_length=150, blank=False)
    reactions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}: {self.text[:30]}"




class Reply(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    text = models.CharField(max_length=150, blank=False)
    reactions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by {self.user.username} on comment {self.comment.id}: {self.text[:30]}"
