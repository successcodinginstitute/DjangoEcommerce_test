# from django.contrib import admin

# # Register your models here.

# from .models import Product, Category

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'price', 'rating', 'is_bestseller')
#     list_filter = ('category', 'is_bestseller')
#     search_fields = ('name', 'description')


# from django.contrib import admin
# from .models import BlogPost

# admin.site.register(BlogPost)

from django.contrib import admin
from .models import Product, Category, BlogPost

# Register Product model with custom admin interface
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating', 'is_bestseller')
    list_filter = ('category', 'is_bestseller')
    search_fields = ('name', 'description')

# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Shows the category name in the list view

# Register BlogPost model (assuming it's defined elsewhere)
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'date')  # Use 'date' instead of 'published_date'
    search_fields = ('title', 'description', 'author')  # You can also search by author or description

# admin.site.register(UserProfile)