from django.contrib import admin
from .models import Book, CustomUser  # 👈 Import your custom user model
from django.contrib.auth.admin import UserAdmin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)

@admin.register(CustomUser)  # 👈 Register your custom user model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff']
