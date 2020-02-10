"""billing_gateway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

from api.views import auth, accounts, transfer, operations


urlpatterns = [
    path('admin/', admin.site.urls),

    #
    # API
    #
    path('signup', auth.SignupView.as_view()),
    path('login', auth.LoginView.as_view()),
    path('transfer', transfer.TransferView.as_view()),
    path('accounts', accounts.AccountListView.as_view()),
    path('operations', operations.OperationListView.as_view()),
]
