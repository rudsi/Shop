from django.shortcuts import render, redirect
from .forms import ShopRegistrationForm, SearchShopsForm
from .utils import haversine
from .models import Shop

def register_shop(request):
    if request.method == 'POST':
        form = ShopRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop_success')
    else:
        form = ShopRegistrationForm()

    return render(request, 'shops/register_shop.html', {'form': form})

def shop_success(request):
    return render(request, 'shops/success.html')


def home(request):
    return render(request, 'shops/home.html')


def search_shops(request):
    form = SearchShopsForm() 
    
    if request.method == 'POST':
        form = SearchShopsForm(request.POST)  
        if form.is_valid():
            user_lat = form.cleaned_data.get('latitude')
            user_lon = form.cleaned_data.get('longitude')

            latitude_error = None
            longitude_error = None

            if user_lat is None or not (-90 <= user_lat <= 90):
                latitude_error = "Please provide a valid latitude between -90 and 90."

            if user_lon is None or not (-180 <= user_lon <= 180):
                longitude_error = "Please provide a valid longitude between -180 and 180."

            if latitude_error or longitude_error:
                return render(request, 'shops/search_shops.html', {
                    'form': form,
                    'latitude_error': latitude_error,
                    'longitude_error': longitude_error
                })

            if user_lat is None or user_lon is None:
                return render(request, 'shops/search_shops.html', {
                    'form': form,
                    'error': 'Please provide both latitude and longitude.'
                })

            shops = Shop.objects.all()
            shop_distances = []

            for shop in shops:
                distance = haversine(user_lat, user_lon, shop.latitude, shop.longitude)
                shop_distances.append({
                    'shop_name': shop.name,
                    'latitude': shop.latitude,
                    'longitude': shop.longitude,
                    'distance_km': distance
                })

            sorted_shops = sorted(shop_distances, key=lambda x: x['distance_km'])
            return render(request, 'shops/search_shops.html', {
                'form': form,
                'results': sorted_shops
            })

    
    return render(request, 'shops/search_shops.html', {'form': form})
