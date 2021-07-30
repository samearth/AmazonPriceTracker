from django.shortcuts import render,redirect
from .forms import AddLinkForm
from .models import Link
from django.views.generic import DeleteView
from django.urls import reverse_lazy
import schedule
from schedule import Scheduler
import time
import threading

_thread_locals = threading.local()

def get_current_request():
    print('hi')
    return getattr(_thread_locals, 'request', None)

class ThreadLocals(object):
    """
    Middleware that gets various objects from the
    request object and saves them in thread local storage.
    """
    def process_request(self, request):
        _thread_locals.request = request
    

class LinkDeleteView(DeleteView):
    model = Link
    template_name = 'links/confirm_del.html'
    success_url = reverse_lazy('home')


def update_prices(request):
    print('hi')
    products = Link.objects.all()
    for product in products:
        product.save()


def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously
# update_prices(get_current_request) # call foo
# schedule.every(5).seconds.do(
#         update_prices,get_current_request) 
def start_scheduler(request):
    scheduler = Scheduler()
    scheduler.every(10).seconds.do(update_prices , request)
    scheduler.run_continuously()

def home(request):
    no_of_discounted=0
    error=None
    form = AddLinkForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
            else :
                print('error')
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


# start_updates()