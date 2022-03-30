from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .tokens import generate_token
from hyperdrated import settings
from core.models import Post


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']

        user = authenticate(username=username, password=password1)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')

    return render(request, 'signin.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        name = request.POST['fullname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exists')
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.error(request, 'Email already exists')
            return redirect('signup')
        
        if len(username) > 10:
            messages.error(request, 'Username too long')
            return redirect('signup')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, 'Username must be alphanumeric')
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = name
        myuser.is_active = False
        myuser.save()

        messages.success(request, 'Account created for ' + name)

        #email
        subject = 'Welcome to Hyperdrated'
        message = 'Welcome to Hyperdrated, ' + name + '!\n\n' + 'Thank you for using Hyperdrated!'
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        #confirmation
        current_site = get_current_site(request)
        conf_subject = 'Please confirm your email address'
        conf_message = render_to_string('email_confirmation.html', {
            'user': myuser,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })

        email = EmailMessage(
            conf_subject,
            conf_message,
            settings.EMAIL_HOST_USER,
            [myuser.email]
        )

        email.fail_silently = True
        email.send()


        return redirect('signin') 

    return render(request, 'signup.html')

def signout(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_encode(force_bytes(uidb64)))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for confirming your email address.')
        return redirect('signin')
    else:
        messages.error(request, 'Activation failed')
        return redirect('home')

def publicate(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        author = request.user
        slug = title.replace(' ', '-')

        blog_post = Post(title=title, slug=slug, content=content, author=author)
        blog_post.save()
        return redirect('home')

    return render(request, 'user_page.html')
