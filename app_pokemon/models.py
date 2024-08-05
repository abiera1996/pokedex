from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Ability(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    photo = models.URLField()
    types = models.ManyToManyField(Type)
    abilities = models.ManyToManyField(Ability)
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return self.name