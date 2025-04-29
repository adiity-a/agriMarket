"""
URL configuration for agrimarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from users import views as uviews
from . import views
from products import views as pviews
from bidding import views as bviews

urlpatterns = [
    path("super/", admin.site.urls),
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("home/", views.home, name="home"),
    path("admin/", uviews.admin, name="admin"),
    path("buyer/", uviews.buyer, name="buyer"),
    path("farmer/", uviews.farmer, name="farmer"),
    path("add-product/", pviews.add_product, name="add-product"),
    path("edit-product/<product_id>", pviews.edit_product, name="edit-product"),
    path("place-bid/<product_id>", bviews.place_bid, name="place-bid"),
    path('admin/manage_users/', uviews.manage_users, name='manage_users'),
    path('admin/manage_products/', uviews.manage_products, name='manage_products'),
    path('admin/manage_bids/', uviews.manage_bids, name='manage_bids'),
    path('admin/delete_user/<int:user_id>/', uviews.delete_user, name='delete_user'),
    path('admin/delete_product/<int:product_id>/', uviews.delete_product, name='delete_product'),
    path("my-bids/", bviews.my_bids, name="my_bids"),
    path("edit-bid/", bviews.edit_bid, name="edit_bid"),
    path("remove-bid/", bviews.remove_bid, name="remove_bid"),
    path('predict/', views.predict_price, name='predict_price'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
