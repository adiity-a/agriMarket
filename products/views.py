from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseForbidden
from agriMarket.forms import ProductForm
from django.contrib.auth.decorators import login_required
from products.models import Product
from bidding.models import Bid
from agriMarket.utils import reverse_geocode

# Create your views here.
@login_required
def add_product(request):
    success = False
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.lat = request.user.lat
            product.lng = request.user.lng
            product.save()
            success = True
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form, 'success': success})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if not (request.user == product.farmer or request.user.is_admin):
        return HttpResponseForbidden("You don't have permission to edit this product")
    
    success = False
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # form.save()
            # success = True
            product = form.save(commit=False)

            product.lat = form.cleaned_data.get('lat', product.lat)
            product.lng = form.cleaned_data.get('lng', product.lng)
            product.save()
            success = True
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {
        'form': form,
        'product': product,
        'request': request,
        'success': success 
    })

@user_passes_test(lambda u: u.is_authenticated and u.is_admin)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
    return redirect('admin')