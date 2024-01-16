from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Board, Topic, Post
from .forms import NewTopicForm

def home(request):
    boards = Board.objects.all()
    boards_names = list()

    for board in boards:
        boards_names.append(board.name)
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})
# THE CODE BELOW IS THE OLD WAY TO CREATE A NEW TOPIC
# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
    
#     if request.method == 'POST':
#         subject = request.POST['subject']
#         message = request.POST['message']
#         user = request.user
        
#         topic = Topic.objects.create(
#             subject=subject,
#             board=board,
#             starter=user
#         )
        
#         post = Post.objects.create(
#             message=message,
#             topic=topic,
#             created_by=user
#         )
        
#         return redirect('board_topics', pk=board.pk)
#     return render(request, 'new_topic.html', {'board': board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})