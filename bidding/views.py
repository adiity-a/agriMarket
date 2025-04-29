from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from bidding.models import Bid
from products.models import Product

@require_POST
@login_required
def place_bid(request, product_id):
    if not request.user.is_buyer():
        return redirect("home")

    product = Product.objects.get(id=product_id)
    offered_price = float(request.POST.get("offered_price"))
    quantity = int(request.POST.get("quantity"))

    Bid.objects.create(
        buyer=request.user,
        product=product,
        offered_price=offered_price,
        quantity=quantity
    )

    messages.success(request, "Bid placed successfully!")
    return redirect("buyer")

def auto_select_expired_bids():
    ten_days_ago = timezone.now() - timedelta(days=10)
    pending_bids = Bid.objects.filter(is_selected=False, timestamp__lte=ten_days_ago)

    # Group by product and approve the first oldest pending bid for each
    processed_products = set()

    for bid in pending_bids.order_by('timestamp'):
        if bid.product_id not in processed_products:
            bid.is_selected = True
            bid.save()
            processed_products.add(bid.product_id)

@login_required
def my_bids(request):
    if not request.user.is_buyer():
        return redirect('home')

    all_bids = Bid.objects.filter(buyer=request.user).select_related('product')
    active_bids = all_bids.filter(status='pending')
    past_bids = all_bids.filter(status__in=['approved', 'rejected'])

    return render(request, 'my_bids.html', {
        'active_bids': active_bids,
        'past_bids': past_bids,
    })

def edit_bid(request, bidId):
    return HttpResponse("editing bid")

@require_POST
@login_required
def edit_bid(request):
    bid_id = request.POST.get("bid_id")
    bid = get_object_or_404(Bid, id=bid_id, buyer=request.user)

    new_price = float(request.POST.get("price"))
    new_quantity = int(request.POST.get("quantity"))

    bid.offered_price = new_price
    bid.quantity = new_quantity
    bid.save()

    messages.success(request, "Bid updated successfully.")
    return redirect('my_bids')


@require_POST
@login_required
def remove_bid(request):
    bid_id = request.POST.get("bid_id")
    bid = get_object_or_404(Bid, id=bid_id, buyer=request.user)
    bid.delete()

    messages.success(request, "Bid removed successfully.")
    return redirect('my_bids')