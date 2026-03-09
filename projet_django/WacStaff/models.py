from django.db import models


class Collaborateur(models.Model):
    name = models.CharField(max_length=100, unique=True)
    prenom = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date1ereEmbauche = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField
    password = models.CharField(max_length=200, unique=True) | None
    

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name




class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')

    def __str__(self):
        return self.title
