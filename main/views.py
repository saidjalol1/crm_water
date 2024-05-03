from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from expances.models import Expances
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Decorators
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class MainView(View):
    template_name = "index.html"
    
    def get_context_data(self, *args, **kwargs):
        context = {}
        context["debt_sales"] = Expances.objects.filter(payment_type="nasiya")
        return context
    
    
    def get(self, request):
        context = self.get_context_data()
        print(context)
        return render(request, self.template_name, context)
    
    
    def post(self, request):
        context = self.get_context_data()
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