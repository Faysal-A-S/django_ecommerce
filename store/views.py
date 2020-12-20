from django.shortcuts import render, redirect
from .models import Product, Order, OrderItem, ShippingAddress
import json
from django.http import JsonResponse
from django.contrib import auth
import datetime
from django.contrib.auth.models import User

# Create your views here.


def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity
    else:
        items = []
        order = {'get_cart_quantity': 0,
                 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()

        cartItems = order.get_cart_quantity
        print(order.shipping)
    else:
        items = []
        order = {'get_cart_quantity': 0,
                 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
    return render(request, "store/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(action)
    print(productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Product was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_items):
            order.complete = True
        order.save()
        if order.shipping == True:

            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],


            )
            print(data['shipping']['address'])

    else:
        print('Not logged in...')
    print(customer)
    print(order)
    return JsonResponse('Payment submitted', safe=False)


def searches(request, search):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    product = Product.objects.filter(pname__icontains=search)

    #  print(tvseries.id)
    context = {
        'products': product,
        'cartItems': cartItems

    }
    return render(request, 'store/searches.html', context)


def search(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.filter(catagory=id).order_by('-id')

    context = {
        'products': products,
        'cartItems': cartItems

    }
    return render(request, 'store/search.html', context)


def login(request):
    if request.method == 'POST':
        username3 = request.POST['signinuser']
        password2 = request.POST['signinpass']

        user = auth.authenticate(username=username3, password=password2)
        if user is None:
            return render(request, 'store/login.html', {'lerror': 'Incorrect username or password'})

        else:
            auth.login(request, user)
            return redirect('store')

    elif request.method == 'GET':
        return render(request, 'store/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['signupuser']
        password = request.POST['signuppass']
        cpassword = request.POST['confirmsignuppass']
        print(username, password)
        if password == cpassword:
            try:
                user = User.objects.get(username=username)
                return render(request, 'store/register.html', {'error': 'Username already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=username, password=password)
                user.save()
                auth.login(request, user)
                return redirect('store')

        else:
            return render(request, 'store/register.html', {'rerror': 'Password doesn\'t match'})
    elif request.method == 'GET':
        return render(request, 'store/register.html')


def logout(request):
    auth.logout(request)
    return redirect('store')
