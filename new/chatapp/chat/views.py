from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Message

# Sign up view
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('chat_home')
    return render(request, 'signup.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat_home')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Chat homepage
def chat_home(request):
    users = User.objects.exclude(username=request.user.username)  # Exclude current user
    return render(request, 'chat_home.html', {'users': users})
def chat(request, user_id):
    other_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        sender=request.user, receiver=other_user
    ) | Message.objects.filter(
        sender=other_user, receiver=request.user
    )
    return render(request, 'chat.html', {'other_user': other_user, 'messages': messages})
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('message')
        receiver_id = request.POST.get('receiver_id')
        receiver = User.objects.get(id=receiver_id)

        # Create a new message
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content
        )

        # Redirect back to the chat page
        return redirect('chat', user_id=receiver_id)
    return HttpResponse(status=400)