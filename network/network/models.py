from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Follow(models.Model):
    following_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    followed_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_user")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # auto_now_add set the field's value to the current date and time when an instance of the model is created. 
    
    def __str__(self):
        return f"User Following: {self.following_user_id} -> Followed: {self.followed_user_id} - {self.created_at}"
    

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    content = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User posting: {self.poster} Content: {self.content} - {self.created_at}"
    
  
class Like(models.Model):
    liking_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liking_user")
    liked_postid = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # auto_now_add set the field's value to the current date and time when an instance of the model is created. 
    
    def __str__(self):
        return f"User {self.liking_user_id} liked {self.liked_postid} on {self.created_at}"
     
 
  
''' NOT UPDATED WITH MODEL LIKE
Graphic help to see the DB    
https://dbdiagram.io/d

// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table follows {
  following_user_id integer
  followed_user_id integer
  created_at timestamp 
}

Table users {
  id integer [primary key]
  username varchar
  created_at timestamp
}

Table posts {
  id integer [primary key]
  user_id integer
  content text [note: 'Content of the post']
  likes integer
  created_at timestamp
}

// Table like {
//   id integer [primary key]
//   liker_user_id integer
//   post_id integer
//   likes integer //0 by default
//   created_at timestamp
// }

Ref: posts.user_id > users.id // many-to-one

// Ref: users.id < like.liker_user_id 

// Ref: like.post_id > posts.id // many-to-one

Ref: users.id < follows.following_user_id

Ref: users.id < follows.followed_user_id
'''    