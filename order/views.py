from django.http.request import HttpRequest
from product.models import Category, Product
from django.contrib import messages
from order.models import OrderDetail, ShopCart, ShopCartForm, OrderForm, Order
from django.http.response import  HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

from django.utils.crypto import get_random_string
from user.models import *
# Create your views here.
def index(request):
    return HttpResponse('order page')

# @login_required(login_url='/login') # Check login
def addToShopCart(request,id):
    url =  request.META.get('HTTP_REFERER') #get last url
    current_user = request.user #access user session information

    checkproduct = ShopCart.objects.filter(product_id = id) #ccheck product in shopcart
    if checkproduct:
        control = 1 #the product is in cart
    else:
        control = 0 #the product is not in cart

    if request.method == 'POST': #if there is a POST  (for product detail)
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save() #save data
            else: #insert to shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Cart")
        return HttpResponseRedirect(url)

    else: #if no POST ( just add one product)
        if control ==1 : #update shopcart
            data = ShopCart.objects.get(product_id = id)
            data.quantity += 1
            data.save()
        else: #insert to shopcart
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, "Product added to Cart")
        return HttpResponseRedirect(url)

def shopcart(request):
    category = Category.objects.all()
    current_user = request.user #access user session information
    shopcart = ShopCart.objects.filter(user_id = current_user.id)

    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    # return HttpResponse(str(total))
    
    context = {'shopcart': shopcart,
                'category':category,
                'total':total}
    return render(request, 'order/shopcart_products.html', context)

# @login_required(login_url='/login') # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted from Shop Cart")
    return HttpResponseRedirect("/shopcart")


def orderdetail(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode= get_random_string(5).upper() # random cod
            data.code =  ordercode
            data.save() #

            #move shopcart items to order detail item
            # shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderDetail()
                detail.order_id     = data.id # Order Id
                detail.product_id   = rs.product_id
                detail.user_id      = current_user.id
                detail.quantity     = rs.quantity
                detail.price        = rs.product.price
                detail.amount       = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
                #-----------------------

            ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'order/order_completed.html',{'ordercode':ordercode,'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderdetail")

    form= OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }
    return render(request, 'order/order_form.html', context)