from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from warehouse.models import Storage, Product
from .models import Sale
from .print_functions import export_products_to_excel, export_products_to_pdf
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class SaleView(View):
    template_name = "sale.html"
    
    def get_context_data(self, *args, **kwargs):
        context = {}
        context["sale"] =  Sale.objects.all()
        context["products"] = Product.objects.filter(storage__slug="tayyor-mahsulot")
        return context
    
    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request):
        context = self.get_context_data()
        if "filtr" in request.POST:
            start_date  = request.POST.get("from")
            end_date  = request.POST.get("till")
            if start_date and end_date:
                context["sale"] = Sale.objects.filter(date_added__range=(start_date, end_date))
            else:
                pass
            
        if "add" in request.POST:
            product = Product.objects.get(id= request.POST.get("product"))
            product_base_amount = product.amount - int(request.POST.get("amount"))
            if product_base_amount >= 0:
                sale = Sale.objects.create(
                    name = request.POST.get("name"),
                    product_name = product,
                    product_amount = request.POST.get("amount"),
                    payment_type = request.POST.get("payment_type"),
                    deadline = request.POST.get("deadline")
                )
                product.amount = product_base_amount
                product.save()
            else:
                messages.error(request, 'Bu nomdagi mahsulot Omborda Yetarli emas')
                return redirect("sale:sale_view")
            
        if "search" in request.POST:
            try:
                sale = Sale.objects.filter(name__icontains=request.POST.get("query"))
                context["sale"] = sale
            except Sale.DoesNotExist:
                return redirect("sale:sale_view")
            
        if "delete" in request.POST:
            try:
                sale = Sale.objects.get(id=request.POST.get("sale"))
                sale.delete()
            except Sale.DoesNotExist:
                pass
            
        if "action_edit" in request.POST:
            sale = Sale.objects.get(id=request.POST.get("sale"))
            context["edit_sale"] = sale
            return JsonResponse({'success': True, 'sale': {
                    'id': sale.id,
                    'name': sale.name,
                    'product_name': sale.product_name.id,
                    'product_amount': sale.product_amount,
                    'payment_type': sale.payment_type,
                    "deadline": sale.deadline
                }})
        
        
        if "save" in request.POST:
            sale = Sale.objects.get(id = request.POST.get("sale"))
            sale.name = request.POST.get("name")
            sale.product_name = Product.objects.get(id=request.POST.get("product"))
            sale.product_amount = request.POST.get("amount")
            sale.payment_type = request.POST.get("payment_type")
            sale.deadline = request.POST.get("deadline")
            sale.save()
        
        if 'excel' in request.POST:
            return export_products_to_excel(context["sale"])
        if "pdf" in request.POST:
            return export_products_to_pdf(context["sale"])
        
        return render(request, self.template_name, context)
    
