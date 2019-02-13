from django.shortcuts import render,redirect
from django.contrib import messages,auth
from .models import Contact
from django.core.mail import send_mail
def contact(request):
    if request.method=='POST':
        listing_id=request.POST['listing_id']
        listing=request.POST['listing']
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        user_id=request.POST['user_id']
        realtor_email=request.POST['realtor_email']

    #check if user has already made inquery
    if request.user.is_authenticated:
        user_id = request.user.id
        has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
        if has_contacted:
            messages.error(request,"You already made inquiry for this car")
            return redirect('/listings/'+listing_id)
    
    contact = Contact(listing=listing,listing_id=listing_id,name=name,phone=phone,email=email,message=message,user_id=user_id)

    contact.save()

    #send email
    send_mail(
        'CAR INQUIRY',
        'THERE HAS BEEN AN INQUIRY FOR ' + listing + '. SIGN INTO ADMIN TO KNOW MORE',
        'kalitester007@gmail.com',
        [realtor_email,'aashutosh.sehgal@gmail.com'],
        fail_silently= False
    )
    messages.success(request,"your request has been submitted, Realtor will reach you soon...")

    return redirect('/listings/'+listing_id)

