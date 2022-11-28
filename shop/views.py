import requests
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required
from django.http import FileResponse


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def product_category(request, name):
    if name == 'fruits':
        products = Product.objects.filter(category__name='Fruits')
        return render(request, 'product_category.html', {'products': products})
    elif name == 'veggies':
        products = Product.objects.filter(category__name='Vegetables')
        return render(request, 'product_category.html', {'products': products})


@login_required
def product(request, id):
    product = Product.objects.get(id=id)
    prod_name = product.name
    # Parsing
    URL = f'https://en.wikipedia.org/wiki/{prod_name}'
    r = requests.get(URL)
    soup = bs(r.text, 'html.parser')
    fr = soup.find_all('p')
    fr_str = str(re.sub(r'\<[^>]*\>', '', str(fr)))[4:1100]
    i = fr_str.rfind('.')
    product.description = fr_str[:i+1]
    return render(request, 'product.html', {'product': product})


@login_required
def export(request):
    prods = Product.objects.all()
    data = ET.Element('data')
    for prod in prods:
        element = ET.SubElement(data, 'product')
        element.set('name', prod.name)
        element.set('price', str(prod.price))

    ET.ElementTree(data).write("products.xml", encoding='UTF-8')

    f = open('products.xml', 'rb')
    return FileResponse(f, as_attachment=True)


