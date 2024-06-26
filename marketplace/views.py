from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from orders.forms import OrderForm
from .context_processors import get_cart_amounts, get_cart_counter
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import Cart
from django.contrib.auth.decorators import login_required


def marketplace(request):
  vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
  vendor_count = vendors.count()

  context = {
    "vendors": vendors,
    "vendor_count": vendor_count,
  }
  return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
  vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

  categories = Category.objects.filter(vendor=vendor).prefetch_related(
    Prefetch(
      "fooditems",
      queryset = FoodItem.objects.filter(is_available=True)
    )
  )
  # fooditems = FoodItem.objects.filter(vendor=vendor)
  if request.user.is_authenticated:
    cart_items = Cart.objects.filter(user=request.user)
  else:
    cart_items=None
  context = {
    "vendor": vendor,
    "categories":categories,
    "cart_items": cart_items,
  }
  return render(request, "marketplace/vendor_detail.html", context)

def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
  


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        # decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
    

@login_required(login_url="login")
def cart(request):
   cart_items = Cart.objects.filter(user=request.user).order_by("created_at")
   context = {
      "cart_items": cart_items
   }
   return render(request, "marketplace/cart.html", context)

def delete_cart(request, cart_id):
   if request.user.is_authenticated:
      if request.headers.get('x-requested-with') == 'XMLHttpRequest':
         try:
            # Check if cart item exist
            cart_item = Cart.objects.get(user=request.user, id=cart_id)
            if cart_item:
               cart_item.delete()
               return JsonResponse({'status': 'success', 'message': 'Cart item has been deleted!', "cart_counter": get_cart_counter(request), "cart_counter": get_cart_amounts(request)})   
         except:
            return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist!'})
      else:
         return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
      

def checkout(request):
   form = OrderForm()
   context = {
      "form":form
   }
   return render(request, 'marketplace/checkout.html', context)


def search(request):
   pass
#   if not 'address' in request.GET:
#       return redirect('marketplace')
#   else:
#       address = request.GET['address']
#       latitude = request.GET['lat']
#       longitude = request.GET['lng']
#       radius = request.GET['radius']
#       keyword = request.GET['keyword']

#       # get vendor ids that has the food item the user is looking for
#       fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
      
#       vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
#       if latitude and longitude and radius:
#           pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))

#           vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True),
#           user_profile__location__distance_lte=(pnt, D(km=radius))
#           ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

#           for v in vendors:
#               v.kms = round(v.distance.km, 1)
#       vendor_count = vendors.count()
#       context = {
#           'vendors': vendors,
#           'vendor_count': vendor_count,
#           'source_location': address,
#       }


#       return render(request, 'marketplace/listings.html', context)