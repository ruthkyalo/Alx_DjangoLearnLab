from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Display fields
    search_fields = ('title', 'author')                     # Enable search
    list_filter = ('publication_year',)                     # Filter by year
