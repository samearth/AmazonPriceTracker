from django.shortcuts import render,redirect
from .forms import AddLinkForm
from .models import Link
from django.views.generic import DeleteView
from django.urls import reverse_lazy
# Create your views here.

def home(request):
    no_of_discounted=0
    error=None

    form = AddLinkForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
        except AttributeError:
            error = "Can't get the name or price"
        except:
            error="Something went wrong"
    form  = AddLinkForm()
    products = Link.objects.all()
    total_items = products.count()
    if total_items>0:
        discount_list = []
        for item in products:
            if item.old_price > item.current_price:
                discount_list.append(item)
            no_of_discounted = len(discount_list)
    context = {
        'products':products,
        'total_items':total_items,
        'form':form,
        'dp':no_of_discounted,
        'error':error
    }
    return render(request , 'links/home.html' , context)
    

class LinkDeleteView(DeleteView):
    model = Link
    template_name = 'links/confirm_del.html'
    success_url = reverse_lazy('home')

def update_prices(request):
    products = Link.objects.all()
    for product in products:
        product.save()
    return redirect('home')