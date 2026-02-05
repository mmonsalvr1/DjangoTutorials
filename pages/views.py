from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.shortcuts import render, redirect

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

class AboutPageView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Matias Monsalve Ruiz",
        })
        return context

class ContactPageView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "subtitle": "Contact us",
            "description": "This is a contact page ...",
            "address": "Address: Calle 123 #45-67, Medellin, Colombia. ",
            "phone": "Phone: +57 123 456 7890. ",
            "email": "Email: contact@onlinestore.com"
        })
        return context

class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price":1000},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price":1200},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price":50},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price":200}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'
    def get(self, request, id):
        try:
            index = int(id)-1
            if index < 0 or index >= len(Product.products):
                return HttpResponseRedirect(reverse('home')) 
        except ValueError:
            return HttpResponseRedirect(reverse('home'))
        viewData = {}
        product = Product.products[int(id)-1]
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)


class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class ProductCreateView(View):
    template_name = "products/create.html"
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            return redirect("confirmation")
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

class ProductConfirmationView(TemplateView):
    template_name = "products/confirmation.html"
    
