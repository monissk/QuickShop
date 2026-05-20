from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
from datetime import datetime
from django.contrib import messages
import razorpay
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'home.html', params)

def searchMatch(query, item):
    if query.lower() in item.desc.lower() or \
       query.lower() in item.product_name.lower() or \
       query.lower() in item.category.lower():
        return True
    else:
        return False
    
def search(request):
    query = request.GET.get('search', '')

    allProds = []

    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)

        prod = [item for item in prodtemp if searchMatch(query, item)]

        if len(prod) > 0:
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))

            allProds.append([prod, range(1, nSlides), nSlides])

    params = {
        'allProds': allProds,
        'msg': ""
    }

    if len(allProds) == 0 or len(query) < 2:
        params = {
            'msg': "Please make sure to enter relevant search query"
        }

    return render(request, 'search.html', params)

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Password match check
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('/')
        
        # Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/')
        
        # Create user
        myuser = User.objects.create_user(
            username=username,
            email=email,
            password=pass1
        )
        myuser.save()
        messages.success(request, "Signup Successful!")
        return redirect('/')

    return redirect('/')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(
            username=loginusername,
            password=loginpassword
        )
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/')

    return redirect('/')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('/')

def electronics(request):
    allProds = []
    prod = Product.objects.filter(category='Electronic')
    n = len(prod)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'electronics.html', params)

def cloths(request):
    allProds = []
    prod = Product.objects.filter(category='Cloth')
    n = len(prod)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'cloths.html', params)

def shoes(request):
    allProds = []
    prod = Product.objects.filter(category='Shoes')
    n = len(prod)
    nSlides = n // 4 + ceil((n / 4) - (n // 4))
    allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shoes.html', params)
    
def prodView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'prodView.html', {'product':product[0]})

def cart(request):
    thank = False
    id = None
    if request.method == 'POST':
        items_json = request.POST.get('itemsJson', '')
        cardHolderName = request.POST.get('cardHolderName', '')
        cardNumber = request.POST.get('cardNumber', '')
        cardExpiry = request.POST.get('cardExpiry', '')
        cardCvv = request.POST.get('cardCvv', '')
        amount = request.POST.get('amount', '0')

        try:
            amount = int(amount)
        except ValueError:
            amount = 0

        order = Orders(
            items_json=items_json,
            cardHolderName=cardHolderName,
            cardNumber=cardNumber,
            cardExpiry=cardExpiry,
            cardCvv=cardCvv,
            amount=amount
        )
        order.save()

        # OrderUpdate.objects.create(
        #     order_id=order.order_id,
        #     update_desc="The order has been placed"
        # )
        # update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        # update.save()
        thank = True
        id = order.order_id

        # messages.success(request, "Thank you! Your Order has been placed.")
        # return redirect('/')

    return render(request, 'cart.html', {'thank':thank, 'id': id})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        amount = int(request.POST.get('amount', 0))
        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )
        payment = client.order.create({
            'amount': amount * 100,
            'currency': 'INR',
            'payment_capture': '1'
        })
        order = Orders(
            items_json=items_json,
            amount=amount,
            payment_id=payment['id']
        )
        order.save()
        params = {
            'payment': payment,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount': amount
        }
        return render(request, 'payment.html', params)

    return redirect('/')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        textarea = request.POST.get('textarea')

        contact_obj = Contact(
            name=name,
            email=email,
            address=address,
            phone=phone,
            city=city,
            state=state,
            zip=zip,
            textarea=textarea,
            date=datetime.today()
        )
        contact_obj.save()
        messages.success(request, "Thank you! Your message has been sent.")
        return redirect('contact') 

    return render(request, 'contact.html')