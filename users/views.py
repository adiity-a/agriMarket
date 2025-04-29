from products.models import Product
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from bidding.models import Bid  
from .models import User
from agriMarket.utils import reverse_geocode, haversine

# @login_required
# def buyer(request):
#     if not request.user.is_buyer():
#         return redirect("home")

#     buyer_lat = request.user.lat
#     buyer_lng = request.user.lng

#     products = Product.objects.all()

#     # Filters
#     search = request.GET.get("search", "")
#     min_price = request.GET.get("min_price")
#     max_price = request.GET.get("max_price")
#     sort = request.GET.get("sort")
#     radius = request.GET.get("radius")

#     if search:
#         products = products.filter(name__icontains=search)
#     if min_price:
#         products = products.filter(price__gte=min_price)
#     if max_price:
#         products = products.filter(price__lte=max_price)
#     if sort == "price_asc":
#         products = products.order_by("price")
#     elif sort == "price_desc":
#         products = products.order_by("-price")

#     product_data = []

#     for product in products:
#         distance = haversine(buyer_lat, buyer_lng, product.lat, product.lng)
#         if radius and distance > float(radius):
#             continue  # Skip products beyond the radius
        
#         bids = Bid.objects.filter(product=product, buyer=request.user)
#         product.location_name = reverse_geocode(product.lat, product.lng)
#         product_data.append({
#             'product': product,
#             'bids': bids,
#             # 'distance': round(distance, 2)
#         })

#     return render(request, 'buyer.html', {
#         'product_data': product_data
#     })

@login_required
def buyer(request):
    if not request.user.is_buyer():
        return redirect("home")

    # Get predicted price from session if it exists
    predicted_price = request.session.pop('predicted_price', None)
    prediction_details = request.session.pop('prediction_details', None)
    prediction_error = request.session.pop('prediction_error', None)

    buyer_lat = request.user.lat
    buyer_lng = request.user.lng

    products = Product.objects.all()

    # Existing filter logic...
    search = request.GET.get("search", "")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort")
    radius = request.GET.get("radius")

    if search:
        products = products.filter(name__icontains=search)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")

    product_data = []

    for product in products:
        distance = haversine(buyer_lat, buyer_lng, product.lat, product.lng)
        if radius and distance > float(radius):
            continue
        
        bids = Bid.objects.filter(product=product, buyer=request.user)
        product.location_name = reverse_geocode(product.lat, product.lng)
        product_data.append({
            'product': product,
            'bids': bids,
        })

    context = {
        'product_data': product_data,
        'predicted_price': predicted_price,
        'prediction_details': prediction_details,
        'prediction_error': prediction_error,
    }

    return render(request, 'buyer.html', context)

@login_required
def farmer(request):
    if not request.user.is_farmer():
        return redirect("home")
    
    products = Product.objects.filter(farmer=request.user)

    for product in products:
        product.bids = Bid.objects.filter(product=product)
        product.location_name = reverse_geocode(product.lat, product.lng)

    return render(request, 'farmer.html', {'products': products})

# Admin dashboard
@user_passes_test(lambda u: u.is_authenticated and u.is_admin())
def admin(request):
    total_users = User.objects.count()
    total_farmers = User.objects.filter(role='farmer').count()
    total_buyers = User.objects.filter(role='buyer').count()
    total_products = Product.objects.count()
    total_bids = Bid.objects.count()
    pending_bids = Bid.objects.filter(status='pending').count()

    context = {
        'total_users': total_users,
        'total_farmers': total_farmers,
        'total_buyers': total_buyers,
        'total_products': total_products,
        'total_bids': total_bids,
        'pending_bids': pending_bids,
    }
    return render(request, 'admin.html', context)

# Manage users (farmers and buyers)
@user_passes_test(lambda u: u.is_authenticated and u.is_admin())
def manage_users(request):
    farmers = User.objects.filter(role='farmer', is_superuser=False)
    buyers = User.objects.filter(role='buyer', is_superuser=False)
    return render(request, 'manage_users.html', {'farmers': farmers, 'buyers': buyers})

# Manage products
@user_passes_test(lambda u: u.is_authenticated and u.is_admin())
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'manage_products.html', {'products': products})

# Manage bids
@user_passes_test(lambda u: u.is_authenticated and u.is_admin())
def manage_bids(request):
    products = Product.objects.all()
    product_data = []

    for product in products:
        bids = Bid.objects.filter(product=product).order_by('-timestamp')
        product_data.append({
            'product': product,
            'bids': bids
        })

    if request.method == "POST":
        approve_bid_id = request.POST.get("approve_bid")
        reject_bid_id = request.POST.get("reject_bid")

        if approve_bid_id:
            # bid = get_object_or_404(Bid, id=approve_bid_id)
            # bid.status = 'approved'
            # bid.save()
            bid = get_object_or_404(Bid, id=approve_bid_id)
            product = bid.product  # Correctly fetch the product associated with the bid
            if product.quantity >= bid.quantity:
                product.quantity -= bid.quantity
                product.save()
            bid.status = 'approved'
            bid.save()
        elif reject_bid_id:
            bid = get_object_or_404(Bid, id=reject_bid_id)
            bid.status = 'rejected'
            bid.save()
            

    return render(request, 'manage_bids.html', {
        'product_data': product_data
    })

# Delete user
@user_passes_test(lambda u: u.is_authenticated and u.is_admin())
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
    return redirect('manage_users')

# Delete product
@user_passes_test(lambda u: u.is_authenticated and u.is_admin())
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
    return redirect('manage_products')