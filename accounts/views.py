from django.shortcuts import render, get_object_or_404,redirect

from shopping_cart.models import Order
from .models import Profile
from shop.models import Review
from django.urls import reverse_lazy
from django.contrib import messages

def my_profile(request):
	my_user_profile = Profile.objects.filter(user=request.user).first()
	if request.method == 'POST':
		tel = request.POST['tel']
		address = request.POST['address']
		my_user_profile.phone_number = tel
		my_user_profile.delivery_address = address
		my_user_profile.save()
		messages.info(request, "Данные успешно обновлены!")
		return redirect(reverse_lazy('accounts:my_profile'))
	my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
	my_reviews = Review.objects.filter(author__user__username = request.user.username)
	context = {
		'my_orders': my_orders,
		'my_reviews': my_reviews,
		'my_user_profile': my_user_profile,
	}
	return render(request, "profile.html", context)