from django.db import models
from composite_field import CompositeField

class Brand(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=255, db_column='name')
    color = models.CharField(max_length=18, blank=True, db_column='color')
    url = models.CharField(max_length=200, blank=True, db_column='url')

    class Meta:
        db_table = 'brands'


class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name_ru = models.CharField(max_length=200, db_column='name_ru')
    name_uz = models.CharField(max_length=200, db_column='name_uz')
    site_picture = models.CharField(max_length=100, db_column='site_picture')
    collections = models.BooleanField(db_column='collections')
    sort = models.IntegerField(db_column='sort')

    class Meta:
        db_table = 'categories'


class BrandCategory(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_column='brand_id')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category_id')

    class Meta:
        db_table = 'brands_categories'
        unique_together = (('brand', 'category'),)