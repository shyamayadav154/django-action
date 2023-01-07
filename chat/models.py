
from django.db import models
from accounts.models import CustomUser
# from gdstorage.storage import GoogleDriveStorage
from datetime import datetime
# Define Google Drive Storage
# gd_storage = GoogleDriveStorage()

# Create your models here.

class Message1(models.Model):
    sender=models.CharField(max_length=120)
    receiver=models.CharField(max_length=120)
    message=models.CharField(max_length=1000000)
    date=models.DateTimeField(default=datetime.now,blank=True)
    file_status=models.BooleanField(default=False)
    file_name=models.CharField(max_length=1000000,default=None,null=True)

class Friend(models.Model):
    user=models.CharField(max_length=120)
    friend=models.CharField(max_length=120)
    nickname=models.CharField(max_length=120)

import random
import string

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Room(models.Model):
    """
    Room model that holds associated messages and users.
    """

    # Unique room name.
    name = models.TextField(max_length=50)
    # Allow users to join the room.
    active = models.BooleanField(default=True)
    # Time room was created.
    timestamp = models.DateTimeField(auto_now_add=True)
    # User who created this room.
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    # Administrator users.
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, related_name='room_admins')
    # Normal room users who will be sending messages.
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, related_name='room_users')

    def __str__(self):
        return f'Room | id: {self.id},  name:{self.name}'


class Message(models.Model):
    """
    Message model that holds user messages.
    """
    class Meta:
        ordering = ['-timestamp']

    # Room the message is in.
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None, related_name='messages')
    # User that sent the message.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    # Time message was sent.
    timestamp = models.DateTimeField(auto_now_add=True)
    # Message text content.
    text = models.TextField(null=False)

    def __str__(self):
        return f'Message | id:{self.id} text:{self.text}'


def get_invite_key_string():
    """
    :returns: Random and unique string of random characters.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


def get_inivite_key_expire_date():
    """
    :returns: Room invite key expire date.
    """
    # print(timezone.now())
    # print(timezone.timedelta(hours=2))
    # print(timezone.now() + timezone.timedelta(hours=2))
    return timezone.now() + timezone.timedelta(hours=2)  # Valid for 2 hours.


class RoomInviteKey(models.Model):
    """
    Room invite key model that holds access keys for rooms.
    """

    # Invite key string.
    key = models.TextField(null=False, unique=True, default=get_invite_key_string)
    # User who created this key.
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                                related_name='roominvitekey_creator')
    # Room the key is used with.
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None)
    # If not null, invite key is only for specific user.
    only_for_this_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None,
                                           null=True, blank=True, related_name='roominvitekey_only_for_this_user')
    # Valid until.
    valid_due = models.DateTimeField(default=get_inivite_key_expire_date)
    # Give admin to this user if true.
    give_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'Key | id:{self.id}, key:{self.key}, room: {self.room.id}'

# class Fileupload(models.Model):
#     file=models.FileField(upload_to='uploaded_files/', storage=gd_storage)

# class Room1(models.Model):
#     pass

# from django.db import models
# from accounts.models import CustomUser
# # from gdstorage.storage import GoogleDriveStorage
# from datetime import datetime
# # Define Google Drive Storage
# # gd_storage = GoogleDriveStorage()

# # Create your models here.

# class Message1(models.Model):
#     sender=models.CharField(max_length=120)
#     receiver=models.CharField(max_length=120)
#     message=models.CharField(max_length=1000000)
#     date=models.DateTimeField(default=datetime.now,blank=True)
#     file_status=models.BooleanField(default=False)
#     file_name=models.CharField(max_length=1000000,default=None,null=True)

# # class Friend1(models.Model):
# #     user=models.CharField(max_length=120)
# #     friend=models.CharField(max_length=120)
# #     nickname=models.CharField(max_length=120)

# import random
# import string

# from django.conf import settings
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils import timezone

# class Room(models.Model):
#     """
#     Room model that holds associated messages and users.
#     """

#     # Unique room name.
#     name = models.TextField(max_length=50)
#     # Allow users to join the room.
#     active = models.BooleanField(default=True)
#     # Time room was created.
#     timestamp = models.DateTimeField(auto_now_add=True)
#     # User who created this room.
#     creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
#     # Administrator users.
#     admins = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, related_name='room_admins')
#     # Normal room users who will be sending messages.
#     users = models.ManyToManyField(settings.AUTH_USER_MODEL, default=None, related_name='room_users')

#     def __str__(self):
#         return f'Room | id: {self.id},  name:{self.name}'


# class Message(models.Model):
#     """
#     Message model that holds user messages.
#     """
#     class Meta:
#         ordering = ['-timestamp']

#     # Room the message is in.
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None, related_name='messages')
#     # User that sent the message.
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
#     # Time message was sent.
#     timestamp = models.DateTimeField(auto_now_add=True)
#     # Message text content.
#     text = models.TextField(null=False)

#     def __str__(self):
#         return f'Message | id:{self.id} text:{self.text}'


# def get_invite_key_string():
#     """
#     :returns: Random and unique string of random characters.
#     """
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


# def get_inivite_key_expire_date():
#     """
#     :returns: Room invite key expire date.
#     """
#     # print(timezone.now())
#     # print(timezone.timedelta(hours=2))
#     # print(timezone.now() + timezone.timedelta(hours=2))
#     return timezone.now() + timezone.timedelta(hours=2)  # Valid for 2 hours.


# class RoomInviteKey(models.Model):
#     """
#     Room invite key model that holds access keys for rooms.
#     """

#     # Invite key string.
#     key = models.TextField(null=False, unique=True, default=get_invite_key_string)
#     # User who created this key.
#     creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
#                                 related_name='roominvitekey_creator')
#     # Room the key is used with.
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None)
#     # If not null, invite key is only for specific user.
#     only_for_this_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None,
#                                            null=True, blank=True, related_name='roominvitekey_only_for_this_user')
#     # Valid until.
#     valid_due = models.DateTimeField(default=get_inivite_key_expire_date)
#     # Give admin to this user if true.
#     give_admin = models.BooleanField(default=False)

#     def __str__(self):
#         return f'Key | id:{self.id}, key:{self.key}, room: {self.room.id}'

# # class Fileupload(models.Model):
# #     file=models.FileField(upload_to='uploaded_files/', storage=gd_storage)

# # class Room1(models.Model):
# #     pass
# # # Create your models here.
# # class Chat(models.Model):
# #     user1=models.ManyToManyField(CustomUser,related_name='user1')
# #     user2=models.ManyToManyField(CustomUser,related_name='user2')
# #     seen=models.BooleanField(default=False)
# #     sent_at=models.DateTimeField(auto_now_add=True)
# #     message=models.TextField()
