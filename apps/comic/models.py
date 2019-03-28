from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+(\s[a-zA-Z]+)?$')
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name'])< 3:
            errors['first_name'] = "First name should be at least 2 characters"
        elif not 'first_name' in errors and not re.match(NAME_REGEX, postData['first_name']):
            errors['first_name'] = "First name must only contain letters"
        if not 'email' in errors and not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Email is invalid"
        if len(postData['password'])< 8:
            if len(postData['password'])< 1:
                errors['password'] = "Password can't be blank"
            errors['password'] = "Password should be no fewer than 8 characters in length"
        if postData['conf_password'] != postData['password']:
            errors['conf_password'] = "Passwords do not match"
        return errors
        
    def login_validator(self, postData):
        errors = {}
        if len(postData['email1']) < 1:
            errors['email1'] = "Not a valid email"
        if len(User.objects.filter(email=postData['email1'])) == 0:
            errors['email1'] = "Email does not exist. Register first!"
        if len(User.objects.filter(email=postData['email1'])) == 1:
            password_hash = User.objects.get(email=postData['email1']).password
            if bcrypt.checkpw(postData['password1'].encode(), password_hash.encode()) == False:  
                errors['password1'] = "Incorrect password. Try again!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, unique=True )
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "<User_object: {} {} {}>".format(self.first_name, self.email)

class ComicManager(models.Manager):
    def comic_validator(self, postData):
        errors = {}
        if len(postData['title']) < 4:
            errors['title'] = "Title should be more then 3 characters"
        return errors
        
class Comic(models.Model):
    title = models.CharField(max_length=255, blank=False)
    desc = models.TextField(blank=True)
    docfile = models.FileField(blank=True, upload_to='media/')
    qty = models.IntegerField(blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    price_sold = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    profit = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    date_of_purchase = models.DateField(null=True, blank=True, default='2019-01-01')
    date_of_sale = models.DateField(null=True, blank=True, default='2019-01-01')
    author = models.ForeignKey(User, related_name="comics", on_delete=models.CASCADE)
    my_collection = models.ManyToManyField(User, related_name="added_to_my_collect_comic")
    wishlist = models.ManyToManyField(User, related_name="added_to_wishlist_comic")
    sold = models.ManyToManyField(User, related_name="added_to_sold_comic")
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    creator = models.CharField(max_length=255, blank=True)
    year = models.DateField(null=True, blank=True, default='2019-01-01')
    cover = models.CharField(max_length=255, blank=True)
    
    objects = ComicManager()
    
    def __repr__(self):
        return "<Comic_object: {} {} {} {} {} {} >".format(self.title, self.price, self.price_sold, self.date_of_purchase, self.date_of_sale, self.author)