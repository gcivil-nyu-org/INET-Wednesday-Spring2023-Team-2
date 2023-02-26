from django.shortcuts import render
def header_view(request):
    return render(request, 'header.html')
# Create your views here.
