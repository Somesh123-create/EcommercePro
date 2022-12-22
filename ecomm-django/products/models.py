from django.db import models

# Create your models here
class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, max_length=255)
    cat_image = models.ImageField(blank=True, upload_to='photos/categories')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name





class Product(models.Model):
    product_name = models.CharField(max_length=125)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    stock = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='product_cat',  on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.product_name
