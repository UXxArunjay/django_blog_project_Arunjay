# Import necessary modules
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.urls import path
import requests
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_blog_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# ------------------------- MODELS -------------------------
# Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    country = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Comment Model
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Like Model
class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# ------------------------- UTILITY FUNCTION -------------------------
# Function to fetch country info from REST API
def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[0]
    return None

# ------------------------- VIEWS -------------------------
# Blog List View
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})

# Blog Detail View
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    country_info = get_country_info(blog.country)
    return render(request, 'blog_detail.html', {'blog': blog, 'country_info': country_info})

# Add Comment View
def add_comment(request, blog_id):
    if request.method == "POST":
        blog = get_object_or_404(Blog, id=blog_id)
        content = request.POST.get("content")
        Comment.objects.create(blog=blog, user=request.user, content=content)
        return redirect('blog_detail', blog_id=blog_id)

# Like Blog View
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    like, created = Like.objects.get_or_create(blog=blog, user=request.user)
    if not created:
        like.delete()
    return JsonResponse({"likes": blog.likes.count()})

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('blog_list')
    return render(request, 'login.html')

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('blog_list')

# ------------------------- URL Configuration -------------------------
urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('blog/<int:blog_id>/comment/', add_comment, name='add_comment'),
    path('blog/<int:blog_id>/like/', like_blog, name='like_blog'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]

# ------------------------- TEMPLATES -------------------------
# blog_list.html
BLOG_LIST_TEMPLATE = """
{% for blog in blogs %}
    <h2><a href="{% url 'blog_detail' blog.id %}">{{ blog.title }}</a></h2>
    <p>{{ blog.content }}</p>
{% endfor %}
"""

# blog_detail.html
BLOG_DETAIL_TEMPLATE = """
<h2>{{ blog.title }}</h2>
<p>{{ blog.content }}</p>
<p>Country: {{ blog.country }}</p>
<h3>Comments</h3>
{% for comment in blog.comments.all %}
    <p>{{ comment.content }} - {{ comment.user.username }}</p>
{% endfor %}
<form method="post" action="{% url 'add_comment' blog.id %}">
    {% csrf_token %}
    <textarea name="content"></textarea>
    <button type="submit">Add Comment</button>
</form>
<form method="post" action="{% url 'like_blog' blog.id %}">
    {% csrf_token %}
    <button type="submit">Like ({{ blog.likes.count }})</button>
</form>
"""

# register.html
REGISTER_TEMPLATE = """
<h2>Register</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Register</button>
</form>
"""

# login.html
LOGIN_TEMPLATE = """
<h2>Login</h2>
<form method="post">
    {% csrf_token %}
    <input type="text" name="username" placeholder="Username">
    <input type="password" name="password" placeholder="Password">
    <button type="submit">Login</button>
</form>
"""

# ------------------------- FINAL NOTES -------------------------
"""
To run this Django project:

1. Install Django
    pip install django

2. Create a new Django project
    django-admin startproject myproject
    cd myproject

3. Create a new Django app (blog)
    python manage.py startapp blog

4. Copy this code into 'blog/views.py' and configure it in 'myproject/settings.py'

5. Run database migrations
    python manage.py migrate

6. Create a superuser
    python manage.py createsuperuser

7. Run the server
    python manage.py runserver
"""

