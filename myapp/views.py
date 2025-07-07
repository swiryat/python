# myapp/views.py
from django.shortcuts import render

def my_view(request):
    # Ваш код представления
    return render(request, 'my_template.html', {'variable': 'value'})



