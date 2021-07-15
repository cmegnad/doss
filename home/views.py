from order.views import shopcart
from home.models import Setting
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from  home.models import *
from product.models import Category, Comment, Images, Product
from order.models import ShopCart
import json

from home.forms import SearchForm
# Create your views here.
def index(request):

    setting = Setting.objects.get(pk = 1)
    category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4] #first 4 product
    product_newest = Product.objects.all().order_by('-create_at') #sản phẩm mới nhất
    products_lasted = Product.objects.all() #last 4 product
    products_picked = Product.objects.all().order_by('?')[:4] #random 4 product

    current_user = request.user #access user session information
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    page = "home"
    context = {'setting': setting, 
                'page': page, 
                'category':category,
                'products_slider':products_slider,
                'product_newest':product_newest,
                'products_lasted':products_lasted,
                'products_picked':products_picked,
                'total':total}
    return render(request, 'home/index.html', context)

def aboutUs(request):
    category = Category.objects.all()   #hiển thị thanh navbar
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,'category':category}
    return render(request, 'home/about.html', context)

def contact(request):
    category = Category.objects.all()  #hiển thị thanh navbar
    if request.method == 'POST': # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #save data to table
            messages.success(request,"Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactForm
    context = {'setting': setting, 'form': form,'category':category}
    return render(request, 'home/contact.html', context)


def category_products(request, id, slug):
    shopcart = ShopCart.objects.all()

    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    context = {'products':products,
                'category':category,
                'shopcart':shopcart
                }
    return render(request, 'home/category_products.html', context)


def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            shopcart = ShopCart.objects.all()

            category = Category.objects.all()
            context = {'products': products, 'query':query,
                       'category': category, 'shopcart':shopcart }
            return render(request, 'home/search_products.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    products = Product.objects.filter(title__icontains=q)
    results = []
    for rs in products:
      products_json = {}
      products_json = rs.title
      results.append(products_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    
    comments = Comment.objects.filter(product_id=id,status='True')
    context = {'product':product,
                'category':category,
                'images': images,
                'comments':comments,
                }
    return render(request, 'home/product_detail.html', context)
