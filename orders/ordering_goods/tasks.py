from django.http import JsonResponse
from orders.celery import app
from requests import get
from yaml import load, Loader
from .models import *


@app.task
def price_loader(url, user_id):
    stream = get(url).content
    data = load(stream, Loader=Loader)
    shop, _ = Shop.objects.get_or_create(user_id=user_id, name=data['shop'])
    for category in data['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.shops.add(shop.id)
        category_object.save()
    ProductInfo.objects.filter(shop_id=shop.id).delete()
    for item in data['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])
        product_info = ProductInfo.objects.create(product_id=product.id,
                                                  external_id=item['id'],
                                                  model=item['model'],
                                                  price=item['price'],
                                                  price_rrc=item['price_rrc'],
                                                  quantity=item['quantity'],
                                                  shop_id=shop.id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductInfoParameter.objects.create(product_info_id=product_info.id,
                                                parameter_id=parameter_object.id,
                                                value=value)