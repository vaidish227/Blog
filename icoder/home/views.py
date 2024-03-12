from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post

#this is inbuilt facility
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from blog.views import blogHome

# HTML Pages.
def home(request):
    allPosts= Post.objects.all()
    context={'allPosts': allPosts}
    return render(request,'home/home.html',context)
    #return HttpResponse('this is home')

def about(request):
    allPosts= Post.objects.all()
    context={'allPosts': allPosts}
    return render(request,'home/about.html',context) 

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

#this function help to search the query from search button and the blog post
#icontain is the way for search key word available in our post 
def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)


# Authentication APIs
#This code for handling singup
def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        #user name should be under 10 character
        if len(username)<10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')
        #user name shoupd be alphanumeric
        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        #Passwrd should match
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your iCoder has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")
    
   # Login and Logout
def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found") 

#logout function
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')
