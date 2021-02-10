# UserChatProject
Django powered chat project


#### Create a virtualenv 
`virtualenv vme`


#### Activate the env

##### linux
`source vme/bin/activate`

##### window
`vme\Scripts\activate`




## Now run following commands on activated virtualenv



## Make directories if not exists
`mkdir media static templates`


#### Install required packages
`pip install -r requirements.txt`


### Run makemigrations for users app first
`python manage.py makemigrations users`

#### In case of any makemigrations error

##### commentout the url include of user i.e

###### change `UserChatProject/urls.py` from

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]

```
######  to this

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('users.urls')),
]


```
### And again run makemigrations and then uncomment above line






### Run migrate to create the tables
`python manage.py migrate`



### Move 'user-profile.png' to media directory

##### linux
`mv user-profile.png media`
##### window
`move user-profile.png media`



### Runserver on port 8000
`python manage.py runserver 0.0.0.0:8000`
