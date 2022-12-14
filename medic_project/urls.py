"""medic_project URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from history import views as history_views
from appointment import views as appointment_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.RegisterView.as_view(), name='register'),
    path('profile/<username>/', user_views.ProfileView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('records/<username>/',
         history_views.UserMedicalHistoryView.as_view(),
         name='records'),
    path('appointments/', appointment_views.MakeAppointmentView.as_view(), name='create-appointment'),
    path('appointments/<username>/<str:select>', appointment_views.ListAppointmentsView.as_view(),
         name='list-appointment'),
    path('appointments/detail/<username>/<int:pk>', appointment_views.AppointmentDetailView.as_view(),
         name='appointment-detail'),
    path('appointments/treat/<username>/<int:pk>', appointment_views.PatientTreatmentView.as_view(), name='treatment'),
    path('', include('home_page.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


