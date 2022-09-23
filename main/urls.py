from django.urls import path, include
from . import views


urlpatterns= [
    path('category/', views.CategoryView.as_view(), name='category'),
    path('category/<int:category_id>/',views.CategoryDetailView.as_view(), name='category '),
    path('product', views.ProductView.as_view(), name='product item'),
    path('product/<int:product_id>/',views.ProductDetailView.as_view(), name='product'),
    path('cart/', views.CartView.as_view(), name='cart-view'),
    path('cart-item-delete/<int:item_id>/', views.CartDetailView().as_view(), name='detail-delete'),
    path('shopping-status/<int:item_id>/', views.shopping_status, name='status'),

    
]