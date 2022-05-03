from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.renderers import TemplateHTMLRenderer
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.contrib import messages
from .tokens import generate_token
from .models import BlogPost
from core import settings



class Home(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'hyperdrated/index.html'

    def get(self, request):
        queryset = BlogPost.objects.all()
        return Response({'post_list': queryset})


class BlogPostDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'hyperdrated/post_detail.html'

    def get(self, request, pk, slug):
        post_detail = BlogPost.objects.get(pk=pk, slug=slug)
        return Response({'post': post_detail})


class Signin(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'hyperdrated/signin.html'

    def get(self, request):
        return Response({})

    def post(self, request):
        username = request.POST['username']
        password1 = request.POST['password1']

        user = authenticate(username=username, password=password1)

        if user is not None:
            login(request, user)
            return redirect('hyperdrated:index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('hyperdrated:signin')


class Signout(APIView):
    def get(self, request):
        logout(request)
        return redirect('hyperdrated:signin')


class Signup(APIView):
    permissions_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'hyperdrated/signup.html'

    def get(self, request):
        return Response({})

    def post(self, request):
        username = request.POST['username']
        name = request.POST['fullname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if username == "" or name == "" or password1 == "" or password2 == "" or email == "":
            messages.error(request, 'All fields are required')
            return redirect('hyperdrated:signup')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('hyperdrated:signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('hyperdrated:signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.first_name = name
                user.is_active = False
                user.save()

                messages.success(request, 'Account created for ' + name)

                #email
                subject = 'Welcome to Hyperdrated'
                message = 'Welcome to Hyperdrated, ' + name + '!\n\n' + 'Thank you for using Hyperdrated!'
                from_email = settings.EMAIL_HOST_USER
                to_list = [user.email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)

                #confirmation
                current_site = get_current_site(request)
                conf_subject = 'Please confirm your email address'
                conf_message = render_to_string('hyperdrated/email_confirmation.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                })

                email = EmailMessage(
                    conf_subject,
                    conf_message,
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )

                email.fail_silently = True
                email.send()
                return redirect('hyperdrated:signin')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('hyperdrated:signup')


class UserActivate(APIView):
    permissions_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError,  ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save() 
            messages.success(request, 'Thank you for confirming your email address.')
            return redirect('hyperdrated:signin')
        else:
            messages.error(request, 'Activation failed')
            return redirect('hyperdrated:signin')


class UserPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'hyperdrated/user_page.html'

    def get(self, request):
        return Response({})

    def post(self, request):
        title = request.POST['title']
        content = request.POST['content']

        if title == "" or content == "":
            messages.error(request, 'Title and content are required')
            return redirect('hyperdrated:userpage')

        slug = title.replace(' ', '-')
        post = BlogPost.objects.create(title=title, slug=slug, content=content, author=request.user)
        post.save()
        return redirect('hyperdrated:index')
