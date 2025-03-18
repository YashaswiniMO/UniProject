from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Forum, Message
from django.contrib import messages
from .forms import ForumForm, MessageForm

def forum_home(request):
    forums = Forum.objects.all().order_by('-created_at')  # Show all forums
    return render(request, 'collaboration/forum_home.html', {'forums': forums})

def forum_list(request):
    forums = Forum.objects.all().order_by('-created_at')
    return render(request, 'collaboration/forum_list.html', {'forums': forums})

# Display a single forum with messages
@login_required
def forum_detail(request, forum_id):
    forum = get_object_or_404(Forum, id=forum_id)
    messages = forum.messages.all()
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.forum = forum  # Ensure the message is linked to the forum
            message.save()
            return redirect('forum_detail', forum_id=forum.id)
    else:
        form = MessageForm()

    return render(request, 'collaboration/forum_detail.html', {'forum': forum, 'messages': messages, 'form': form})

# Posting a message in the forum
@login_required
def post_message(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    
    if request.method == "POST":
        message_text = request.POST['message']
        message = Message.objects.create(forum=forum, sender=request.user, text=message_text)
        message.save()
        return redirect('forum_messages', forum_id=forum.id)
    
    return render(request, 'collaboration/forum_messages.html', {'forum': forum})

# View all messages in a forum
def forum_messages(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    messages = Message.objects.filter(forum=forum).order_by('-created_at')
    return render(request, 'collaboration/forum_messages.html', {'forum': forum, 'messages': messages})


@login_required
def forum_create(request):
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.created_by = request.user
            forum.save()
            return redirect('forum_home')
    else:
        form = ForumForm()
    return render(request, 'collaboration/create_forum.html', {'form': form})


# Check if the user is a moderator
def is_moderator(user):
    return user.is_moderator

# Edit Message View (Allow the sender or moderator to edit)
@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    # Check if the user is the sender or a moderator
    if message.sender != request.user and not request.user.is_moderator:
        return redirect('forum_detail', forum_id=message.forum.id)

    if request.method == 'POST':
        message.text = request.POST['text']  # Update message text
        message.save()
        return redirect('forum_detail', forum_id=message.forum.id)

    return render(request, 'collaboration/edit_message.html', {'message': message})

# Delete Message View (Allow the sender or moderator to delete)
@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    # Check if the user is the sender or a moderator
    if message.sender != request.user and not request.user.is_moderator:
        return redirect('forum_detail', forum_id=message.forum.id)

    forum_id = message.forum.id
    message.delete()
    return redirect('forum_detail', forum_id=forum_id)