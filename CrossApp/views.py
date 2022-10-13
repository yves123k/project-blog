import re
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, View, CreateView, ListView, UpdateView, DeleteView
from hitcount.views import HitCountDetailView 
from django.views.generic.edit import FormMixin
from django.shortcuts import render, redirect,reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import Comments, MyUser
from .forms import AdForm, FormComment, LoginForm, SignupForm, UpdateForm, formAc,FormContact
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from CrossHouse import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .tokens import generate_token
from CrossApp.models import Create_Ad


# Create your views here.
class Website_Manager(TemplateView):
    template_name = "index.html"


class Login(View):
    template_name = 'login.html'
    class_form = LoginForm

    def get(self, request):
        form = self.class_form()
        return render(request, self.template_name, locals())

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            user = authenticate(
                email=request.POST["email"],
                password=request.POST["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'content de vous voir', request.user.username)
                    return redirect('home')
                else:
                    messages.error(request, 'Your account is not active')
                    return render(request, self.template_name, locals())
            else:
                messages.error(request, 'username or password not correct')
                return render(request, self.template_name, locals())
        else:
            return render(request, self.template_name, locals())


class Signup(Login):
    template_name = 'register.html'
    class_form = SignupForm

    def get(self, request):
        form = self.class_form()
        return render(request, self.template_name, locals())

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            MyUser.is_active = False
            f.save()
            messages.success(request, "register success")
            admin = MyUser.objects.filter(is_superuser=True)
            subject = "Crosspay confirm email!!"
            message = "Hello " + f.email + "!! \n" + "Welcome to Crosspay!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nYves kouame technical director"
            from_email = settings.EMAIL_HOST_USER
            to_list = [f.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            current_site = get_current_site(request)
            email_subject = "Confirm your Email @ Good - Crosspay Login!!"
            message2 = render_to_string('email_token_script.html', {

                'name': f.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(f.pk)),
                'token': generate_token.make_token(f),
                'date': f.date_joined
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [f.email],
            )
            email.content_subtype="html"
            email.fail_silently = True
            email.send()

            return redirect('email-validate')
        return render(request, self.template_name, locals())


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
        if user.is_active:
            return redirect('not_found')

    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user == None:
        return redirect('not_found')

    else:

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            # user.profile.signup_confirmation = True
            user.save()
            login(request, user)
            messages.success(request, "Your Account has been activated!!")
            return redirect('login')

        else:
            return render(request, 'activation_failed.html', locals())


class email_validate_view(Login):
    template_name = 'confirmation.html'

    def get(self, request):
        return render(request, self.template_name ,{"text_method":"Confirmation"})
    

class Admin_Register_User(Login):
    template_name = 'admin_create_user.html'
    class_form = SignupForm

    def get(self, request):
        form = self.class_form()
        return render(request, self.template_name, locals())

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            MyUser.is_active = False
            f.save()
            messages.success(request, "Create user success")
            return redirect("admin_create_user")



        else:
            return render(request, self.template_name, locals())


class All_User(ListView):
    model = MyUser
    template_name = 'come_on_app/users.html'
    context_object_name = 'users'

    def get(self, request):
        user_list = MyUser.objects.all()
        paginator = Paginator(user_list, 4)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'blogger': page_obj})


class Update_User(View):
    template_name = 'update-user.html'
    class_form = UpdateForm

    def get(self, request):
        form = self.class_form()
        update_info = MyUser.objects.filter(pk=request.user.pk)    
        return render(request, self.template_name, locals())

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request):
        form = self.class_form(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Profil update with success")
            f = form.save(commit=False)
            f.username = form.cleaned_data['username']
            f.last_name = form.cleaned_data['last_name']
            f.first_name = form.cleaned_data['first_name']
            f.phoneNumber = form.cleaned_data['phoneNumber']
            f.address = form.cleaned_data['address']
            f.website = form.cleaned_data['website']
            f.job = form.cleaned_data['job']
            f.save()
            return redirect('update-user')


        
        messages.error(request, "error")
        return render(request, self.template_name, locals())
# class Update_User(UpdateView):
#     template_name = 'update-user.html'
#     class_form = UpdateForm

#     def form_valid(self, form):
#         messages.success(self.request, "AD CREATE SUCCESS")
#         return super().form_valid(form)

    
    # def post(self, request):
    #     form = self.class_form(request.POST, request.FILES, instance=request.user)
    #     if form.is_valid():
    #         f = form.save(commit=False)
    #         f.username = form.cleaned_data['username']
    #         f.last_name = form.cleaned_data['last_name']
    #         f.first_name = form.cleaned_data['first_name']
    #         f.phoneNumber = form.cleaned_data['phoneNumber']
    #         f.address = form.cleaned_data['address']
    #         f.website = form.cleaned_data['website']
    #         f.save()
    #         messages.success(request, "Profil update with success")
    #         return render(request, self.template_name, locals())


    #     else:
    #         messages.error(request, "error")
    #         return render(request, self.template_name, locals())

class CreateAdForm_View(CreateView):
    model = Create_Ad
    template_name = "create_ad.html"
    form_class = AdForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        messages.success(self.request, "AD CREATE SUCCESS")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Echec de l'operation ")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("create_ad")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = "Create"
        context['method_ad'] = "Create Your Ad"
        context['last_method'] = "Update My Ad"
        return context


class AdUpdate_View(UpdateView):
    model = Create_Ad
    template_name = "create_ad.html"
    form_class = AdForm
    context_object_name = 'blog'

    def form_valid(self, form):
        messages.success(self.request, "Ad Update Success")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error Update")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = "Update Ad"
        context['method_ad'] = "Edit My Ad"
        context['last_method'] = "Update My Ad"
        return context


class AdDelete_View(DeleteView):
    model = Create_Ad
    template_name = "delete_ad_view.html"
    context_object_name = "delete"
    
    def get_success_url(self):
        return reverse("home")

# class PropertyView(View):
#     model = Create_Ad
#     template_name = "property.html"
    
#     def get(self,request):
#         return render(request, self.template_name, locals())

class BlogView(ListView):
    model = Create_Ad
    template_name = "blog_page.html"
    context_object_name = "blog"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs) 
        return context

