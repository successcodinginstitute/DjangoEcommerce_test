from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now


# Create your models here.

# class Product(models.Model):
#     CATEGORY_CHOICES = [
#         ('sunscreen', 'Sunscreen'),
#         ('moisturizer', 'Moisturizer'),
#         ('serum', 'Serum'),
#         ('facewash', 'Facewash'),
#     ]

#     name = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='products/')
#     description = models.TextField()
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     rating = models.FloatField()
#     reviews = models.PositiveIntegerField()
#     is_bestseller = models.BooleanField(default=False)
#     tag_line = models.CharField(max_length=255, blank=True, null=True)

#     # ✅ The field that was missing
#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    # def __str__(self):
    #     return self.name
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='categories/', default='categories/default.jpg')
    description = models.TextField(default='')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.FloatField()
    reviews = models.PositiveIntegerField()
    is_bestseller = models.BooleanField(default=False)
    tag_line = models.CharField(max_length=255, blank=True, null=True)
    
    # ForeignKey to Category model
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)  


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)  


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    ], default='Pending')
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)  # Ensure this field exists

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class SkincareProduct(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='skincare/')
    description = models.TextField()
    skin_type = models.CharField(max_length=100)
    rating = models.FloatField()
    reviews = models.PositiveIntegerField()
    weight = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.CharField(max_length=50, blank=True)
    tag = models.CharField(max_length=50, default='JUST IN 💗')

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    # CATEGORY_CHOICES = [
    #     ('Sunscreens', 'Sunscreens'),
    #     ('Skin Care', 'Skin Care'),
    #     ('Routine', 'Routine'),
    # ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Link to Category model
    author = models.CharField(max_length=100)
    date = models.DateField()
    image = models.ImageField(upload_to='blog_images/')

    def __str__(self):
        return self.title

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=15, blank=True)
#     profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.jpg', blank=True)

#     def __str__(self):
#         return self.user.username