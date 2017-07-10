from __future__ import unicode_literals

import datetime
import sched
import time

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic import View, CreateView, UpdateView
from .forms import UserRegForm, BidForm
from .models import category, product

# s = sched.scheduler(time.time, time.sleep)


# def AuctionCheck(sc, pk):
#    print 1222222
#    user = product.objects.get(pk=pk)
#    start = user.start
#    x = datetime.timedelta(minutes=30)
#    end = (datetime.datetime.combine(datetime.date.today(), start) + x).time()
#    time_now = datetime.datetime.now()
#    t = time_now.time().replace(microsecond=0)
#    if t > end:
#        print 111111
#
#        #   user.status = True
#        #   user.save()
#    s.enter(60, 1, AuctionCheck, (sc,))
#

# s.enter(60, 1, AuctionCheck, (s,))
# s.run()
# print 123


class CategoryView(generic.DetailView):
    model = category
    template_name = 'auction/category.html'


class HomeView(generic.ListView):
    template_name = 'auction/home.html'
    context_object_name = 'all_categories'

    def get_queryset(self):
        return category.objects.all()


class ProductDetail(generic.DetailView):
    model = product
    template_name = 'auction/product.html'


class UserReg(View):
    form_class = UserRegForm
    template_name = 'auction/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('auction:home')

        return render(request, self.template_name, {'form': form})


class ProductReg(CreateView):
    model = product
    fields = ['product_name', 'p_category', 'price', 'start', 'image']


class BidView(UpdateView):
    form_class = BidForm
    model = product
    # fields = ['price']
    template_name = 'auction/bid_page.html'

    def post(self, request, pk):
        user = product.objects.get(pk=pk)
        bid = float(request.POST['price'])
        # do backend authentication, verify time difference here
        start = user.start
        x = datetime.timedelta(minutes=30)
        end = (datetime.datetime.combine(datetime.date.today(), start) + x).time()
        time_now = datetime.datetime.now()
        t = time_now.time().replace(microsecond=0)
        print time_now
        print start
        if t >= start and t <= end:
            if bid > user.price:
                user.highest = request.user.username
                user.price = bid
                user.save()

        return redirect(reverse('auction:product-detail', kwargs={'pk': pk}))
