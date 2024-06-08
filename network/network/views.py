from django.http import JsonResponse
import json
import time
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Case, When, BooleanField, Q, Count, OuterRef, Exists

from .models import User, Follow, Post, Like

from django.core.paginator import Paginator

def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def savepost(request):    
    if request.method == "POST":
        # Load the JSON data sent by the POST request
        data = json.loads(request.body)
        
        # Access the content JSON
        content = data.get('content')
        userid = data.get('userid')

        #Save in db
        try:
            user = User.objects.get(id = userid)
            newpost = Post(poster = user, content = content)
            newpost.save()
            return JsonResponse({"message": "Post saved successfully!", "success": "true"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"message": "User does not exist.", "success": "false"}, status=404)
        except Exception:
            return JsonResponse({"message": "Error saving the post.", "success": "false"}, status=500)        
        # print(newpost)
            
    else:
        # If it's not a POST request, render your index page or handle accordingly
        return render(request, "network/index.html")


def posts(request):

    # Get start and end points
    page_number = int(request.GET.get("page_number") or 1)  
    
    followingflag = int(request.GET.get("followingflag"))
    #print(followingflag) Following flagis to check if we should share all posts or just following posts.
    
    # means all posts
    if followingflag == 0:
        
        userid = request.user.id
        
        if not userid: 
            posts = list(Post.objects.annotate(like_count=Count('liked_post')).values('poster__username', 'poster__id', 'content', 'like_count', 'created_at', 'id').order_by('-created_at'))
        
        else: 
            like_subquery = Like.objects.filter(
            liked_postid=OuterRef('pk'),
                liking_user_id=userid
            )
            
            # Query to get posts with like_count and is_liked flag
            posts = list(
                Post.objects.annotate(
                    like_count=Count('liked_post'),
                    liked=Exists(like_subquery)  # Annotate with a boolean liked flag
                )
                .values(
                    'poster__username',
                    'poster__id',
                    'content',
                    'like_count',
                    'created_at',
                    'id',
                    'liked'  # Include the liked field in the result
                )
                .order_by('-created_at')
            ) 
            
        # convert the QuerySet to a list of dictionaries using values and list
        # print(posts)
        
    # means to display only posts of users being followed. 
    elif followingflag == 1:
        
        # convert the QuerySet to a list of dictionaries using values and list
        userid = int(request.GET.get("userid"))
        
        #Get query set of users that are being followed by tge userid. 
        following_users = Follow.objects.filter(following_user_id=userid).values_list('followed_user_id', flat=True)
        #print(following_users)
        
        #Use this following_users "list" to filter the Post objects. You can do this by using the __in field lookup in Django, which allows you to filter based on whether a field's value is found in a given list.
        #This was adviced by CS50 ai rubber duck


        like_subquery = Like.objects.filter(
            liked_postid=OuterRef('pk'),
                liking_user_id=userid
            )

        posts = list(
            Post.objects.filter(poster__id__in=following_users)
                .annotate(like_count=Count('liked_post'),
                          liked=Exists(like_subquery)
                          )
                .values(
                    'poster__username',
                    'poster__id',
                    'content',
                    'like_count',
                    'created_at',
                    'id',
                    'liked'  # Include the liked field in the result
                    )
                .order_by('-created_at'))
        # print(posts)

    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)
    
    has_next = page_obj.has_next()
    # print(has_next)
    
    has_previous = page_obj.has_previous()
    # print(has_previous)
    
    if has_next:
        next_page_number = page_obj.next_page_number()
        # print(next_page_number)
    if not has_next:
        next_page_number = -1
    
    if has_previous:
        previous_page_number = page_obj.previous_page_number()
        # print(previous_page_number)
    if not has_previous:
        previous_page_number = -1


    data = {
    'page_obj': page_obj.object_list,
    'page_number': page_obj.number,
    'num_pages' : page_obj.paginator.num_pages,
    'has_next' : has_next,
    'has_previous': has_previous,
    'next_page_number': next_page_number,
    'previous_page_number': previous_page_number
    }
    

    # To allow non-dict objects to be serialized use safe false
    return JsonResponse(data, safe=False, status=200)

