from django.shortcuts import render, redirect
from django.http import HttpResponse
from math import ceil
from .models import Product, Cart, Wishlist, Wishlist_item, Product_category, Order_quantity, Order_item, Order, Cart_item
import re
from django.contrib.auth.models import User
import smtplib 
from email.message import EmailMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
#from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
# Create your views here.


def index(request):
	allProds = []
	catx = Product.objects.values('category')
	cats = {item['category'] for item in catx}
	for cat in cats:
		product = Product.objects.filter(category=cat)
		allProds.append([cat, product])

	# allProds = [params, params, params]
	"""if (request.user.is_authenticated):
		user = request.user
		userid = user.id
		a = Cart.objects.filter(user = request.user)
		cartid = a[0].cart_id
		carx = len(Cart_item.objects.filter(cart_id=cartid))
	else:"""
	carx = None
	params = {'list' : allProds, 'cart':carx }
	print("I ma in ")
	return render(request, 'pantry/index.html', params)

def register(request):
    carx = None
    if request.user.is_authenticated:
	    carx = len(Cart.objects.filter(user=request.user))
    if request.method == 'POST':
        forms = UserRegisterForm(request.POST)
        if forms.is_valid():
            forms.save()
            username = forms.cleaned_data.get('username')
            messages.success(request, f'{username} your account has been created. Log In to continue')
            return redirect('login')
    else:
        forms = UserRegisterForm()
    return render(request, 'pantry/register.html', {'form': forms, 'cart': carx})

def Login(request):
    if request.method == 'POST':
        loginusername = request.POST['loginuname']
        passw = request.POST['loginpass']

        user = authenticate(username=loginusername, password=passw)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")
    return redirect('home')

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

