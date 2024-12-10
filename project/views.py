from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login  # Import the login function
from django.http import HttpResponseForbidden
from .models import Post, University, Region, PostImage, Comment, Reply
from .forms import PostForm, CustomUserCreationForm, CustomAuthenticationForm

# Homepage View
@login_required
def index(request):
    # Fetch posts that are not tied to any specific university or region
    posts = Post.objects.filter(university=None, region=None).order_by('-created_at')
    return render(request, 'forum/all_schools.html', {'posts': posts})

# All Schools Forum
@login_required
def all_schools_forum(request):
    posts = Post.objects.filter(university=None, region=None).order_by('-created_at')
    return render(request, 'forum/all_schools.html', {'posts': posts})

# My Region Forum
@login_required
def region_forum(request):
    if not request.user.region:
        return HttpResponseForbidden("You are not associated with any region.")
    posts = Post.objects.filter(region=request.user.region).order_by('-created_at')
    return render(request, 'forum/region.html', {'posts': posts, 'region': request.user.region})

# My School Forum
@login_required
def school_forum(request):
    if not request.user.university:
        return HttpResponseForbidden("You are not associated with any university.")
    posts = Post.objects.filter(university=request.user.university).order_by('-created_at')
    return render(request, 'forum/school.html', {'posts': posts, 'university': request.user.university})

# Create Post View
@login_required
def create_post(request, forum_type):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if forum_type == "region" and request.user.region:
                post.region = request.user.region
            elif forum_type == "school" and request.user.university:
                post.university = request.user.university
            post.save()

            # Handle multiple image uploads
            for image in request.FILES.getlist('images'):
                PostImage.objects.create(post=post, image=image)

            # Redirect to the appropriate forum
            if forum_type == "region":
                return redirect('region_forum')
            elif forum_type == "school":
                return redirect('school_forum')
            else:
                return redirect('index')
    else:
        form = PostForm()
    return render(request, 'forum/create_post.html', {'form': form, 'forum_type': forum_type})

# Signup View
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email_domain = user.email.split('@')[1]
            university_name = email_domain.split('.')[0]
            university = University.objects.filter(name__iexact=university_name).first()
            if university:
                user.university = university
                user.region = university.region
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST.get('content')
        comment_id = request.POST.get('comment_id')
        if comment_id:  # This is a reply to a comment
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(comment=comment, author=request.user, content=content)
        else:  # This is a new comment
            Comment.objects.create(post=post, author=request.user, content=content)
        return redirect('post_detail', post_id=post.id)
    return render(request, 'forum/post_detail.html', {'post': post})

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

@csrf_exempt
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        Comment.objects.create(post=post, author=request.user, content=content)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def toggle_like(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content_type = data.get("content_type")
            object_id = data.get("object_id")
            
            if not content_type or not object_id:
                return JsonResponse({"error": "Missing content_type or object_id"}, status=400)
            
            model = ContentType.objects.get(model=content_type).model_class()
            obj = model.objects.get(id=object_id)
            
            user = request.user
            if user in obj.likes.all():
                obj.likes.remove(user)
                liked = False
            else:
                obj.likes.add(user)
                liked = True
            
            return JsonResponse({"liked": liked, "like_count": obj.likes.count()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

from django.db.models import Q

def search_page(request):
    """Display the search page."""
    recommended_keywords = ["초코파이", "초코파이 먹고", "초코파이 맛있다"]
    return render(request, 'forum/search.html', {'recommended_keywords': recommended_keywords})

@login_required
def search_results(request):
    """Display the search results."""
    query = request.GET.get('q', '').strip()
    user = request.user

    if not query:
        return redirect('search_page')

    # Filter posts based on the user's access level
    if user.university and user.region:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            Q(university=user.university) | Q(region=user.region) | Q(university=None, region=None)
        ).distinct()
    elif user.university:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            Q(university=user.university) | Q(university=None)
        ).distinct()
    elif user.region:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            Q(region=user.region) | Q(region=None)
        ).distinct()
    else:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            university=None,
            region=None
        ).distinct()

    return render(request, 'forum/search_results.html', {'posts': posts, 'query': query})

