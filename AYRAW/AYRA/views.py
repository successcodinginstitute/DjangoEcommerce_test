from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import BlogPost
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.shortcuts import render
from .models import SkincareProduct,Category
from .forms import RequestDemoForm, SalesInquiryForm, CustomerSupportForm
# In your views.py file
from django.shortcuts import render, redirect
from .forms import RequestDemoForm
from .forms import SalesInquiryForm
from .forms import CustomerSupportForm
from .models import Product,Order 
from django.db.models import Q
# views.py
from django.shortcuts import render
import requests
from django.shortcuts import redirect, render
from django.http import HttpResponse
import hmac
import hashlib
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from collections import defaultdict
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Wishlist
from django.core.mail import send_mail
from django.conf import settings

def shipping_policy(request):
    context = {
        'title': 'Shipping Policy',
        'shipping_options': [
            {
                'name': 'Standard Shipping',
                'price': '$5.99',
                'time': '3-5 business days',
                'description': 'Our most economical shipping option'
            },
            {
                'name': 'Express Shipping',
                'price': '$12.99',
                'time': '1-2 business days',
                'description': 'Get your order faster'
            },
            {
                'name': 'Free Shipping',
                'price': 'FREE',
                'time': '5-7 business days',
                'description': 'On orders over $50'
            }
        ],
        'faqs': [
            {
                'question': 'How do I track my order?',
                'answer': 'Once your order ships, you will receive a tracking number via email.'
            },
            {
                'question': 'Do you ship internationally?',
                'answer': 'Yes, we ship to most countries. International shipping rates apply.'
            },
            {
                'question': 'What if my package is lost or damaged?',
                'answer': 'Please contact our customer service within 7 days of delivery.'
            }
        ]
    }
    return render(request, 'shipping_policy.html', context)

def all_products(request):
    products = Product.objects.all()
    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    print("products",products)
    return render(request, 'all_products.html', {'products': products,'wishlist_product_ids': wishlist_product_ids,})

def products(request):
    products = Product.objects.all()
    products_list = list(products)
    return JsonResponse({'products': products_list})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print("prodcut deatils",product )
    return render(request, 'product_detail.html', {'product': product})

def toggle_wishlist(request):
    if request.method == "POST" and request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if not created:
            wishlist_item.delete()
            return JsonResponse({'added': False})
        else:
            return JsonResponse({'added': True})

    return JsonResponse({'error': 'Unauthorized'}, status=401)

def search_products(request):
    query = request.GET.get('q')
    products = []
    if query:
        products = Product.objects.filter(name__icontains=query)

    return render(request, 'search_results.html', {'products': products, 'query': query})

def customer_support(request):
    if request.method == 'POST':
        form = CustomerSupportForm(request.POST)
        if form.is_valid():
            return redirect('contact')
    else:
        form = CustomerSupportForm()
    return render(request, 'your_template.html', {'form': form})

def sales_inquiry(request):
    if request.method == 'POST':
        form = SalesInquiryForm(request.POST)
        if form.is_valid():
            # You can save form or send email here
            return redirect('contact')
    else:
        form = SalesInquiryForm()
    return render(request, 'your_template.html', {'form': form})

def request_demo(request):
    if request.method == 'POST':
        form = RequestDemoForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email, save to the database)
            return redirect('contact')  # Redirect to the contact page after success
    else:
        form = RequestDemoForm()

    return render(request, 'your_template.html', {'form': form})


def home(request):
    sunscreens = Product.objects.filter(category=1)[:10]
    print(sunscreens)
    moisturizers = Product.objects.filter(category=2)[:10]
    serums = Product.objects.filter(category=3)[:10]
    facewash = Product.objects.filter(category=3)[:10]
    categories = Category.objects.all()
    print("Categories==>",categories)
    # category = get_object_or_404(Category, id=category_id)
    products = Product.objects.all()
    categories = Category.objects.all()
    products = Product.objects.select_related('category').all()

    grouped = defaultdict(list)
    for product in products:
        grouped[product.category].append(product)
    print(grouped.items())
    
    context = {
        'sunscreens': sunscreens,
        'moisturizers': moisturizers,
        'serums': serums,
        'facewash': facewash,
        'category': categories,
        'products': products,
        'grouped_products': grouped.items()
    }

    return render(request, 'home.html', context)

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  # Change 'home' to your homepage URL name
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, 'login.html')


