from django.shortcuts import render, HttpResponse
from home.models import Contact
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,'home/home.html')
    #return HttpResponse('this is home')

def about(request):
   return render(request,'home/about.html') 

#this will use for post request and save the data in the data base..
# Contact page
#all this method are imported from Template/home/contact.html 
def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        # Message alert Show Valid or Invalid
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request,'home/contact.html')