from django.contrib.auth import logout

@login_required
def profile_page(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def delete_account(request):
    user = request.user
    user.is_active = False  # Mark the account as inactive
    user.save()
    logout(request)  # Log the user out after deactivation
    return redirect('index')  # Redirect to the homepage

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import MessageRoom
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def create_message_room(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if receiver == request.user:
        return HttpResponseForbidden("You cannot message yourself.")
    room, created = MessageRoom.objects.get_or_create(
        creator=request.user,
        receiver=receiver,
    )
    return redirect('message_room', room_id=room.id)

from django.shortcuts import render
from .models import MessageRoom, Message

@login_required
def message_room(request, room_id):
    room = get_object_or_404(MessageRoom, id=room_id)
    if request.user not in [room.creator, room.receiver]:
        return HttpResponseForbidden("You are not part of this room.")
    
    if request.method == "POST":
        content = request.POST.get("content")
        Message.objects.create(room=room, sender=request.user, content=content)
        return redirect('message_room', room_id=room.id)

    messages = room.messages.order_by('timestamp')
    return render(request, 'forum/message_room.html', {'room': room, 'messages': messages})

from .models import Comment, Reply
from itertools import chain
from django.db.models import F

@login_required
def messages_list(request):
    # Fetch message rooms
    created_rooms = MessageRoom.objects.filter(creator=request.user).annotate(
        timestamp=F('created_at'), type=F('creator')
    )
    received_rooms = MessageRoom.objects.filter(receiver=request.user).annotate(
        timestamp=F('created_at'), type=F('receiver')
    )
    rooms = created_rooms | received_rooms
    for room in rooms:
        room.item_type = "MessageRoom"  # Explicitly set the type

    # Fetch comments where the user is the post author, excluding self-comments
    comments = Comment.objects.filter(post__author=request.user).exclude(author=request.user).annotate(
        timestamp=F('created_at'), type=F('author')
    )
    for comment in comments:
        comment.item_type = "Comment"

    # Fetch replies where the user is the comment author, excluding self-replies
    replies = Reply.objects.filter(comment__author=request.user).exclude(author=request.user).annotate(
        timestamp=F('created_at'), type=F('author')
    )
    for reply in replies:
        reply.item_type = "Reply"

    # Combine all items and order by timestamp
    items = sorted(
        chain(rooms, comments, replies),
        key=lambda x: x.timestamp,
        reverse=True  # Newest first
    )

    return render(request, 'forum/messages_list.html', {'items': items})

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure the current user is the author
    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()

            # Handle image updates if provided
            if request.FILES.getlist('images'):
                post.images.all().delete()  # Remove existing images
                for image in request.FILES.getlist('images'):
                    PostImage.objects.create(post=post, image=image)

            return redirect('post_detail', post_id=post.id)
    else:
        # Pre-fill the form with the existing post data
        form = PostForm(instance=post)

    return render(request, 'forum/edit_post.html', {'form': form, 'post': post})

from django.http import HttpResponseForbidden

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure the user is the author
    if request.user != comment.author:
        return HttpResponseForbidden("You are not allowed to edit this comment.")

    if request.method == "POST":
        content = request.POST.get('content')
        comment.content = content
        comment.save()
        return redirect('post_detail', post_id=comment.post.id)

@login_required
def edit_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    # Ensure the user is the author
    if request.user != reply.author:
        return HttpResponseForbidden("You are not allowed to edit this reply.")

    if request.method == "POST":
        content = request.POST.get('content')
        reply.content = content
        reply.save()
        return redirect('post_detail', post_id=reply.comment.post.id)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Ensure the user is the author
    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    post.delete()
    return redirect('index')  # Redirect to the homepage or forum after deletion

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure the user is the author
    if request.user != comment.author:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    post_id = comment.post.id
    comment.delete()
    return redirect('post_detail', post_id=post_id)  # Redirect to the post detail page

@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    # Ensure the user is the author
    if request.user != reply.author:
        return HttpResponseForbidden("You are not allowed to delete this reply.")

    post_id = reply.comment.post.id
    reply.delete()
    return redirect('post_detail', post_id=post_id)  # Redirect to the post detail page
