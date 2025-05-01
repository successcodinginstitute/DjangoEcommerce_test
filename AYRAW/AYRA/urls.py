from django.urls import path
from . import views
from .views import faq_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('skincare/', views.skincare, name='skincare'),
    path('scalpcare/', views.scalpcare, name='scalpcare'),
    path('profile/', views.profile_view, name='profile'), 
    path('shop/all/', views.all_products, name='all_products'),
    # path('category_products', views.category_products, name='category_products'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),

    path('skincare/', views.skincare_view, name='skincare'),
    path('scalp-care/', views.scalpcare_products, name='scalpcare_products'),
    path('weight-loss/', views.weightloss_products, name='weightloss_products'),

    path('skincare/cleanser/', views.cleanser_detail, name='cleanser_detail'),
    path('skincare/', views.skincare_list, name='skincare'),  
    path('shipping-policy/', views.shipping_policy, name='shipping_policy'),
    path('weightloss/', views.weightloss, name='weightloss'),
    path('about/', views.about, name='about'), 
    path('user_guide/', views.user_guide, name='user_guide'), 
    # path('product/<int:product_id>/', views.product_view, name='product_view'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('update-qty/<int:product_id>/<int:action>/', views.update_qty, name='update_qty'),
    path('place-order/', views.place_order, name='place_order'),
    path('payment/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('instamojo-webhook/', views.instamojo_webhook, name='instamojo_webhook'),
    # path('razorpay-webhook/', views.razorpay_webhook, name='razorpay_webhook'),
    # https://30ac-106-221-216-216.ngrok-free.app/razorpay-webhook/

    path('my-orders/', views.order_list, name='order_list'),
    path('toggle-wishlist/', views.toggle_wishlist, name='toggle_wishlist'),

    path('order_success/', views.order_success, name='order_success'),
    #path('my-orders/', views.my_orders, name='my_orders'),
    #path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('contact/', views.contact, name='contact'),
    path('request_demo/', views.request_demo, name='request_demo'),  # Add this line
    path('sales_inquiry/', views.sales_inquiry, name='sales_inquiry'),  # 👈 Add this
    path('customer_support/', views.customer_support, name='customer_support'),
    path('search/', views.search_products, name='search_products'),

    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    
    path("faq/", faq_view, name="faq"),

    path('moisturizer/', views.moisturizer_detail, name='moisturizer_detail'),
    # Add other products similarly:
    path('serum/', views.serum_detail, name='serum_detail'),
    path('sheetmask/', views.sheet_mask_detail, name='sheet_mask_detail'),
    path('sunscreen/', views.sunscreen_detail, name='sunscreen_detail'),
    path('toner/', views.toner_detail, name='toner_detail'),
    path('cleanser/', views.cleanser_detail, name='cleanser_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    path('shampoo/', views.shampoo, name='serum_detail'),
    path('hairmask/', views.hair_mask, name='sheet_mask_detail'),
    path('hairoil/', views.hair_oil, name='sunscreen_detail'),
    path('hairspray/', views.hairspray, name='toner_detail'),

    path('fatburnercapsule/', views.fat_capsule, name='serum_detail'),
    path('appetite/', views.appetite, name='sheet_mask_detail'),
    path('weightloss_coffee/', views.weightloss_coffee, name='sunscreen_detail'),
    path('metabolism boost/', views.metabolism, name='toner_detail'),

    path('blog_list/', views.blog_list, name='blog_list'),
    # path('forget-password/', views.forget_password_view, name='forget_password')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)