from . import views
from django.urls import path

app_name = 'profile'

urlpatterns = [
    path('dashboard/', views.ProfileDashboard.as_view(), name='dashboard'),
    path('favorite/', views.ProfileFavorites.as_view(), name='favorite'),
    path('recent/', views.ProfileRecent.as_view(), name='recent'),
    path('edit/', views.ProfileEdit.as_view(), name='edit'),
    path('new_article/', views.ArticleCreateView.as_view(), name='new_article'),
    path('update_full_name/', views.UpdateFullName.as_view(), name='update_full_name'),
    path('update_phone/', views.UpdatePhone.as_view(), name='update_phone'),
    path('update_email/', views.UpdateEmail.as_view(), name='update_email'),
    path('update_image/', views.UpdateImage.as_view(), name='update_image'),
    path('update_bio/', views.UpdateBio.as_view(), name='update_bio'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
]
