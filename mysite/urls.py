"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
import webhook.views  # 確保導入了您的views模組
import accounts.views  # 導入 accounts 的 views

urlpatterns = [
    path('', accounts.views.home, name='home'),  # 將這個設置為首頁
    path('update_server/', webhook.views.update_server, name='update_server'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]

