from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect

from post.models import Tag,Stream,Follow,Post,Likes
from post.forms import NewPostForm
from django.urls import reverse
from userauths.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from comment.models import Comment
from comment.forms import CommentForm






def index(request):
    user = request.user
    user = request.user
    all_users = User.objects.all()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    profile = Profile.objects.all()

    posts = Stream.objects.filter(user=user)
    group_ids = []

    
    for post in posts:
        group_ids.append(post.post_id)
        
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)


    context = {
        'post_items': post_items,
        'follow_status': follow_status,
        'profile': profile,
        'all_users': all_users,
        # 'users_paginator': users_paginator,
    }
    return render(request, 'index.html', context)



def Newpost(request):
    user=request.user.id
    tags_objs = []

    if request.method == "POST":
        form = NewPostForm(request.POST,request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            tags_list = list(tag_form.split(','))

            for tag in tags_list:
                t,created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p,created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tags.set(tags_objs)
            p.save() 
            return redirect('index')
    else:
        form = NewPostForm()
    context = {
        'form':form
    }
    return render(request, 'newpost.html',context)

def PostDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-detail', args=[post.id]))
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }

    return render(request, 'post-details.html', context)

def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    context = {
        'posts': posts,
        'tag': tag,

        }
    return render(request, 'tags.html', context)



def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        liked = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        liked = Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save()
    
    return HttpResponseRedirect(reverse('post-detail', args=[post_id]))

def favourite(request,post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-detail', args=[post_id]))      


