from django.db import models
from django.contrib.auth.models import User


class PositionUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    position = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.position


class Unversity_Pbooks(models.Model):

    font_shrift_choices = [
        ('LOTIN', 'Lotin'),
        ('CYRILLIC', 'Cyrillic'),
    ]


    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, null=True, blank=True)
    genres = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    font_shrift = models.CharField(max_length=20, choices=font_shrift_choices, default='LOTIN')

    def __str__(self):
        return self.title


class UbookImage(models.Model):
    book = models.ForeignKey(Unversity_Pbooks, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ubook_images')

    def __str__(self):
        return self.book.title

class Unversity_Ebook(models.Model):
    font_shrift_choices = [
        ('LOTIN', 'Lotin'),
        ('CYRILLIC', 'Cyrillic'),
    ]

    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, null=True, blank=True)
    genres = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    font_shrift = models.CharField(max_length=20, choices=font_shrift_choices, default='LOTIN')

    def __str__(self):
        return self.title

class Ebook(models.Model):
    book = models.ForeignKey(Unversity_Ebook, on_delete=models.CASCADE,related_name='file')
    book_file = models.FileField(upload_to='books')

    def __str__(self):
        return self.book.title


class Students_book(models.Model):
    cover_choices = [
        ('PB', 'Paperback'),
        ('EB', 'E-book'),
    ]

    title = models.CharField(max_length=200)
    cover = cover = models.CharField(max_length=20, choices=cover_choices, default='HC')
    authors = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class SbookImage(models.Model):
    book = models.ForeignKey(Students_book, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sbook_images')

    def __str__(self):
        return self.book.title

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='messages')
    book = models.ForeignKey(Unversity_Pbooks, on_delete=models.CASCADE, related_name='messages')
    kurs = models.IntegerField(default=1)
    student_id = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.user.username
    
class Reply(models.Model):
    ruxsat_choices = [
        ('Ruxsat',True),
        ('Mumkinmas',False)
    ]

    message = models.ForeignKey(Message,on_delete=models.CASCADE, related_name='reply')
    description = models.TextField()
    ruxsat = models.CharField(max_length=10,choices=ruxsat_choices, default='Mumkinmas')
