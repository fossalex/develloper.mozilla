from django.contrib import admin
from .models import Author, Genre, Book, BookInstance


class BooksInline(admin.TabularInline):
    """Define o formato da inserção de livro (usado no AuthorAdmin)"""
    model = Book


# Define a classe admin
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


# Registra as classes admin para Book usando decorator.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


# Registra a classe admin para BookInstance usando decorator.
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


# Registra a classe admin com o modelo associado.
# admin.site.register(Book)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
# admin.site.register(BookInstance)
