from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.views.generic.edit import CreateView, View, FormView
from django.views.generic import DetailView, TemplateView, UpdateView, ListView
# from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.contrib import messages
from .mixins import NextUrlMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
# from profiles.models import Setting
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from users.models import UserProfile
from users.forms import UserProfileForm
from django.contrib.contenttypes.models import ContentType


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class SignUpView(NextUrlMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = '/'
    template_name = 'registration/signup.html'
    success_message = 'You have signed up successfully'
    default_next = '/'

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        # authenticate user then login
        user = authenticate(
            username=form.cleaned_data['username'], password=form.cleaned_data['password1'], )
        login(self.request, user)
        messages.success(self.request, 'You have signed up successfully')
        next_path = self.get_next_url()
        return HttpResponseRedirect(next_path)


class UserLoginView(NextUrlMixin, SuccessMessageMixin, LoginView):
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True
    # template_name = 'registration/login3.html'


class UserLogoutView(NextUrlMixin, SuccessMessageMixin, LogoutView):
    pass


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/profile_page.html'
    model = UserProfile
    form_class = UserProfileForm
    success_url = reverse_lazy('users:user-profile')

    def get_object(self, queryset=None):
        ''' overwrite the method so we not need to config url '''
        try:
            obj = self.model.objects.get(user=self.request.user)
            return obj
        except Exception as ex:
            print('class UserProfileView def get_object', ex)
            return

    def get_initial(self, *args, **kwargs):
        ''' initialize your's form values here '''
        base_initial = self.initial.copy()
        base_initial.update({'user': self.request.user})
        return base_initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user_profile_form'] = context.pop('form')
        except KeyError:
            context['user_profile_form'] = self.get_form()

        try:
            context['user_profile_object'] = context.pop('object')
        except KeyError:
            context['user_profile_object'] = self.get_object()

        return context

    def form_valid(self, form, *args, **kwargs):
        if not form.instance.user:
            form.instance.user = self.request.user
        form.save()
        if self.request.is_ajax():
            return JsonResponse({'result': 'Success', 'content': 'Profile Updated'})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax() and form.errors:
            errors = form.errors.as_json()
            return HttpResponse(errors, status=400, content_type='application/json')
        return super().form_invalid(form)


class DeleteProfileImage(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            # db = request.POST.get('disabled')
            # print('---- is Disabled ----', db)
            p = UserProfile.objects.get(user=request.user)
            p.image = ''
            p.save()
            return JsonResponse({'result': 'Success', 'content': 'Image Deleted'})
        except Exception as ep:
            print('class DeleteProfileImage def post', ep)
        return HttpResponse({'result': 'error', 'content': 'Unable to Delete'}, status=400, content_type='application/json')
