"""Django URL Configuration

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

    #path('', views.CustomLoginView.as_view(), name='login'),
    #path('view/', views.my_view, name='my-view'),
    #path('signup/', views.signup, name='signup'),
    #path('option/', views.option, name='option'),  # 옵션 페이지 URL 추가
    #path('accounts/profile/', RedirectView.as_view(pattern_name='my-view')),
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.view_calendar, name='view-calendar'),  # 루트 URL에 연결된 뷰를 view_calendar로 변경
    path('exercise-record/', views.exercise_record, name='exercise-record'),
    path('accounts/profile/', RedirectView.as_view(pattern_name='view-calendar')),  # accounts/profile/ URL을 view-calendar로 리디렉션
]