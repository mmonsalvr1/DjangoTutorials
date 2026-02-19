from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView

from .models import Product


# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "About us - Online Store",
                "subtitle": "About us",
                "description": "This is an about page ...",
                "author": "Developed by: Matias Monsalve Ruiz",
            }
        )
        return context


class ContactPageView(TemplateView):
    template_name = "contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Contact us - Online Store",
                "subtitle": "Contact us",
                "description": "This is a contact page ...",
                "address": "Address: Calle 123 #45-67, Medellin, Colombia. ",
                "phone": "Phone: +57 123 456 7890. ",
                "email": "Email: contact@onlinestore.com",
            }
        )
        return context


class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        try:
            product_id = int(id)
            index = int(id) - 1
            if index < 0 or index >= len(Product.objects.all()):
                return HttpResponseRedirect(reverse("home"))
        except ValueError:
            return HttpResponseRedirect(reverse("home"))
        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = (
        "products"  # This will allow you to loop through 'products' in your template
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products - Online Store"
        context["subtitle"] = "List of products"
        return context


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]

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
            form.save()
            return redirect("confirmation")
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)


class ProductConfirmationView(TemplateView):
    template_name = "products/confirmation.html"
