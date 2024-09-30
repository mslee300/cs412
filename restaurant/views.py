from django.shortcuts import render
import random
import time
from datetime import datetime, timedelta
from django.utils import timezone

def main(request):
    return render(request, 'restaurant/main.html')


def order(request):
    daily_specials = ['Pizza with thermonuclear sauce', 'Super Spicy Burger', 'Extra Cheese Pasta', 'Salad with Avocado']
    daily_special = random.choice(daily_specials)  # Randomly select the daily special
    context = {'daily_special': daily_special}
    return render(request, 'restaurant/order.html', context)


def confirmation(request):
    if request.method == 'POST':
        # Collect form data
        items = request.POST.getlist('items')  # This gets the selected item indices
        customer_name = request.POST['name']
        customer_email = request.POST['email']
        customer_phone = request.POST['phone']
        special_instructions = request.POST['instructions']

        # Random time between 30 and 60 minutes from now in Boston time zone
        ready_time = timezone.now() + timedelta(minutes=random.randint(30, 60))

        # Define menu items and prices
        item_names = ['Pizza', 'Burger', 'Pasta', 'Salad', request.POST.get('daily_special', 'Special Item')]  # Include special item
        item_prices = [10, 8, 7, 6, 5]  # Corresponding prices

        # Initialize selected_items to avoid index errors
        selected_items = []
        for i in items:
            try:
                index = int(i)  # Convert to integer
                # Ensure the index is within the valid range
                if 0 <= index < len(item_names):
                    selected_items.append((item_names[index], item_prices[index]))
            except (ValueError, IndexError):
                # Handle invalid input (e.g., non-integer or out-of-range index)
                continue

        # Total price calculation
        total_price = sum([price for item, price in selected_items])

        context = {
            'items': selected_items,  # Pass selected items with names and prices
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'special_instructions': special_instructions,
            'total_price': total_price,
            'ready_time': ready_time.strftime("%H:%M %p"),  # Format time in 12-hour format with AM/PM
        }
        return render(request, 'restaurant/confirmation.html', context)