def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {
        'category': category,
        'products': products
    })

def skincare_view(request):
    products = SkincareProduct.objects.all()
    return render(request, 'skincare.html', {'products': products})

def cleanser_detail(request):
    return render(request, 'cleanser_detail.html')

def skincare_list(request):
    return render(request, 'skincare.html') 

# def home(request):
#     sunscreens = Product.objects.filter(category='sunscreen')
#     return render(request, 'home.html', {'sunscreens': sunscreens})

def skincare(request):
    return render(request, 'skincare.html')

def scalpcare(request):
    return render(request, 'scalpcare.html')

def skincare_products(request):
    return render(request, 'skincare.html')

def scalpcare_products(request):
    return render(request, 'scalpcare/scalpcare_products.html')

def weightloss_products(request):
    return render(request, 'weightloss.html')

def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'profile': profile, 'form': form, 'user': request.user})

def weightloss(request):
    return render(request, 'weightloss.html')

def about(request):
    return render(request, 'about.html')

def user_guide(request):
    return render(request, 'user_guide.html')

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = request.session.get('cart', {})

    if slug in cart:
        cart[slug]['quantity'] += 1
    else:
        cart[slug] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1,
            'image': product.image.url
        }

    request.session['cart'] = cart
    return redirect('cart_view')

def remove_from_cart(request, slug):
    cart = request.session.get('cart', {})
    if slug in cart:
        del cart[slug]
    request.session['cart'] = cart
    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'cart.html', {'cart': cart, 'total': total})

# def cart_count(request):
#     if request.user.is_authenticated:
#         count = Cart.objects.filter(user=request.user).count()
#     else:
#         count = 0
#     return {'cart_count': count}

def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_view')
    total_price = Decimal('0.00')  # initialize as Decimal
    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            total_price=item.product.price * item.quantity,
            status='Pending',
        )
        total_price += item.product.price * item.quantity
        item.delete()
    request.session['total_price'] = float(total_price)
    # messages.success(request, "Your order has been placed successfully!")
    return redirect('payment')  # You can show a simple success page


@login_required(login_url='login')
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')  # latest first
    context = {
        'orders': orders,
    }
    return render(request, 'order_list.html', context)

from django.shortcuts import render, redirect
from instamojo_wrapper import Instamojo

# Instamojo test credentials
API_KEY = '801643e8bf855eeff0252a0b03df48e5'
AUTH_TOKEN = '970dd00bcc5ba487a7f13687cef69dda'
# ENDPOINT = 'https://test.instamojo.com/api/1.1/'
ENDPOINT = 'https://www.instamojo.com/api/1.1/'


api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint=ENDPOINT)

def payment(request):
    total_price = request.session.get('total_price', 0)

    # Create payment request with Instamojo
    response = api.payment_request_create(
        amount=str(total_price),
        purpose='Order Payment',
        buyer_name='Test User',
        send_email=True,
        email='test@example.com',  # You can make this dynamic
        redirect_url='http://localhost:8000/payment-success/'
        # redirect_url=use

    )

    payment_url = response['payment_request']['longurl']
    return redirect(payment_url)

def payment_success(request):
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('payment_status')

    return render(request, 'payment_success.html', {
        'payment_id': payment_id,
        'status': status,
    })

INSTAMOJO_SALT = '2d7e011ecacc4211af1018e09d7b466a'  # From Instamojo dashboard

