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
from users.models import UserProfile, ChatGroup, ChatMessage
from users.forms import UserProfileForm,ChatGroupForm,  ChatMessageForm
from django.contrib.contenttypes.models import ContentType


class Home(LoginRequiredMixin, TemplateView):
    '''
    default home view
    '''
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
    '''
    user profile view

    '''
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
    '''
    delete profile image
    '''
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


class ChatGroupFormView(LoginRequiredMixin,  CreateView):
    '''
        Chat Group Create View
    '''
    # permission_required = ('users.view_chat_group',
    #                        'users.add_chat_group',
    #                        'users.change_chat_group')
    model = ChatGroup
    form_class = ChatGroupForm
    template_name = 'chat_group_page.html'
    success_url = reverse_lazy('users:group-list')

    def form_valid(self, form):
        # form.save()
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['chat_group_form'] = context.pop('form')
        except KeyError:
            context['chat_group_form'] = self.get_form()
        return context

class ChatGroupListView(LoginRequiredMixin, ListView):
    '''
    list all Chat Group
    '''
    model = ChatGroup
    context_object_name = 'chat_group_object_list'
    template_name = 'chat_group_page.html'


class ChatGroupMessageView(LoginRequiredMixin, DetailView, FormView):
    '''
    comment create view
    '''
    model = ChatGroup
    template_name = 'chat_group_page.html'
    form_class = ChatMessageForm


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_initial(self):
        """Return the initial data to use for forms on this view.
        Initial to work with Comment form
        """
        base_initial = self.initial.copy()
        # context = super().get_context_data()
        obj = self.get_object()
        base_initial['content_type'] = ContentType.objects.get_for_model(
            model=obj.__class__)
        base_initial['object_id'] = obj.pk
        base_initial['user'] = self.request.user
        # print('ddddd',dir(self))
        return base_initial

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        obj = self.get_object()
        # return  reverse_lazy("erpapp:followup-detail",kwargs={"pk":obj.pk})
        return obj.get_update_url()

    def form_valid(self, form):
        print('form_valid')
        print(form.cleaned_data)
        f_content_type = form.cleaned_data.get('content_type')
        f_object_id = form.cleaned_data.get('object_id')
        f_user = form.cleaned_data.get('user')
        f_message = form.cleaned_data.get('message')
        parent_obj = None
        if f_user != self.request.user:
            #messages.success(request, "You do not have permission to view this.")
            #raise Http404
            reponse = HttpResponse("You do not have permission to do this.")
            reponse.status_code = 403
            return reponse
        try:
            parent_id = int(self.request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = ChatMessage.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        ChatMessage.objects.create(message=f_message,
                                     user=f_user,
                                     content_type=f_content_type,
                                     object_id=f_object_id,
                                     parent=parent_obj,
                                     )
        # obj = self.get_object()
        # return HttpResponseRedirect(obj.get_update_url())
        return super().form_valid(form)

    def form_invalid(self, form):
        print('form_invalid')
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        obj = kwargs.pop('object', None)
        if obj is None:
            self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        # content_type = ContentType.objects.get_for_model(model=self.object.__class__)
        try:
            context['chat_message_form'] = context.pop('form')
        except KeyError:
            context['chat_message_form'] = self.get_form()

        try:
            context['chat_group_object'] = context.pop('object')
        except KeyError:
            context['chat_group_object'] = self.get_object()

        # if self.request.user.is_superuser:
        #     context['chat_group_object_list'] = ChatGroup.objects.all()
        # else:
        #     context['chat_group_object_list'] = ChatGroup.objects.filter(
        #         user=self.request.user)
        context['chat_group_object_list'] = ChatGroup.objects.all()
        return context