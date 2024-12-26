from . import views
from django.urls import path

app_name = 'ProfileApp'

url_patterns_data = [
    ('dashboard', views.ProfileDashboard),
    ('favorite', views.ProfileFavorites),
    ('recent', views.ProfileRecent),
    ('edit', views.ProfileEdit),
    ('new_article', views.ArticleCreateView),
    ('update_full_name', views.UpdateFullName),
    ('update_phone', views.UpdatePhone),
    ('update_email', views.UpdateEmail),
    ('change_password', views.ChangePassword),
]

urlpatterns = [path(f'{pattern}/', view.as_view(), name=pattern) for pattern, view in url_patterns_data]
