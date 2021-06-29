from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as logout_user

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import BunkForm
from .models import Bunk, User

# global vars used to keep track of personal page sorting state
prevInbox = '-time'
prevSent = '-time'

def login_view(request):
    """logs in a user and redirects to their personal feed if successful"""
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        auth_user = authenticate(username=username, password=password)
        if auth_user is not None:
            login(request,  auth_user)
            try:
                user = get_object_or_404(User, username=username)
            except:
                context = {'error_msg': 'unable to find existing user - enter a correct username and password'}
                return render(request, 'jitter/login.html', context)
            else:
                user.logged_in = True
                user.save()
                return HttpResponseRedirect(reverse('jitter:personal_feed', args=(username,)))
        else:
            context = {'error_msg': 'unable to authenticate user - enter a correct username and password'}
            return render(request, 'jitter/login.html', context)
    else:
        return render(request, 'jitter/login.html')

def signup(request):
    """creates a new user from signup page"""
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not username:
                context = {'error_msg': 'username is required - please enter a username'}
                return render(request, 'jitter/signup.html', context)
        if not password:
                context = {'error_msg': 'password is required - please enter a password'}
                return render(request, 'jitter/signup.html', context)
        try:
            # check if user already exists
            user = get_object_or_404(User, username=username)
        except:
            email = request.POST.get('email', None)
            photo_url = request.POST.get('photo_url', None)
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            
            # if we have a username and a password, we can create a new user
            u = User.objects.create(username=username, password=password)
            if email:
                u.email = email
            if photo_url:
                u.photo = photo_url
            if first_name:
                u.first_name = first_name
            if last_name:
                u.last_name = last_name

            u.set_password(u.password)
            u.save()

            # log user in so they can access their personal feed
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request,  auth_user)
                u.logged_in = True
                u.save()
            else:
                context = {'error_msg': 'unable to log new user in - please sign up again'}
                return render(request, 'jitter/signup.html', context)
            
            # now that user is signed up and logged in, take them to their personal feed
            return HttpResponseRedirect(reverse('jitter:personal_feed', args=(username,)))

        else:
            context = {'error_msg': 'user already exists - enter a different username'}
            return render(request, 'jitter/signup.html', context)
    
    return render(request, 'jitter/signup.html')

@login_required
def logout(request, username):
    """logs out a user and redirects to the login page"""
    logout_user(request)
    try:
        user = get_object_or_404(User, username=username)
    except:
        context = {'error_msg': 'unable to find user - enter a correct username and password to login'}
        return render(request, 'jitter/login.html', context)
    else:
        user.logged_in = False
        user.save()
        return HttpResponseRedirect(reverse('jitter:login'))

@login_required
def main_feed(request, column='-time'):
    """displays the main feed of bunks, with default sort by most recent time"""
    bunks = Bunk.objects.order_by(column)
    active_users = User.objects.filter(logged_in=True).order_by('-num_bunks')
    context = {'bunks': bunks, 'active_users': active_users}
    return render(request, 'jitter/main_feed.html', context)

@login_required
def personal_feed(request, username, column_inbox='old', column_sent='old'):
    global prevInbox
    global prevSent
    """
    displays the most recent bunks to a given user
    if a user is logged in, they can bunk another user from here
    """

    # setup bunk form
    if request.method == "POST":
        form = BunkForm(request.POST)
        if form.is_valid:
            return HttpResponseRedirect(reverse('jitter:personal_feed', args=(username,)))
    else: 
        form = BunkForm()
    
    # check user exists before continuing to their personal feed
    try:
        user = get_object_or_404(User, username=username)
    except:
        context = {'error_msg': 'unable to find user - login to be able to bunk'}
        return render(request, 'jitter/login.html', context)
    else:
        # determine if we need to update which column to sort on in the inbox table
        if column_inbox == 'old':
            column_inbox = prevInbox
        else:
            prevInbox = column_inbox
        
        # determine if we need to update which column to sort on in the sent table
        if column_sent == 'old':
            column_sent = prevSent
        else:
            prevSent = column_sent

        # retrieve bunks and users to populate tables and bunk form drop down list
        personal_bunks = Bunk.objects.filter(to_user=user).order_by(column_inbox)
        bunks_sent = Bunk.objects.filter(from_user=user).order_by(column_sent)
        users = User.objects.all()
        context = {
            'personal_bunks': personal_bunks, 
            'user': user, 
            'users': users, 
            'bunk_form': form,
            'bunks_sent': bunks_sent
        }
        return render(request, 'jitter/personal_feed.html', context)

@login_required
def add_bunk(request, username):
    """bunks a user - if unable to find a username, redirects to the main feed"""
    try:
        from_user = get_object_or_404(User, username=username)
    except:
        return HttpResponseRedirect(reverse('jitter:main_feed'))
    else:
        to_user_name = request.POST.get('user_to_input', None)
        if to_user_name is not None:
            from_user.num_bunks+=1
            from_user.save()
            to_user = User.objects.get(username=to_user_name)
            Bunk.objects.create(from_user=from_user, to_user=to_user)
            return HttpResponseRedirect(reverse('jitter:personal_feed', args=(from_user.username,)))
        else:
            return HttpResponseRedirect(reverse('jitter:main_feed'))
