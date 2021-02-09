from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.text import Truncator
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# Create your models here.

'''
delete migrations folder
python manage.py makemigrations profiles
python manage.py migrate --fake profiles zero
python manage.py migrate profiles
'''


class CustomUser(AbstractUser):
    name = models.CharField(
        db_column='name', max_length=45, blank=True)

    first_name = None
    last_name = None

    REQUIRED_FIELDS = ['email', ]  # already set in abstract model

    def __str__(self):
        if self.name is not None:
            return self.name
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = 'user'
        unique_together = ('email',)



class UserProfile(models.Model):
    id = models.SmallAutoField(primary_key=True)
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="userprofile/%Y/%m/%d/", default='user-profile.png', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
        db_table = 'user_profile'


# create the user profile is a new user created
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)


# attached a post save signal to the user model
post_save.connect(create_user_profile, sender=CustomUser)



class ChatGroup(models.Model):
    name = models.CharField(max_length=56)
    # user = models.ManyToManyField('users.CustomUser')
    user = models.ForeignKey('users.CustomUser',on_delete=models.CASCADE)
    # messages = GenericRelation('users.ChatMessage')
    class Meta:
        verbose_name = _("Chat Group")
        verbose_name_plural = _("Chat Group")
        db_table = 'chat_group'

    def __str__(self):
        # truncating after 10 words
        return Truncator(self.name).words(10, truncate=' …')

    def get_update_url(self):
        return reverse('users:chat-group-update', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('ChatGroup_detail', kwargs={"pk": self.pk})

    # @property
    # def created_by_user_avatar_url(self):
    #     usr = UserProfile.objects.get(user=self.created_by)
    #     if usr.image:
    #         return usr.image.url
    #     return ''
    @property
    def user_avatar_url(self):
        usr = UserProfile.objects.get(user=self.user)
        if usr.image:
            return usr.image.url
        return ''

    @property
    def messages(self):
        instance = self
        qs = ChatMessage.objects.filter_by_instance(instance)
        return qs


class ChatMessageManager(models.Manager):

    def all(self):
        qs = super(ChatMessageManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.pk
        qs = super(ChatMessageManager, self).filter(content_type=content_type,
                                                      object_id=object_id).filter(parent=None)
        return qs


class ChatMessage(models.Model):
    message = models.TextField()
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey('self',
                               on_delete=models.SET_NULL,
                               blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    objects = ChatMessageManager()
    # is_read_users = models.ManyToManyField('CustomUser',through='User')
    class Meta:
        # ordering = ['-timestamp']
        verbose_name = _("Chat Message")
        verbose_name_plural = _("Chat Messages")
        db_table = 'chat_message'

    def __str__(self):
        if self.user.name:
            return self.user.name
        return self.user.username

    def children(self):
        # replies
        return ChatMessage.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    @property
    def user_avatar_url(self):
        usr = UserProfile.objects.get(user=self.user)
        if usr.image:
            return usr.image.url
        return ''