from django.conf import settings
from django.db import models

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="posts")
    title = models.CharField(max_length=200,blank=True,verbose_name="Title")
    caption = models.TextField(max_length=2000,blank=True,verbose_name="Caption")
    image = models.ImageField(upload_to="posts/%Y/%m/",verbose_name="Post Image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Meta:
    ordering = ["-created_at"]
    indexes = [
        models.Index(fields=["-created_at"],name="post_created_idx"),
        models.Index(fields=["author","-created_at"],name="post_author_created_idx")
    ]
    
def __str__(self):
    return f"{self.author.username} - post #{self.title}"


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="comments")
    text = models.TextField(max_length=2000,verbose_name="Comment Text")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["post","created_at"],name="comment_post_date_idx")]
        
    def __str__(self):
        return f"{self.author.username}-{self.text[:30]}"
        
    