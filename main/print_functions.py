from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from openpyxl import Workbook
from django.http import JsonResponse, HttpResponse


def export_products_to_excel(products):
    # Create a new workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Chiqimlar"

    # Define headers
    headers = ["Nomi", "Summasi", "Valyuta", "Sanasi"]
    ws.append(headers)

    # Write product data to the worksheet
    for product in products:
        ws.append([product.name,product.amount,product.currency,product.date_added])

    # Create a response with Excel content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Set the content-disposition header to force download the file
    response['Content-Disposition'] = 'attachment; filename=chiqim.xlsx'

    # Save the workbook content to the response
    wb.save(response)
    print("ishladi")
    return response


def export_products_to_pdf(products):
    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')

    # Set the content-disposition header to force download the file
    response['Content-Disposition'] = 'attachment; filename=chiqim.pdf'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Define table data (products)
    data = [["Nomi", "Summasi", "Valyuta", "sanasi"]]
    for product in products:
        data.append([product.name,product.amount , product.currency, product.date_added])

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


def export_products_to_excel_debts(products):
    # Create a new workbook
    wb = Workbook()
    ws = wb.active
    ws.title ='Qarzlar'

    # Define headers
    headers = ["Ismi", "Mahsulot nomi", "Mahsulot miqdori", "To'lov turi","Holati", "Jami summasi", "Jami foyda", "muddati"]
    ws.append(headers)

    # Write product data to the worksheet
    for product in products:
        status = "To'landi" if product.status else "To'lanmadi"
        ws.append([product.name,product.product_name.name,product.product_amount,product.payment_type, status,product.get_overall(), product.get_income(), product.deadline])

    # Create a response with Excel content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Set the content-disposition header to force download the file
    response['Content-Disposition'] = f'attachment; filename=Qarzlar.xlsx'

    # Save the workbook content to the response
    wb.save(response)
    print("ishladi")
    return response



def export_products_to_pdf_debts(products):
    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')

    # Set the content-disposition header to force download the file
    response['Content-Disposition'] = 'attachment; filename=Qarzlar.pdf'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Define table data (products)
    data = [["Ismi", "Mahsulot nomi", "Mahsulot miqdori", "To'lov turi","Holati", "Jami summasi", "Jami foyda", "muddati"]]
    for product in products:
        status = "To'landi" if product.status else "To'lanmadi"
        data.append([product.name,product.product_name.name,product.product_amount,product.payment_type, status,product.get_overall(), product.get_income(), product.deadline])

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