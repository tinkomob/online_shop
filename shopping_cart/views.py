from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect


from accounts.models import Profile
from shop.models import Product
from shopping_cart.extras import generate_order_id, generate_client_token
from shopping_cart.models import OrderItem, Order, Transaction


import datetime



def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()

    # check if the user already owns this product
    # if product in request.user.profile.ebooks.all():
    #     messages.info(request, 'You already own this ebook')
    #     return redirect(reverse('shop:home')) 
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product, user = user_profile)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    # order_products = [item.product for item in order_items]
    user_profile.ebooks.add(product)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "товар  " + product.title + " добавлен в корзину")
    return HttpResponseRedirect('/')


@login_required()
def delete_from_cart(request, item_id):
    user_profile = get_object_or_404(Profile, user=request.user)
    item_to_delete = OrderItem.objects.get(pk=item_id)
    product = Product.objects.get(id=item_to_delete.product.id)
    user_profile.ebooks.remove(product)
    item_to_delete.delete()
    messages.info(request, "товар был удалён")
    return redirect(reverse('shopping_cart:order_summary'))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'shopping_cart/order_summary.html', context)

@login_required()
def inc_orderItem(request, item_id):
    item = OrderItem.objects.get(id=item_id)
    item.quantity += 1
    item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required()
def decr_orderItem(request, item_id):
    item = OrderItem.objects.get(id=item_id)
    item.quantity -= 1
    if item.quantity < 1:
        item.quantity = 1
    item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required()
def checkout(request, **kwargs):
    existing_order = get_user_pending_order(request) 
    user_profile = get_object_or_404(Profile, user=request.user)
    client_token = generate_client_token()
    context = {
        'order': existing_order,
        'client_token': client_token,
        'user_profile': user_profile,
    }

    return render(request, 'shopping_cart/checkout.html', context)


@login_required()
def update_transaction_records(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    
    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # get the products from the items
    # user_profile.ebooks.add(*order_products)
    user_profile.ebooks.clear()
    user_profile.save()

    
    # create a transaction
    transaction = Transaction(profile=request.user.profile,
                            token=token,
                            order_id=order_to_purchase.id,
                            amount=order_to_purchase.get_cart_total(),
                            success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()


    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Спасибо! Покупка успешно совершена!")
    return redirect(reverse('accounts:my_profile'))


def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'shopping_cart/purchase_success.html', {})