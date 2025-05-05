from django.shortcuts import render

def home(request):
    return render(request, 'landing/home.html')

def about(request):
    return render(request, 'landing/about.html')

def reviews(request):
    return render(request, 'landing/reviews.html')