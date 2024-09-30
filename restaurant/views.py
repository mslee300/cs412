from django.shortcuts import render
import random
import time
from datetime import datetime, timedelta
from django.utils import timezone

def main(request):
    return render(request, 'restaurant/main.html')


def order(request):
    daily_specials = ['Pizza with thermonuclear sauce', 'Super Spicy Burger', 'Extra Cheese Pasta', 'Salad with Avocado']
    daily_special = random.choice(daily_specials)
    context = {'daily_special': daily_special}
    return render(request, 'restaurant/order.html', context)


def confirmation(request):
    if request.method == 'POST':

        items = request.POST.getlist('items')
        customer_name = request.POST['name']
        customer_email = request.POST['email']
        customer_phone = request.POST['phone']
        special_instructions = request.POST['instructions']

        ready_time = timezone.now() + timedelta(minutes=random.randint(30, 60))

        item_names = ['Pizza', 'Burger', 'Pasta', 'Salad', request.POST.get('daily_special', 'Special Item')]  # Include special item
        item_prices = [10, 8, 7, 6, 5]

        selected_items = []
        for i in items:
            try:
                index = int(i)

                if 0 <= index < len(item_names):
                    selected_items.append((item_names[index], item_prices[index]))
            except (ValueError, IndexError):
                continue

        total_price = sum([price for item, price in selected_items])

        context = {
            'items': selected_items,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'special_instructions': special_instructions,
            'total_price': total_price,
            'ready_time': ready_time.strftime("%H:%M %p"),
        }
        return render(request, 'restaurant/confirmation.html', context)