class BlogDetailView(FormMixin,HitCountDetailView):
    model = Create_Ad
    template_name = "single_post.html"
    context_object_name = "blog_detail"
    pk_url_kwarg = 'pk'
    form_class = FormComment
    count_hit = True

    def get_success_url(self):
        return reverse("blog_detail", kwargs={'pk': self.object.pk})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FormComment()
        context['form_contact'] = FormContact()
        context['comments'] = Comments.objects.filter(ad_comments=self.object) 
        context['number_comments'] = Comments.objects.filter(ad_comments=self.object).count()
        # seller = Create_Ad.objects.filter(pk=self.object.pk)
        # print(seller)
        return context

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        if 'post_comment' in request.POST:
            form = FormComment(request.POST)
            if form.is_valid:
                f = form.save(commit=False)
                f.author_comment = self.request.user
                f.ad_comments = self.object
                f.save()
                return super(BlogDetailView, self).form_valid(form)
            else:
                return self.form_invalid(form)
        elif 'post_contact' in request.POST:
            form = FormContact(request.POST)
            if form.is_valid:
                self.contact_proccess(request,pk=self.object.pk)
                return super(BlogDetailView, self).form_valid(form)
            else:
                return super(BlogDetailView, self).form_valid(form) 

    def contact_proccess(self,request,pk):
        email = request.POST.get("email_contact")
        message = request.POST.get("area_message")
        print(message,email)
        seller = Create_Ad.objects.filter(pk=pk)
        print(seller)
        for info in seller:
            email_seller = info.author.email
            username_seller = info.author.username
        print(email_seller)  
        current_site = get_current_site(request)
        email_subject = "Croospay Offer received "
        message2 = render_to_string('contact_seller.html', {
            
            'name_seller': username_seller,
            'domain': current_site.domain,
            'message': message,
            'photo': request.user.photo.url,
            'name_client':request.user.username,
            'email_client' : request.user.email,
            'number_client': request.user.phoneNumber,
            'job': request.user.job


        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
        )
        email.content_subtype = "html"
        email.fail_silently = True
        email.send()
        
        return redirect('home')

    # def form_valid(self, form):
    #     f = form.save(commit=False)
    #     f.author_comment = self.request.user
    #     f.ad_comments = self.object 
    #     f.save()
    #     return super(BlogDetailView, self).form_valid(form)
    
    

    def numbers_view(request):
        number = Comments.objects.filter(ad_comments=request.object)
        return number

class ContactView(TemplateView):
    template_name = "contact.html"
    
class MyBlogView(View):
    template_name = "myblog.html"
    
    def get(self,request):
        myblog = Create_Ad.objects.filter(author=request.user.pk)
        print(myblog)
        return render(request, self.template_name, locals())

class BloggerProfilView(View):
    template_name = "users.html"

    def get(self,request,pk):
        blogger_query = MyUser.objects.filter(pk=pk)
        return render(request, self.template_name, locals())

class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request,"index.html")
                
# def post(self,request,pk):
#     if request.method == "POST":
#         email = request.POST.get("email_contact")
#         message = request.POST.get("area_message")
#         print(message,email)
#         seller = Create_Ad.objects.filter(pk=pk)
#         for info in seller:
#             email_seller = info.author.email
#             username_seller = info.author.username
#         print(email_seller)  
#         current_site = get_current_site(request)
#         email_subject = "Croospay Offer received "
#         message2 = render_to_string('contact-seller.html', {
            
#             'name_seller': username_seller,
#             'domain': current_site.domain,
#             'message': message,
#             'photo': request.user.photo.url,
#             'name_client':request.user.username

#         })
#         email = EmailMessage(
#             email_subject,
#             message2,
#             settings.EMAIL_HOST_USER,
#             [email_seller],
#         )
#         email.content_subtype = "html"
#         email.fail_silently = True
#         email.send()
        
#         return redirect('home')
            