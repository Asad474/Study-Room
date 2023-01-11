from django.shortcuts import render,redirect
from .models import Room,Topic,Message,User
from .forms import RoomForm , UserForm , MyUserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def home(request):
    q=request.GET.get('q') if request.GET.get('q') else ''
    r=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) | 
        Q(description__icontains=q)
    )
    t=Topic.objects.all()[:5]
    rm_message=Message.objects.filter(Q(room__topic__name__icontains=q))
    count=r.count()
    context={'room':r,'topic':t,'count':count,'rm_message':rm_message}
    return render(request,'first_app/home.html',context)


def room(request,pk):
    rm=Room.objects.get(id=pk)
    rm_message=rm.message_set.all().order_by('-created')
    participants=rm.participants.all()

    if request.method=='POST':
        Message.objects.create(
            user=request.user,
            room=rm,
            body=request.POST.get('body')
        )
        rm.participants.add(request.user)
        return redirect('room',pk=rm.id)

    context={'r':rm,'rm_messages':rm_message,'participants':participants} 
    return render(request,'first_app/room.html',context)    


@login_required(login_url='loginpage') 
def createroom(request):
    form=RoomForm()
    topics=Topic.objects.all()

    if request.method=='POST':
        topic_name=request.POST.get('topic')
        top , created=Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user, 
            topic=top,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        # form=RoomForm(request.POST)
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host=request.user
        #     form.save()
        return redirect('home')

    return render(request,'first_app/form.html',{'form':form,'topics':topics})    


@login_required(login_url='loginpage') 
def updateroom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()

    if request.user!=room.host:
        return HttpResponse('You are not allowed!!!')

    if request.method=='POST':
        topic_name=request.POST.get('topic')
        top , created=Topic.objects.get_or_create(name=topic_name)
        room.topic=top
        room.name=request.POST.get('name')
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')

    return render(request,'first_app/form.html',{'form':form,'topics':topics})    


@login_required(login_url='loginpage') 
def deleteroom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user!=room.host:
        return HttpResponse('You are not allowed!!!')

    if request.method=='POST':
        room.delete()
        return redirect('home')

    return render(request,'first_app/delete.html',{'obj':room})


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=authenticate(request,email=email,password=password)             
            login(request,user)
            return redirect('home')
        except:
            messages.error(request,'Email or Password does not exist!!!')    
    
    return render(request,'first_app/login_register.html',{'page':'login'})


def logoutuser(request):
    logout(request)
    return redirect('home')


def registeruser(request):
    form=MyUserCreationForm()

    if request.method=='POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            form.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An Error occured during registeration!!!')    

    context={'form':form,'page':'register'}
    return render(request,'first_app/login_register.html',context)


@login_required(login_url='loginpage') 
def deletemessage(request,pk):
    mesg=Message.objects.get(id=pk)
    r=mesg.room

    if request.user!=mesg.user:
        return HttpResponse('You are not allowed!!!')

    if request.method=='POST':
        mesg.delete()
        return redirect('room',pk=r.id)

    return render(request,'first_app/delete.html',{'obj':mesg})


def userprofile(request,pk):
    u=User.objects.get(id=pk)
    room=u.room_set.all()
    t=Topic.objects.all()
    rm_message=Message.objects.all()
    context={'u':u,'room':room,'rm_message':rm_message,'topic':t}
    return render(request,'first_app/user_profile.html',context)


@login_required(login_url='loginpage')    
def updateuser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method == 'POST':
        form=UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile',pk=user.id) 

    return render(request,'first_app/update_user.html',{'form':form})


def topicpage(request):
    q=request.GET.get('q') if request.GET.get('q') else ''
    t=Topic.objects.filter(name__icontains=q)
    context={'topic':t}
    return render(request,'first_app/topics.html',context)


def activitypage(request):
    rm_message=Message.objects.all()
    context={'rm_message':rm_message}
    return render(request,'first_app/activity.html',context)