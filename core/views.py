from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.http import Http404
from .utils import update_views
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def home_page(request):

    username = request.user.username

    categories = Category.objects.all()

    posts = Post.objects.all()

    num_posts = Post.objects.all().count()
    
    num_users = User.objects.all().count()
    
    num_categories = categories.count()

    authors = Author.objects.all()
    
    try:
        last_post = Post.objects.latest("date")
    except:
        last_post = []

    context = {
        'posts': posts,
        'categories': categories,
        'num_posts': num_posts,
        'num_users': num_users,
        'num_categories': num_categories,
        'last_post': last_post,
        'title': 'Home page',
        'authors': authors,
        'username': username,
    }

    return render(request, 'home_page.html', context=context)


def posts_page(request, slug):

    category = get_object_or_404(Category, slug=slug)

    # getting posts specify to definetely category
    posts = Post.objects.filter(approved=True, cat=category)

    paginator = Paginator(posts, 5)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    
    except PageNotAnInteger:
        posts = paginator.page(1)
    
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'categories': category,
        'title': 'Topic'
    }

    return render(request, 'posts_page.html', context=context)


def detail_page(request, slug):

    # вызывает метод get для получения объекта из бд по переданным аргументам
    post = get_object_or_404(Post, slug=slug)
    
    posts = Post.objects.all()
    author = Author.objects.get(user=request.user)      # getting author by comment with request, who make comment

    if 'comment-form' in request.POST:

        comment = request.POST.get('comment')

        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)

        post.comments.add(new_comment.id)

    if 'reply-form' in request.POST:

        reply = request.POST.get('reply')

        comment_id = request.POST.get('comment-id')
        comment_obj = Comment.objects.get(id=comment_id)
        
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply)

        comment_obj.replies.add(new_reply.id)
            

    # getting hits from specify post
    update_views(request, post)

    context = {
        'post': post,
        'posts': posts,
    }

    return render(request, 'detail_page.html',context=context)



@login_required
def create_post(request):

    form = PostForm(request.POST or None)       # форма, либо запрос метода пост, либо ничего

    if request.method == "POST":                # если запрос равен пост

        if form.is_valid():                     # начинается проверка на валидность формы 

            print("\n\n its valid")

            author = Author.objects.get(user=request.user)  # получение автора, который делал запрос

            new_post = form.save(commit=False)      # commit - it's property for specifying that form will be saved in memory but not in database
            new_post.user = author
            new_post.save()

            form.save_m2m()

            return redirect("home_page")

    context = {
        'form': form,
        'title': 'Create New Post'
    }

    return render(request, "create_post.html", context=context)


def latests_posts(request):

    posts = Post.objects.all().filter(approved=True)[:10]   # getting approved, latest 10 posts

    context = {
        'posts': posts,
        'title': 'Latest 10 posts'
    }

    return render(request, 'latests_posts.html', context=context)


def search_page(request):

    return render(request, 'search_page.html')


def local_cabinet(request, slug_us):

    user_id = request.user.id

    forumuser = Author.objects.get(slug=slug_us)

    # get_user = request.user.author

    form = ForumUserForm(instance=forumuser)

    if request.method == 'POST':
       form = ForumUserForm(request.POST, request.FILES, instance=forumuser) 
       if form.is_valid:
           form.save()

    context = {

        'forumuser': forumuser,
        'form': form,

    }

    return render(request, 'local_cabinet.html', context=context)