def Signup(request):
    if request.method == 'POST':
        username = request.POST['uname']
        fname = request.POST['uname']
        lname = request.POST['uname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Account has been successfully created")
        return redirect('home')
    else:
        return redirect('home')

def productview(request, cat):
	"""if(request.user.is_authenticated):
		carx = len(Cart.objects.filter(user=request.user))
	else : 
	"""
	carx = None
	product = Product.objects.all()
	a = []
	for i in product:
		if cat == i.category:
			a.append(i)
	
	return render(request, 'pantry/productview.html', {'list': a, 'cart': carx})

@login_required
def cart(request, idz, typer):
    mode = str(typer)
    id1 = int(idz)
    if mode == 'add':
        cart4 = Cart.objects.filter(user=request.user)
        print(cart4)
        if len(cart4) == 0:
            cart1 = Cart()
            cart1.user = request.user
            total_cost = 0
            cart1.save()
            cart4 = Cart.objects.filter(user = request.user)
        #wish4 = Wishlist.objects.filter(product_id=id1, user=request.user)
        cartprod = Cart_item.objects.filter(p_id = idz, cart_id = cart4[0].cart_id)
        print("\n\n\n\Manish\n\n\n\n\n\n\\n\n")
        print(cart4)
        if len(cartprod) == 0:
            cart1 = Cart_item()
            cart1.cart_id = cart4[0].cart_id
            cart1.p_id = idz
            cart1.prod_quantity = 1
            cart1.save()
        else:
            cart1 = Cart_item.objects.filter(p_id = idz)
            print(cart1)
            print("\n\n\n\\n\n\n\n\n\n\\n\n")
            #cart1.update(cart1.prod_quantity = cart1.prod_quantity + 1)
        #print("I am in add")
        #if wish4:
        #	wish4.delete()
        print("\n\n\n\\n\n\n\n\n\n\\n\n")
    elif mode == 'delete':
        cart2 = Cart.objects.get(user =request.user)
        if cart2:
            cart3 = Cart_item.objects.filter(p_id=id1,cart_id = cart[0].cart_id)
        if cart3:
            cart3.delete()
    elif mode == 'none':
        cart2 = Cart.objects.filter(user=request.user)
        if cart2:
            cart3 = Cart_item.objects.filter(cart2[0].cart_id)
        sum1 = 0
        for car in cart3:
            price = Product.objects.get(p_id = car.p_id).price
            sum1 = sum1 + price * car.prod_quantity
        return render(request, 'pantry/cart.html', {'cart1': cart3, 'sum': sum1, 'cart':len(cart3 = Cart_item.objects.filter(cart2[0].cart_id))})
    return redirect('home')

@login_required
def wishlist(request, idz, typer):
    mode = str(typer)
    id1 = int(idz)
    if mode == 'add':
        wishlist4 = Wishlist.objects.filter(product_id=id1, user=request.user)
        if not wishlist4:
            prod = Product.objects.get(pk=id1)
            cart1 = Wishlist()
            cart1.product_name = prod.product_name
            cart1.product_id = id1
            cart1.user = request.user
            cart1.image = prod.image
            cart1.price = prod.price
            cart1.quantity = 1
            cart1.category = prod.category
            cart1.subcategory = prod.subcategory
            cart1.save()
        else:
            cart1 = wishlist4.first()
            quan = cart1.quantity
            quan = quan + 1
            wishlist4.update(quantity=quan)
    elif mode == 'delete':
        cart3 = Wishlist.objects.filter(product_id=id1).first()
        if cart3:
            cart3.delete()
    elif mode == 'none':
        print('none')
        cart2 = Wishlist.objects.filter(user=request.user)
        return render(request, 'pantry/wishlist.html', {'cart1': cart2, 'cart':len(Cart.objects.filter(user=request.user))})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


"""
def grocery(request):
	if(request.user.is_authenticated):
		carx = len(Cart.objects.filter(user=request.user))
	else : 
		carx = None
	allProds = []
	catx = Product.objects.values('category')
	cats = {item['category'] for item in catx}
	for cat in cats:
		product = Product.objects.filter(category=cat)
		allProds.append([cat, product])

	# allProds = [params, params, params]
	params = {'list': allProds, 'slides': SlideShow.objects.all(), 'cart': carx}
	return render(request, 'shop/grocery.html', params)


def fruits(request):
	if(request.user.is_authenticated):
		carx = len(Cart.objects.filter(user=request.user))
	else : 
		carx = None
	allProds = []
	catx = Product.objects.values('category')
	cats = {item['category'] for item in catx}
	for cat in cats:
		if cat == 'Fruit':
			product = Product.objects.filter(category=cat)
			allProds.append([cat, product])
			params = {'list' : allProds, 'slides': SlideShow.objects.all(), 'cart': carx}
	return render(request, 'shop/fruits.html', params)


def vegetables(request):
	if(request.user.is_authenticated):
		carx = len(Cart.objects.filter(user=request.user))
	else : 
		carx = None
	allProds = []
	catx = Product.objects.values('category')
	cats = {item['category'] for item in catx}
	for cat in cats:
		if cat == 'vegetables':
			product = Product.objects.filter(category=cat)
			allProds.append([cat, product])
			params = {'list' : allProds, 'slides': SlideShow.objects.all(), 'cart': carx}
	return render(request, 'shop/vegetables.html', params)


def search_results(request):
	if(request.user.is_authenticated):
		carx = len(Cart.objects.filter(user=request.user))
	else : 
		carx = None
	search = request.GET.get('Search', 'default')
	products = Product.objects.all()
	a = []

	for i in products:
		if re.search(search, i.product_name, re.IGNORECASE):
			a.append(i)
	params = {'list': a, 'cart': carx}
	return render(request, 'shop/search.html', params)


def about(request):
	if(request.user.is_authenticated):
		carx = len(Cart.objects.filter(user=request.user))
	else : 
		carx = None
	return render(request, 'shop/about.html')


def contact(request):
	if(request.user.is_authenticated):
		carx = len(Cart.objects.filter(user=request.user))
	else : 
		carx = None
	return HttpResponse('we are at contact')


def tracker(request):
	if(request.user.is_authenticated):
		carx = len(Cart.objects.filter(user=request.user))
	else : 
		carx = None
	return HttpResponse('we are at tracker')


def search(request):
	if(request.user.is_authenticated):
		carx = len(Cart.objects.filter(user=request.user))
	else : 
		carx = None
	return HttpResponse('we are at search')

"""

"""

def order(request):
	if(request.user.is_authenticated):
		carx = len(Cart.objects.filter(user=request.user))
	else : 
		carx = None
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls() 
	s.login("wethestockedpantry@gmail.com", "Thestockedpantry@1234")
	msg = EmailMessage()
	subject = "Your Recent Order"
	message = "Dear " + str(request.user) + ", ordered products will be delivered to you within 2-3 working days."
	message = message + "\n"
	message = message + "Your Order:"
	message = message + "\n"
	cart = Cart.objects.filter(user=request.user)
	n = len(cart)
	list1 = []
	order = Orders()
	order.user = request.user
	order.product_name = 'default'
	sum1 = 0
	for car in cart:
		orderr = Orders()
		orderr.product_id = car.product_id
		orderr.user = request.user
		orderr.quantity = car.quantity
		orderr.category = car.category
		orderr.subcategory = car.subcategory
		orderr.price = car.price * car.quantity
		orderr.image = car.image
		orderr.product_name = car.product_name
		orderr.save()
		list1.append(orderr)
		sum1 = sum1 + car.price * car.quantity
		message = message + f"Product : {orderr.product_name}\tQuantity: {orderr.quantity}\tPrice: {orderr.price}\n"
	cart.delete()
	order.price = sum1
	profile = Profile.objects.filter(user=request.user).first()
	order.shipped = profile.address
	order.save()
	message = message + "\n"
	message = message + f"Total Price: {sum1}"
	message = message + "\n"
	message = message + " Thank you for using The Stocked Pantry.\n"
	msg.set_content(message)
	msg['Subject'] = subject
	msg['From'] = "wethestockedpantry@gmail.com"
	msg['To'] = request.user.email
	s.send_message(msg)
	s.quit()
	return render(request, 'shop/checkout.html', {'cart':len(Cart.objects.all()), 'list1': list1})

def register(request):
    carx = None
    if request.user.is_authenticated:
	    carx = len(Cart.objects.filter(user=request.user))
    if request.method == 'POST':
        forms = UserRegisterForm(request.POST)
        if forms.is_valid():
            forms.save()
            username = forms.cleaned_data.get('username')
            messages.success(request, f'{username} your account has been created. Log In to continue')
            return redirect('login')
    else:
        forms = UserRegisterForm()
    return render(request, 'users/register.html', {'form': forms, 'cart': carx})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'{username} your account has been updated!!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form, 
        'cart': len(Cart.objects.filter(user=request.user))
    }
    return render(request, 'users/profile.html', context)


@login_required
def cart(request, idz, typer, quant):
    mode = str(typer)
    id1 = int(idz)
    if mode == 'add':
        cart4 = Cart.objects.filter(product_id=id1, user=request.user)
        wish4 = Wishlist.objects.filter(product_id=id1, user=request.user)
        if not cart4:
            prod = Product.objects.get(pk=id1)
            cart1 = Cart()
            cart1.product_name = prod.product_name
            cart1.product_id = id1
            cart1.user = request.user
            cart1.image = prod.image
            cart1.price = prod.price
            cart1.quantity = 1
            cart1.category = prod.category
            cart1.subcategory = prod.subcategory
            cart1.save()
        else:
            cart1 = cart4.first()
            quan = cart1.quantity
            quan = quan + 1
            cart4.update(quantity=quan)
    
        if wish4:
            wish4.delete()
    elif mode == 'delete':
        cart3 = Cart.objects.filter(product_id=id1).first()
        if cart3:
            cart3.delete()
    elif mode == 'none':
        print('none')
        cart2 = Cart.objects.filter(user=request.user)
        sum1 = 0
        for car in cart2:
            sum1 = sum1 + car.price * car.quantity
        return render(request, 'users/cart.html', {'cart1': cart2, 'sum': sum1, 'cart':len(Cart.objects.filter(user=request.user))})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def wishlist(request, idz, typer, quant):
    mode = str(typer)
    id1 = int(idz)
    if mode == 'add':
        wishlist4 = Wishlist.objects.filter(product_id=id1, user=request.user)
        if not wishlist4:
            prod = Product.objects.get(pk=id1)
            cart1 = Wishlist()
            cart1.product_name = prod.product_name
            cart1.product_id = id1
            cart1.user = request.user
            cart1.image = prod.image
            cart1.price = prod.price
            cart1.quantity = 1
            cart1.category = prod.category
            cart1.subcategory = prod.subcategory
            cart1.save()
        else:
            cart1 = wishlist4.first()
            quan = cart1.quantity
            quan = quan + 1
            wishlist4.update(quantity=quan)
    elif mode == 'delete':
        cart3 = Wishlist.objects.filter(product_id=id1).first()
        if cart3:
            cart3.delete()
    elif mode == 'none':
        print('none')
        cart2 = Wishlist.objects.filter(user=request.user)
        return render(request, 'users/wishlist.html', {'cart1': cart2, 'cart':len(Cart.objects.filter(user=request.user))})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def history(request):
    orders = Orders.objects.filter(user=request.user)
    sum = 0
    for order in orders:
        if order.product_name == 'default':
            order.price = sum
            sum = 0
        else:
            if not order.iscancelled:
                sum = sum + order.price
    return render(request, 'users/history.html', {'orders': orders})


@login_required
def cancel_order(request, idz):
    id1 = int(idz)
    order = Orders.objects.get(user=request.user, product_id=id1, iscancelled = False)
    order.iscancelled = True
    order.save()
    orders = Orders.objects.filter(user=request.user)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("wethestockedpantry@gmail.com", "Thestockedpantry@1234")
    msg = EmailMessage()
    subject = "The Stocked Pantry:Order Cancelled"
    message = "Dear " + str(request.user) + ", Your Order For the following Products is cancelled: "
    message = message + "\n"
    message = message + "Order:"
    message = message + "\n"
    message = message + f"Product : {order.product_name}\tQuantity: {order.quantity}\tPrice: {order.price}\n"
    message = message + '\n'
    message = message + "Total Price: " + str(order.price)
    message = message + "\n"
    message = message + " Thank you for using Thestockedpantry.\n"
    msg.set_content(message)
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = "wethestockedpantry@gmail.com"
    msg['To'] = request.user.email
    s.send_message(msg)
    s.quit()
    sum = 0
    for order in orders:
        if order.product_name == 'default':
            order.price = sum
            sum = 0
        else:
            if not order.iscancelled:
                sum = sum + order.price
    return render(request, 'users/history.html', {'orders': orders})
"""