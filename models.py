from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class Species(models.Model):
    species = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )

    def __str__(self):
        return self.species


class Breed(models.Model):
    breed = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )

    def __str__(self):
        return self.breed


class Color(models.Model):
    color = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )

    def __str__(self):
        return self.color


class Sex(models.Model):
    sex = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )

    def __str__(self):
        return self.sex


class Age(models.Model):
    age = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )

    def __str__(self):
        return self.age


class Pet(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True)
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    sex = models.ForeignKey(Sex, on_delete=models.SET_NULL, null=True)
    age = models.ForeignKey(Age, on_delete=models.SET_NULL, null=True)
    pet_id = models.PositiveIntegerField()

    # Shows up in the admin list
    def __str__(self):
        return self.name + " " + "(" + self.species.__str__() + "|" + self.breed.__str__() + ")" + ": " + self.sex.__str__()\
		        + " " + self.color.__str__() + " " + self.age.__str__() + " " + str(self.pet_id)