@csrf_exempt
def instamojo_webhook(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    try:
        post_data = request.POST.copy()
        received_mac = post_data.pop('mac', [None])[0]

        sorted_keys = sorted(post_data)
        message = "|".join(str(post_data[key]) for key in sorted_keys)

        # Calculate HMAC to verify authenticity
        generated_mac = hmac.new(
            INSTAMOJO_SALT.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha1
        ).hexdigest()

        if received_mac != generated_mac:
            return HttpResponse("MAC mismatch", status=400)

        # Extract payment info
        payment_status = post_data.get("status")
        payment_id = post_data.get("payment_id")
        buyer_email = post_data.get("buyer")

        if payment_status == "Credit":
            # ✅ Payment was successful — process your logic
            print(f"✅ Payment confirmed for {buyer_email}, ID: {payment_id}")
            # Example: update order status in DB here

        return HttpResponse("Webhook received", status=200)

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

# def payment(request):
#     total_price = request.session.get('total_price', 0)

#     payload = {
#         'purpose': 'Order Payment',
#         'amount': str(total_price),
#         'buyer_name': 'John Doe',
#         'email': 'john@example.com',
#         'phone': '9270707122',
#         'redirect_url': 'http://localhost:8000/payment-success/', #'https://yourdomain.com/payment-success/',
#         'allow_repeated_payments': 'False',
#         'send_email': 'True',
#         'send_sms': 'True',
#     }

#     headers = {
#         'X-Api-Key': API_KEY,
#         'X-Auth-Token': AUTH_TOKEN
#     }

#     response = requests.post(
#         'https://www.instamojo.com/api/1.1/payment-requests/',
#         data=payload,
#         headers=headers
#     )

#     try:
#         response_data = response.json()
#     except Exception:
#         return HttpResponse("Invalid response from Instamojo")

#     if response_data.get('success'):
#         payment_url = response_data['payment_request']['longurl']
#         return redirect(payment_url)
#     else:
#         error_msg = response_data.get('message', 'Unknown error')
#         return HttpResponse(f"Payment request failed: {error_msg}")


# def payment(request):
#     total_price = request.session.get('total_price', 0)
    
#     context = {
#         'total_price': total_price,
#     }
#     return render(request, 'payment.html', context)

# import razorpay
# from django.conf import settings
# from django.shortcuts import render

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# def payment(request):
#     total_price = float(request.session.get('total_price', 0))
#     amount_paise = int(total_price * 100)

#     payment = client.order.create({
#         "amount": amount_paise,
#         "currency": "INR",
#         "payment_capture": 1
#     })

#     context = {
#         'total_price': total_price,
#         'razorpay_order_id': payment['id'],
#         'razorpay_amount': amount_paise,
#         'razorpay_key': settings.RAZORPAY_KEY_ID,
#     }
#     return render(request, 'payment.html', context)

# def order_success(request):
#     return render(request, 'order_success.html')

def order_success(request):
    if request.user.is_authenticated:
        # Get the latest order for the user
        latest_order = Order.objects.filter(user=request.user).order_by('-order_date').first()
        
        if latest_order:
            subject = 'Order Confirmation - AYRA'
            message = f"""
            Hello {request.user.username},
            
            Thank you for your purchase!
            Your order (Order ID: {latest_order.id}) has been placed successfully.

            Product: {latest_order.product.name}
            Total Price: ₹{latest_order.total_price}
            Status: {latest_order.status}

            We will notify you once your order is shipped.
            """

            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email]

            send_mail(subject, message, from_email, recipient_list)

    return render(request, 'order_success.html')

def moisturizer_detail(request):
    return render(request, 'moisturizer.html')

def serum_detail(request):
    return render(request, 'serum.html')

def sheet_mask_detail(request):
    return render(request, 'sheetmask.html')

def sunscreen_detail(request):
    return render(request, 'sunscreen.html')

def toner_detail(request):
    return render(request, 'toner.html')

def cleanser_detail(request):
    return render(request, 'cleanser.html')


def hair_oil(request):
    return render(request, 'hairoil.html')

def hair_mask(request):
    return render(request, 'hairmask.html')

def shampoo(request):
    return render(request, 'shampoo.html')