def profile(request):

    profileid = int(request.GET.get("profileid"))
    # Get start and end points
    page_number = int(request.GET.get("page_number") or 1) 
    
    userid = request.GET.get("userid")
    if userid == 'null':
        # user 0 does not exist in DB I used here as a phantom user to pass it wihtout having issues
        userid = 0        
    else: 
        userid = int(userid)
        
    
    # convert the QuerySet to a list of dictionaries using values and list   
    # The Q object in Django allows you to make complex queries with the ORM. In this case, Q(liked_post__liking_user_id=userid) is creating a query that checks if the liking_user_id of the liked_post is equal to userid.
    # The double underscore (__) in liked_post__liking_user_id is used to specify relationships in Django. It's saying "access the liking_user_id field on the liked_post related object".
    # So, if you have a Post object and it has a related Like object (through the liked_post field), this Q object is checking if the liking_user_id on that Like object is equal to userid.
    # this approach was suggested by CS50 AI. 
        
    # posts = list(Post.objects.filter(poster_id=profileid).annotate(
    #     like_count=Count('liked_post'),
        
    #     liked=Case(
    #     When(Q(liked_post__liking_user_id=userid), then=True),
    #     default=False,
    #     output_field=BooleanField()))
        
    #     .values('poster__username','poster__id', 'content', 'like_count', 'created_at', 'id', 'liked').order_by('-created_at'))
    
    # Had to change the approach because it was creating duplicate values. It's better to use a subquery and outerref
    # Subquery to check if the current post is liked by the user
    
    like_subquery = Like.objects.filter(
        liked_postid=OuterRef('pk'),
        liking_user_id=userid
    )

    # Query to get posts with like_count and is_liked flag
    posts = list(
        Post.objects.filter(poster_id=profileid)
        .annotate(
            like_count=Count('liked_post'),
            liked=Exists(like_subquery)  # Annotate with a boolean liked flag
        )
        .values(
            'poster__username',
            'poster__id',
            'content',
            'like_count',
            'created_at',
            'id',
            'liked'  # Include the liked field in the result
        )
        .order_by('-created_at')
    )
    
    # followers of user. Using count() to count numnber of followers
    number_followers = Follow.objects.filter(followed_user_id=profileid).count()
    
    # following
    number_following = Follow.objects.filter(following_user_id=profileid).count()
    
    print(f"followers: {number_followers} following: {number_following}")    
    
    # Checking if user logged in is following the profile clicked
    isfollowing = Follow.objects.filter(followed_user_id=profileid, following_user_id=userid)
    
    if not isfollowing:
        followed = 0
        print("Not following")
    else:
        followed = 1
        print("following")
    
    # Paginator
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)
    
    has_next = page_obj.has_next()
    # print(has_next)
    
    has_previous = page_obj.has_previous()
    # print(has_previous)
    
    if has_next:
        next_page_number = page_obj.next_page_number()
        # print(next_page_number)
    if not has_next:
        next_page_number = -1
    
    if has_previous:
        previous_page_number = page_obj.previous_page_number()
        # print(previous_page_number)
    if not has_previous:
        previous_page_number = -1 
        
    data = {
    'posts': page_obj.object_list,
    'followers': number_followers,
    'following': number_following,
    'followed' : followed,
    'page_number': page_obj.number,
    'num_pages' : page_obj.paginator.num_pages,
    'has_next' : has_next,
    'has_previous': has_previous,
    'next_page_number': next_page_number,
    'previous_page_number': previous_page_number
    }
    
    # To allow non-dict objects to be serialized use safe false
    return JsonResponse(data, safe=False, status=200)


def checkauth(request):   
    if request.session.session_key:
        # User is authenticated
        return JsonResponse({'message': 'Authenticated'}, status=200)
    else:
        # User is not authenticated
        print("Not authenticated")
        return JsonResponse({'message': 'Not authenticated'}, status=200)    
    

def followunfollow(request):
    profileid = int(request.GET.get("profileid"))
    userid = int(request.GET.get("userid"))
    followed = int(request.GET.get("followed"))
    try:
        following_user = User.objects.get(id=userid)
        followed_user = User.objects.get(id=profileid)
        
    except:
        return JsonResponse({'message': 'Users/s do not exist'}, status=400)  
    
    # If followed == 0 it means the user wants to follow this profile now
    if followed == 0:
        follow = Follow(following_user_id=following_user, followed_user_id=followed_user)
        follow.save()
        
        return JsonResponse({'message': 'Logged user is following this profile'}, status=200)  
    
    # if followed == 1 it means the user wants to unfollow this profile
    elif followed == 1: 
        deletefollow = Follow.objects.filter(followed_user_id=profileid, following_user_id=userid)
        deletefollow.delete()
        
        return JsonResponse({'message': 'Logged user is NOT following this profile'}, status=200)  

def edit(request):
    
    
    if request.method == "POST":

        #Save in db
        try:
            # Load the JSON data sent by the POST request
            data = json.loads(request.body)
            
            # Access the content JSON
            content = data.get('content')
            userid = data.get('userid')
            postid = data.get('postid')

            post = Post.objects.filter(id=postid, poster_id=userid)
                
            if post.exists():
                    post.update(content=content)
                    return JsonResponse({"message": "Post updated successfully", "success": "true"}, status=200)
            else:
                return JsonResponse({"message": "Post does not exist for the registered user", "success": "false"}, status=404)
        
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON", "success": "false"}, status=400)            

    else: 
        postid = int(request.GET.get("postid"))
        userid = int(request.GET.get("userid"))
        
        print(userid)

        try:
            # filtering with postid and userid to validate the post indeed belongs to the user if it's returned it means is the user's post
            content = list(Post.objects.filter(id=postid, poster_id=userid).values_list('content', flat=True))
            if not content:
                raise Post.DoesNotExist
        
            data = {
                'content': content[0]
            }
            
            return JsonResponse(data, safe=False, status=200)
        
        except Post.DoesNotExist:
            return JsonResponse({"message": "Post does not exist for the registered user", "success": False}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e), "success": False}, status=500)
        
        
        
def likeunlike(request):
    
    postid = int(request.GET.get("postid"))
    userid = int(request.GET.get("userid"))
    liked = request.GET.get("liked")
    
    boolean_value = liked.lower().strip() == 'true'
    liked = int(boolean_value)
    
    
    try:
        liking_user = User.objects.get(id=userid)
        liked_post = Post.objects.get(id=postid)
        
    except:
        return JsonResponse({'message': 'Users/s do not exist'}, status=400)  
    
    # If liked == 0 it means the user wants to like the post
    if liked == 0:
        like = Like(liking_user_id=liking_user, liked_postid=liked_post)
        like.save()
        
        return JsonResponse({'message': 'Logged user liked this post'}, status=200)  
    
    # if liked == 1 it means the user wants to unlike the post
    elif liked == 1: 
        deletelike = Like.objects.filter(liked_postid=liked_post, liking_user_id=liking_user)
        deletelike.delete()
        
        return JsonResponse({'message': 'Logged user unliked this post'}, status=200)          


