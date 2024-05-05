from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from openpyxl import Workbook


# Decorators
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Expances

def export_products_to_excel(products):
    # Create a new workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Kirimlar"

    # Define headers
    headers = ["Ismi", "Summasi", "Muddati", "To'lov turi", "Telefon Raqamlari"]
    ws.append(headers)

    # Write product data to the worksheet
    for product in products:
        ws.append([product.name, str(product.amount) + " " +str(product.currency), product.deadline, product.payment_type, str(product.phone_number) + "\n" + str(product.extra_phone_number)])

    # Create a response with Excel content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Set the content-disposition header to force download the file
    response['Content-Disposition'] = 'attachment; filename=kirim.xlsx'

    # Save the workbook content to the response
    wb.save(response)
    print("ishladi")
    return response


def export_products_to_pdf(products):
    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')

    # Set the content-disposition header to force download the file
    response['Content-Disposition'] = 'attachment; filename=kirim.pdf'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Define table data (products)
    data = [["Ismi", "Summasi", "Muddati", "To'lov turi", "Telefon Raqamlari"]]
    for product in products:
        data.append([product.name, str(product.amount) + " " + str(product.currency), product.deadline, product.payment_type, str(product.phone_number) + "\n" + str(product.extra_phone_number)])

    # Create a table from the data
    table = Table(data)

    # Add style to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Add the table to the PDF document
    pdf.build([table])

    return response


@method_decorator(login_required, name='dispatch')
class ExpancesView(View):
    template_name = "expances.html"
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context = {}
        context["expances"] = Expances.objects.all()
        return context
    
    
    def get(self, request):
        context = self.get_context_data()
        paginator = Paginator(context["expances"], self.paginate_by)
        page_number = request.GET.get('page')
        try:
            expances = paginator.page(page_number)
        except PageNotAnInteger:
            expances = paginator.page(1)
        except EmptyPage:
            expances = paginator.page(paginator.num_pages)
        context['expances'] = expances
        return render(request, self.template_name, context)
    

    def post(self, request):
        context = self.get_context_data()
        
        if "filtr" in request.POST:
            start_date  = request.POST.get("from")
            end_date  = request.POST.get("till")
            if start_date and end_date:
                context["expances"] = Expances.objects.filter(deadline__range=(start_date, end_date))
            else:
                pass
        
        
        if "add" in request.POST:
            expance = Expances.objects.create(
                name = request.POST.get("name"),
                amount = request.POST.get("amount"),
                currency = request.POST.get("currency"),
                payment_type = request.POST.get("payment_type"),
                deadline = request.POST.get("deadline"),
                phone_number = request.POST.get("phone_number"),
                extra_phone_number = request.POST.get("extra_phone_number")
            )
        
        if "action" in request.POST:
            product = Expances.objects.get(id=request.POST.get("product"))
            context["edit_product"] = product
            return JsonResponse({'success': True, 'expance': {
                    'id': product.id,
                    'name': product.name,
                    'amount': product.amount,
                    'currency': product.currency,
                    'payment_type': product.payment_type,
                    'deadline': product.deadline,
                    'phone_number': product.phone_number,
                    'extra_phone_number': product.extra_phone_number,
                }})
        if "delete" in request.POST:
            try:
                product = Expances.objects.get(id=request.POST.get("product"))
                product.delete()
            except Expances.DoesNotExist:
                return redirect("expances_app:expances_view")
        # Editing
        if "save" in request.POST:
            product_id = request.POST.get("product")
            print(product_id)
            product = get_object_or_404(Expances, id=product_id)
            product.name = request.POST.get("name")
            product.amount = request.POST.get("amount")
            product.currency = request.POST.get("currency")
            product.payment_type = request.POST.get("payment_type")
            product.deadline = request.POST.get("deadline")
            product.phone_number = request.POST.get("phone_number")
            product.extra_phone_number = request.POST.get("extra_phone_number")
            product.save()
            return redirect("expances_app:expances_view")
         # Exporting
        if 'excel' in request.POST:
            return export_products_to_excel(context["expances"])
        if "pdf" in request.POST:
            return export_products_to_pdf(context["expances"])
        
        if "search" in request.POST:
            try:
                product = Expances.objects.filter(name__icontains=request.POST.get("query"))
                context["expances"] = product
            except Expances.DoesNotExist:
                return redirect("expances_app:expances_view")
            
        return render(request, self.template_name, context)
    
    
@method_decorator(login_required, name='dispatch')
class DebtsView(View):
    template_name = "debts.html"
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        context = {}
        context["expances"] = Expances.objects.filter(payment_type='nasiya').filter(amount__gt=0)
        return context
    
    
    def get(self, request):
        context = self.get_context_data()
        paginator = Paginator(context["expances"], self.paginate_by)
        page_number = request.GET.get('page')
        try:
            expances = paginator.page(page_number)
        except PageNotAnInteger:
            expances = paginator.page(1)
        except EmptyPage:
            expances = paginator.page(paginator.num_pages)
        context['expances'] = expances
        return render(request, self.template_name, context)
    

    def post(self, request):
        context = self.get_context_data()
        
        if "filtr" in request.POST:
            start_date  = request.POST.get("from")
            end_date  = request.POST.get("till")
            if start_date and end_date:
                context["expances"] = Expances.objects.filter(deadline__range=(start_date, end_date))
            else:
                pass
            
        
        if "action" in request.POST:
            product = Expances.objects.get(id=request.POST.get("product"))
            context["edit_product"] = product
            return JsonResponse({'success': True, 'expance': {
                    'id': product.id,
                    'name': product.name,
                    'amount': product.amount,
                    'currency': product.currency,
                    'payment_type': product.payment_type,
                    'deadline': product.deadline,
                    'phone_number': product.phone_number,
                    'extra_phone_number': product.extra_phone_number,
                }})
            
            
        if "delete" in request.POST:
            try:
                product = Expances.objects.get(id=request.POST.get("product"))
                product.delete()
            except Expances.DoesNotExist:
                return redirect("expances_app:expances_view")
            
            
        # Editing
        if "save" in request.POST:
            product_id = request.POST.get("product")
            print(product_id)
            product = get_object_or_404(Expances, id=product_id)
            product.name = request.POST.get("name")
            product.amount -= int(request.POST.get("amount"))
            product.currency = request.POST.get("currency")
            product.deadline = request.POST.get("deadline")
            product.save()
            return redirect("expances_app:debts_view")
         # Exporting
         
        if 'excel' in request.POST:
            return export_products_to_excel(context["expances"])
        if "pdf" in request.POST:
            return export_products_to_pdf(context["expances"])
        
        if "search" in request.POST:
            try:
                product = Expances.objects.filter(name__icontains=request.POST.get("query"))
                context["expances"] = product
            except Expances.DoesNotExist:
                return redirect("expances_app:expances_view")
            
        return render(request, self.template_name, context)