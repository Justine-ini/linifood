from django.http import HttpResponse, JsonResponse
import simplejson as json
from django.shortcuts import redirect, render

from marketplace.context_processors import get_cart_amounts
from marketplace.models import Cart
from orders.forms import OrderForm
from orders.models import Order, OrderedFood, Payment
from .utils import generate_order_number
from django.contrib.auth.decorators import login_required

def place_order(request):
  cart_items = Cart.objects.filter(user=request.user).order_by("created_at")
  cart_count = cart_items.count()
  if cart_count <= 0:
    return redirect("marketplace")
  
  subtotal = get_cart_amounts(request)["subtotal"]
  total_tax = get_cart_amounts(request)["tax"]
  grand_total = get_cart_amounts(request)["grand_total"]
  tax_data = get_cart_amounts(request)["tax_dict"]
  
  if request.method == "POST":
    form = OrderForm(request.POST)
    if form.is_valid():
      order = Order()
      order.first_name = form.cleaned_data["first_name"]
      order.last_name = form.cleaned_data["last_name"]
      order.phone = form.cleaned_data["phone"]
      order.email = form.cleaned_data["email"]
      order.address = form.cleaned_data["address"]
      order.country = form.cleaned_data["country"]
      order.state = form.cleaned_data["state"]
      order.city = form.cleaned_data["city"]
      order.pin_code = form.cleaned_data["pin_code"]
      order.feedbacks = form.cleaned_data["feedbacks"]
      order.total = grand_total
      order.tax_data = json.dumps(tax_data)
      order.user = request.user
      order.total_tax = total_tax
      order.payment_method = request.POST["payment_method"]
      order.save() # order id or pk is generated
      order.order_number = generate_order_number(order.id)
      order.save()
      context = {
        "order": order,
        "cart_items": cart_items, #verify error
        
      }
      return render(request, "orders/place_order.html", context)
    else:
      print(form.errors)
  return render(request, "orders/place_order.html")


@login_required(login_url='login')
def payments(request):
        # Check if the request is ajax or not
    if request.method == 'POST':
        # STORE THE PAYMENT DETAILS IN THE PAYMENT MODEL
        order_number = request.POST.get('order_number')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get("status")
        feedbacks = request.POST.get('feedbacks')
        print(feedbacks)

        order = Order.objects.get(user=request.user, order_number=order_number, feedbacks=feedbacks)
        payment = Payment(
            user = request.user,
            payment_method = payment_method,
            amount = order.total,
            status = status,
            
        )
        payment.save()

        # UPDATE THE ORDER MODEL
        order.payment = payment
        order.is_ordered = True
        feedbacks = "Success"
        order.save()

        # MOVE THE CART ITEMS TO ORDERED FOOD MODEL
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity # total amount
            ordered_food.save()

        # CLEAR THE CART IF THE PAYMENT IS SUCCESS
        cart_items.delete() 

        # RETURN BACK TO AJAX WITH THE STATUS SUCCESS OR FAILURE
        response = {
            'order_number': order_number,
            'status': status,
            "feedbacks": feedbacks
        }
        return JsonResponse(response)
    # return HttpResponse('Payments view')
    return render(request, 'customers/my_orders.html')

def order_complete(request):
  order_number = request.GET.get("order_number")
  order = Order.objects.get(order_number=order_number, is_ordered = True)
  ordered_food = OrderedFood.objects.filter(order=order)

  context = {
      "order":order,
      "order_number": order_number,
      "ordered_food": ordered_food
  }
  return render(request, 'orders/order_complete.html', context)