def hairspray(request):
    return render(request, 'hairspray.html')

def fat_capsule(request):
    return render(request, 'fatburnercapsule.html')

def appetite(request):
    return render(request, 'appetite.html')

def weightloss_coffee(request):
    return render(request, 'weightloss_coffee.html')

def metabolism(request):
    return render(request, 'metabolism boost.html')


login_required(login_url='login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product already exists in wishlist
    if Wishlist.objects.filter(user=request.user, product=product).exists():
        messages.warning(request, "Product is already in your wishlist!")
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, "Product added to wishlist!")
    
    return redirect('wishlist_view')

@login_required(login_url='login')
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, "Product removed from your wishlist.")
    else:
        messages.warning(request, "Product was not in your wishlist.")
    
    return redirect('wishlist_view')
# View Wishlist (Only Logged-in User's Wishlist)
@login_required(login_url='login')
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

# Add to Cart
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product already exists in cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, "Product quantity updated in cart!")
    else:
        messages.success(request, "Product added to cart!")
    
    return redirect('cart_view')

# View Cart (Only Logged-in User's Cart)
@login_required(login_url='login')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate total price and total items
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_total': total_price,
        'cart_count': total_items
    }
    return render(request, 'cart.html', context)

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Cart, Product

@login_required(login_url='login')
def update_qty(request, product_id, action):
    cart_item = get_object_or_404(Cart, product_id=product_id, user=request.user)

    if action == 1:  # Increase quantity
        cart_item.quantity += 1
    elif action == 0:  # Decrease quantity
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            messages.warning(request, "Quantity cannot be less than 1!")
    
    cart_item.save()
    return redirect('cart_view')  

def contact(request):
    request_demo_form = RequestDemoForm()
    sales_inquiry_form = SalesInquiryForm()
    customer_support_form = CustomerSupportForm()

    return render(request, 'contact.html', {
        'request_demo_form': request_demo_form,
        'sales_inquiry_form': sales_inquiry_form,
        'customer_support_form': customer_support_form
    })




from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from AYRA.forms import RegisterForm  # Import the form

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# User Login
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  # Change 'home' to your homepage URL name
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, 'login.html')

# User Logout
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('/')


def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Here you would typically generate a password reset token
            # and send it via email. This is a simplified example:
            
            reset_link = f"http://127.0.0.1:8000/reset_password/"#f"http://yourdomain.com/reset-password/{user.pk}/"
            subject = 'Password Reset Request'
            message = f'Hello {user.username},\n\nClick the link to reset your password: {reset_link}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list)
            
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('forget_password')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
            return render(request, 'forget_password.html')
    
    return render(request, 'forget_password.html')

from django.shortcuts import render

def faq_view(request):
    category = request.GET.get("category", "product")

    faqs = {
        "product": [
            {"question": "What are clean skincare products?", "answer": "They are free from harmful chemicals and safe for the skin."},
            {"question": "Are your products cruelty-free?", "answer": "Yes, we never test on animals."},
            {"question": "Do your products contain parabens?", "answer": "No, all our products are paraben-free."}
        ],
        "order": [
            {"question": "How can I track my order?", "answer": "Use the tracking link sent via email after purchase."},
            {"question": "Can I cancel my order?", "answer": "Yes, within 24 hours from the order time."},
            {"question": "Do you offer express shipping?", "answer": "Yes, it's available at checkout."}
        ],
        "payment": [
            {"question": "What payment methods do you accept?", "answer": "Credit cards, UPI, PayPal, and net banking."},
            {"question": "Is my payment info secure?", "answer": "Yes, we use encrypted payment gateways."},
            {"question": "Can I use promo codes?", "answer": "Yes, at the checkout page."}
        ]
    }

    return render(request, "faq.html", {
        "category": category,
        "faqs": faqs.get(category, [])
    })


def blog_list(request):
    posts = BlogPost.objects.all().order_by('-date')
    return render(request, 'blog_list.html', {'posts': posts})