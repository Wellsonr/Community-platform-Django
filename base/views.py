from django.shortcuts import render,redirect
from .models import Room, Topic, Message, User
from django.db.models import Q # with this allowing us to add &(and) |(or) statements into filter
from .forms import RoomForm, UserForm, MyUserCreationForm  # use this for create a form from template, and {{ form.as_p }} .as_p wrap all the forms in the one places
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# rooms = [
#     {'id':1, 'name': 'Learn Django with me'},
#     {'id':2, 'name': 'Design the web'},
#     {'id':3, 'name': 'FrontEnd Developers'}
# ]

def loginPage(request) :
    if request.method == 'POST' :
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try :
            user = User.objects.get(email=email)
        except :
            messages.error(request, "User not found")

    
        user = authenticate(request, email=email, password=password)
        
        if user is not None : 
            login(request, user)
            return redirect(home)
    return render(request, 'base/login-form.html')

def logoutPage(request):
    logout(request)
    return redirect(home)

def signupPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST' :
        form = MyUserCreationForm(request.POST)
        if form.is_valid() :
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect(home)
        else :
            messages.error(request, 'an error occurred during registration')
    return render(request, 'base/signup-form.html', {'form': form})

def home (request) :
    q = request.GET.get('queries') if request.GET.get('queries') != None else ''
# Check if 'q' parameter exists in the GET request
# query_param = request.GET.get('q')

# Assign the value of 'q' parameter if it exists, otherwise assign an empty string
# query = query_param if query_param is not None else ""

    room = Room.objects.filter(Q(topic__name__icontains=q)|
                               Q(name__icontains=q)|
                               Q(description__icontains=q))
    topics = Topic.objects.all()[:5]
    rooms_count = room.count()
    
    message_activity = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':room, 'topics':topics,
               "rooms_count":rooms_count, "message_activity":message_activity}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def createRoom (request) :
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST' :
        form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create (
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        # if form.is_valid() :
        # room = form.save(commit=True)
        # room.host = request.user
        # room.save()
        return redirect(home)
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room-form.html', context)

def updateRoom(request, pk) :
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host :
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST' :
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room-form.html', context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host :
        return HttpResponse('You are not allowed here')
    
    if request.method == "POST" :
        room.delete()
        return redirect(home)
    return render(request, 'base/delete.html', {'obj':room})

def room (request, pk) :  #pk is a dynamic value name
    room = Room.objects.get(id=pk)
    room_message = room.message_set.all()
    participant = room.participants.all()
    if request.method == "POST" :
        body = request.POST.get('body')
        body_stripped = body.strip()
        if isinstance(body_stripped, str) and body_stripped != "": 
            message = Message.objects.create(
                user = request.user,
                room = room,
                body = request.POST.get('body'),
            )
            room.participants.add(request.user)
        else :
            messages.error(request, 'Type a message')
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_message': room_message, 'participant': participant}
    
    if room is None :
        context['error'] = "Room not found! " # another way to add 2 key value into dictionary

    return render(request, 'base/room.html', context)
# Didalam room function ada parameters pk(primary key), pk ini didapatkan dari url yang terinput,
# 1. Kita buat room value menjadi none jadi ketika pk tidak ada didalam room akan mereturn room template yang kosongan.
# 2. Kedua kita loop rooms dan ketika id kita sesuai dengan pk yang terinput kita akan store id dan juga name dari rooms kedalam variable room.
# 3. Setelah itu kita akan pass data room kedalam render function agar room template kita bisa memperlihatkan room.name dari variable room.

# In simpler terms, this function retrieves a specific room from the rooms list based on the provided pk value. 
# It then passes this room to the room.html template to be displayed on a webpage.

def profilePage (request,pk) :
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    message_activity = user.message_set.all()
    topics = Topic.objects.all()
    context = {'topics': topics, 'user': user, 'rooms': rooms, 'message_activity': message_activity }
    return render (request, 'base/profile-template.html', context)


def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
        
    if request.user != message.user :
        return HttpResponse('You are not the message owner')
    
    if request.method == "POST" :
        message.delete()
        return redirect(home)
    return render(request, 'base/delete.html', {'obj':message})


def settings (request) :
    context = {}
    return render(request, 'base/settings.html', context )

@login_required(login_url ='login')
def updateUser (request) :
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid() :
            form.save()
            return redirect('profile', pk=user.id)
        
    return render (request, 'base/update-user.html', {'form': form})

def topicPage (request) :
    q = request.GET.get('queries') if request.GET.get('queries') != None else ''

    topics = Topic.objects.filter(Q(name__icontains=q))
    
    context = {'topics': topics}
    return render (request, 'base/topics.html', context)

def activityPage (request) :
    q = request.GET.get('queries') if request.GET.get('queries') != None else ''
    message_activity = Message.objects.filter(Q(room__topic__name__icontains=q))[:3]
    context = {'message_activity': message_activity}
    return render (request, 'base/activity.html', context)