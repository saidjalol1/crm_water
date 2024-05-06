from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Product, Storage

# Decorators
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from openpyxl import Workbook

def export_products_to_excel(products):
    # Create a new workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Products"

    # Define headers
    headers = ["Nomi", "Miqdori","O'lchov birligi", "Sof Foyda", "Tan Narxi", "Sanasi"]
    ws.append(headers)

    # Write product data to the worksheet
    for product in products:
        ws.append([product.name, product.amount, product.measurement_unit, product.income, product.body_price, product.date_added])

    # Create a response with Excel content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Set the content-disposition header to force download the file
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'

    # Save the workbook content to the response
    wb.save(response)
    print("ishladi")
    return response


def export_products_to_pdf(products):
    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')

    # Set the content-disposition header to force download the file
    response['Content-Disposition'] = 'attachment; filename=products.pdf'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Define table data (products)
    data = [["Nomi", "Miqdori", "O'lchov birligi", "Sof foyda", "Tan Narxi", "sanasi"]]
    for product in products:
        data.append([product.name, product.amount, product.measurement_unit, product.income, product.body_price, product.date_added])

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
class StorageView(View):
    template_name = "storage.html"
    paginate_by = 10
    
    def get_context_data(self, *args, **kwargs):
        storage = Storage.objects.get(slug = self.kwargs.get("slug"))
        context = {
            "storage": storage,
            "items" : storage.items.all()
        }
        return context
    
    
    def get(self, request, *args , **kwargs):
        context = self.get_context_data()
         
        # Pagination
        paginator = Paginator(context["items"], self.paginate_by)
        page_number = request.GET.get('page')
        try:
            items = paginator.page(page_number)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
    
        context["items"] = items
        return render(request, self.template_name, context)
    
    
    def post(self, request, *args , **kwargs):
        context = self.get_context_data()
        if "filtr" in request.POST:
            start_date  = request.POST.get("from")
            end_date  = request.POST.get("till")
            if start_date and end_date:
                context["items"] = context["storage"].items.filter(date_added__range=(start_date, end_date))
            else:
                pass
        
        if "add_product" in request.POST:
            product = Product.objects.create(
                name = request.POST.get("name"),
                amount = request.POST.get("amount"),
                measurement_unit = request.POST.get("measurement_unit"),
                income = request.POST.get("income"),
                body_price = request.POST.get("body_price"),
                max_amount = request.POST.get("limit"),
                storage = context["storage"],
            )
        if "delete" in request.POST:
            try:
                product = Product.objects.get(id=request.POST.get("product"))
                product.delete()
            except Product.DoesNotExist:
                return redirect("storage:storage")
                
            
        if "action" in request.POST:
            product = Product.objects.get(id=request.POST.get("product"))
            context["edit_product"] = product
            return JsonResponse({'success': True, 'item': {
                    'id': product.id,
                    'name': product.name,
                    'amount': product.amount,
                    'measurement_unit': product.measurement_unit,
                    'income': product.income,
                    'body_price': product.body_price,
                    'max_amount': product.max_amount
                }})
            
        # Editing
        if "save" in request.POST:
            product_id = request.POST.get("product")
            print(product_id)
            product = get_object_or_404(Product, id=product_id)
            product.name = request.POST.get("name")
            product.amount = request.POST.get("amount")
            product.measurement_unit = request.POST.get("measurement_unit")
            product.income = request.POST.get("income")
            product.body_price = request.POST.get("body_price")
            product.max_amount = request.POST.get("limit")
            product.save()

        # Exporting
        if 'excel' in request.POST:
            return export_products_to_excel(context["items"])
        if "pdf" in request.POST:
            return export_products_to_pdf(context["items"])
        
        if "search" in request.POST:
            try:
                product = Product.objects.filter(name__icontains=request.POST.get("query"))
                context["items"] = product
            except Product.DoesNotExist:
                return redirect("storage:storage", slug="your-slug-value")
            
        return render(request, self.template_name, context)
