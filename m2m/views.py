from django.http import JsonResponse
from .models import Brand, Category, BrandCategory
from django.db import connection
from django.http import HttpResponse
import json

def get_brands_in_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        brands = Brand.objects.filter(
            brandcategory__category=category
        )
        brand_list = [{'id': brand.id, 'name': brand.name} for brand in brands]
        data = {'brands': brand_list}
        return JsonResponse(data)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category does not exist'})


def get_categories_in_brand(request, brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)
        categories = Category.objects.filter(
            brandcategory__brand=brand
        )
        category_list = [{'id': category.id, 'name_ru': category.name_ru, 'name_uz': category.name_uz} for category in categories]
        data = {'categories': category_list}
        return JsonResponse(data)
    except Brand.DoesNotExist:
        return JsonResponse({'error': 'Brand does not exist'})



def get_brands_categories(request):
    with connection.cursor() as cursor:
        query = '''
            SELECT b.id, b.name, c.id, c.name_ru, c.name_uz
            FROM brands_categories bc
            JOIN brands b ON bc.brand_id = b.id
            JOIN categories c ON bc.category_id = c.id
        '''
        cursor.execute(query)
        results = cursor.fetchall()

    brand_category_list = []
    for result in results:
        brand_id, brand_name, category_id, category_name_ru, category_name_uz = result
        brand_category_list.append({
            'brand_id': brand_id,
            'brand_name': brand_name,
            'category_id': category_id,
            'category_name_ru': category_name_ru,
            'category_name_uz': category_name_uz,
        })

    return JsonResponse(brand_category_list, safe=False)

def insert_into_brands_categories(request):
    body = json.loads(request.body.decode('utf-8'))
    brand_id = body.get('brand_id')
    category_id = body.get('category_id')

    sql = """
    INSERT INTO brands_categories (brand_id, category_id)
    VALUES (%s, %s)
    """
    values = (brand_id, category_id)

    with connection.cursor() as cursor:
        cursor.execute(sql, values)

    connection.commit()

    return HttpResponse('Data inserted successfully')