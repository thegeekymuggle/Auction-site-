from __future__ import unicode_literals

from django.http.response import HttpResponseRedirect

from django.http import HttpResponse, request
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import View, CreateView, UpdateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import UserRegForm, BidForm
from .models import category, product


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


        # def get(self, request, pk):
        #  form = self.form_class(None)
        # return render(request, self.template_name, {'form': form, 'pk': pk})

        # def post(self, request, pk):
        #  form = self.form_class(request.POST)

        # if form.is_valid:
        # user = form.save(commit=False)
        #    bid = request.POST['price']
        #   user = product.objects.get(pk=pk)
        #  if bid > user.price:
        #     user.price = float(bid)
        #    user.highest = request.user.username
        #   user.save()
        # return redirect(reverse('auction:product-detail', kwargs={'pk': pk}))


class BidView(UpdateView):
    form_class = BidForm
    model = product
    # fields = ['price']
    template_name = 'auction/bid_page.html'

    def post(self, request, pk):
        user = product.objects.get(pk=pk)
        bid = request.POST['price']
        print user.price
        print bid
        print bool(bid > user.price)
        if bid > user.price:
            user.highest = request.user.username
            user.price = bid
            user.save()
        return redirect(reverse('auction:product-detail', kwargs={'pk': pk}))
