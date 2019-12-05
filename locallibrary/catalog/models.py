from django.db import models
from django.urls import reverse  # Usado para gerar URLs, revertendo os padrões de URL
import uuid  # Necessário para instâncias de livros exclusivas


class Genre(models.Model):
    """Model representando um genero de livro."""
    name = models.CharField(max_length=200, help_text='Entre um genero de livro (e.g. Ficção Científica')

    def __str__(self):
        """String para representar o Model object."""
        return self.name


class Language(models.Model):
    """Modelo que representa um idioma (e.g. Inglês, Francês, Japonês, etc."""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese, etc.)")

    def __str__(self):
        """String representando o objeto Model."""
        return self.name

class Book(models.Model):
    """Model representando um livro (mas não uma cópia específica."""
    title = models.CharField(max_length=200)

    # Chave estrangeira usada porque o livro pode ter apenas um autor, mas os autores podem ter vários livros
    # Cria como uma string em vez de um objeto, porque ainda não foi declarado no arquivo
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Faça uma breve descrição do livro')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 caracteres <a href="https://www.isbn-international.org/content/what-isbn">Numero ISBN</a>')

    # ManyToManyField usado porque o gênero pode conter muitos livros. Os livros podem cobrir muitos gêneros
    # A classe de gênero já foi definida para que possamos especificar o objeto acima
    genre = models.ManyToManyField(Genre, help_text='Selecione um gênero para esse livro')

    def __str__(self):
        """String para representar o Model Object."""
        return self.title

    def get_absolute_url(self):
        """Retorna a url para acessar um registro detalhado deste livro."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Cria uma sequência para o Genre. Isso é necessário para exibir o Genre no Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Modelo que representa uma cópia específica de um livro (i. e. que pode ser emprestado da biblioteca)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ID exclusivo para este livro em particular em toda a biblioteca')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String para representar o objeto Model."""
        return f'{self.id} ({self.book.title}) {self.status} {self.due_back}'


class Author(models.Model):
    """Modelo representando um autor."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Retorna a url para acessar uma instância de autor específica."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String para representar o objeto model."""
        return f'{self.last_name}, {self.first_name}'
