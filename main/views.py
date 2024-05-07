from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse

from django.contrib import messages
from .print_functions import export_products_to_excel,export_products_to_pdf, export_products_to_excel_debts, export_products_to_pdf_debts


from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Expance
from sale.models import Sale, Product
from django.contrib.auth.models import User



@method_decorator(login_required, name='dispatch')
class MainView(View):
    template_name = "index.html"
    
    def get_context_data(self, *args, **kwargs):
        context = {}
        context["debt_sales"] = Sale.objects.filter(payment_type='nasiya')
        return context
    
    
    def get(self, request):
        context = self.get_context_data()
        sales = Sale.objects.all()
        sales_data = {}
        for sale in sales:
            month = sale.date_added.strftime("%B")  
            if month in sales_data:
                sales_data[month] += sale.get_overall()  
            else:
                sales_data[month] = sale.get_overall()
        if "action_edit" in request.GET:
            print(request, sales_data)
            return JsonResponse(sales_data)
        else:
            return render(request, self.template_name, context)
    
    
    def post(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ExpanceView(View):
    template_name = "expances.html"
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context = {}
        context["expance"] = Expance.objects.all()
        return context
    
    
    def get(self, request):
        context = self.get_context_data()
        paginator = Paginator(context["expance"], self.paginate_by)
        page_number = request.GET.get('page')
        try:
            expance = paginator.page(page_number)
        except PageNotAnInteger:
            expance = paginator.page(1)
        except EmptyPage:
            expance = paginator.page(paginator.num_pages)
        context['expance'] = expance
        return render(request, self.template_name, context)
    
    
    def post(self, request):
        context = self.get_context_data()
        
        if "filtr" in request.POST:
            start_date  = request.POST.get("from")
            end_date  = request.POST.get("till")
            if start_date and end_date:
                context["expance"] = Expance.objects.filter(date_added__range=(start_date, end_date))
            else:
                pass
            
        
        if "add" in request.POST:
            expance = Expance.objects.create(
                name = request.POST.get("name"),
                amount = request.POST.get("amount"),
                currency = request.POST.get("currency")
            )
            
            
        if "action_edit" in request.POST:
            expance = Expance.objects.get(id=request.POST.get("expance"))
            context["edit_expance"] = expance
            return JsonResponse({'success': True, 'expance': {
                    'id': expance.id,
                    'name': expance.name,
                    'amount': expance.amount,
                    'currency': expance.currency,
                }})
        
        
        if "save" in request.POST:
            expance = Expance.objects.get(id = request.POST.get("expance"))
            expance.name = request.POST.get("name")
            expance.amount = request.POST.get("amount")
            expance.currency = request.POST.get("currency")
            expance.save()
        
        
        if "delete" in request.POST:
            try:
                expance = Expance.objects.get(id=request.POST.get("expance"))
                expance.delete()
            except Expance.DoesNotExist:
                return redirect("main_app:expance")
            
            
        if 'excel' in request.POST:
            return export_products_to_excel(context["expance"])
        if "pdf" in request.POST:
            return export_products_to_pdf(context["expance"])
        
        if "search" in request.POST:
            try:
                expance = Expance.objects.filter(name__icontains=request.POST.get("query"))
                context["expance"] = expance
            except Expance.DoesNotExist:
                return redirect("main_app:expance")
            
        return render(request, self.template_name, context)
    
    
@method_decorator(login_required, name='dispatch')
class DebtsView(View):
    template_name = "debts.html"
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context = {}
        context["products"] = Product.objects.all()
        context["debts"] = Sale.objects.filter(payment_type='nasiya')
        return context
    
    
    def get(self, request):
        context = self.get_context_data()
        paginator = Paginator(context["debts"], self.paginate_by)
        page_number = request.GET.get('page')
        try:
            debts = paginator.page(page_number)
        except PageNotAnInteger:
            debts = paginator.page(1)
        except EmptyPage:
            debts = paginator.page(paginator.num_pages)
        context['debts'] = debts
        return render(request, self.template_name, context)
    
    
    def post(self, request):
        context = self.get_context_data()
        
        if "filtr" in request.POST:
            start_date  = request.POST.get("from")
            end_date  = request.POST.get("till")
            if start_date and end_date:
                context["debts"] = Sale.objects.filter(date_added__range=(start_date, end_date), payment_type='nasiya')
            else:
                pass
            
        
        # if "add" in request.POST:
        #     expance = Sale.objects.create(
        #         name = request.POST.get("name"),
        #         amount = request.POST.get("amount"),
        #         currency = request.POST.get("currency")
        #     )
            
            
        if "search" in request.POST:
            try:
                debts = Sale.objects.filter(name__icontains=request.POST.get("query")).filter(payment_type='nasiya')
                context["debts"] = debts
            except Sale.DoesNotExist:
                return redirect("main_app:debts")
            
        if "delete" in request.POST:
            try:
                debts = Sale.objects.get(id=request.POST.get("debts"))
                debts.delete()
            except Sale.DoesNotExist:
                pass
            
        if "action_edit" in request.POST:
            debts = Sale.objects.get(id=request.POST.get("debts"))
            context["edit_debts"] = debts
            return JsonResponse({'success': True, 'debts': {
                    'id': debts.id,
                    'name': debts.name,
                    'product_name': debts.product_name.id,
                    'product_amount': debts.product_amount,
                    'status': debts.status,
                    "deadline": debts.deadline
                }})
        
        
        if "save" in request.POST:
            debts = Sale.objects.get(id = request.POST.get("debts"))
            debts.name = request.POST.get("name")
            debts.product_name = Product.objects.get(id=request.POST.get("product"))
            debts.product_amount = request.POST.get("amount")
            debts.status = request.POST.get("status")
            debts.deadline = request.POST.get("deadline")
            debts.save()
        
        if 'excel' in request.POST:
            return export_products_to_excel_debts(context["debts"])
        if "pdf" in request.POST:
            return export_products_to_pdf_debts(context["debts"])
            
        return render(request, self.template_name, context)
    
    
    
class LoginView(View):
    template_name = "register/pages-login.html"
    
    def get_context_data(self, *args, **kwargs):
        context = {}
        return context
    
    
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
    
    
    def post(self, request):
        context = {}
        if "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("main_app:main")
            else:
                context["error"] = "Parol Yoki Foydalanuvchi nomi Xato!"
                return render(request, self.template_name, context)
        return render(request, self.template_name, context)