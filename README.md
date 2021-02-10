# UserChatProject
Django powered chat project


#### create a virtualenv 
`virtualenv vme`

#### activate the env

on window
`vme\Scripts\activate`


on linux
`source vme/bin/activate`



## now rurn following commands on activated virtualenv

## Make directories if not exists
`mkdir media static templates`
#### install required packages
`pip install -r requirements.txt`


### run makemigrations for users app first
`python manage.py makemigrations users`

#### in case of any makemigrations error
commentout the url include of user i.e
change `UserChatProject/urls.py` from
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]
```
to this
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('users.urls')),
]
```
### and again run makemigrations and then uncomment above line


### run migrate to create the tables
`python manage.py migrate`

### move 'user-profile.png' to media directory
#### linux system
`mv user-profile.png media`

#### on window system
`move user-profile.png media`

### runserver on port 8000
`python manage.py runserver 0.0.0.0:8000`
