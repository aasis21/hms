from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta, date, datetime
from hms.settings import GR_COUNT
from django.contrib import messages
from django.db.models import Count
from accounts.models import Profile
from bill.models import *
def temp(request):
    if request.method == 'POST':
        req_form = RequestForm(request.POST)
        print("WWW : " ,request.POST)
        return render(request, 'grb/book_form.html', {'form' : req_form })
    req_form = RequestFormSet()
    return render(request, 'grb/book_form.html', {'formset' : req_form })

def see_requests(request):
    if str(request.user) != 'halloffice':
        return redirect('/')
    users_list = Request.objects.values('user').distinct()
    bookings = []
    for x in users_list:
        tmp_unm = User.objects.get(pk = x["user"])
        tmp_bk = Request.objects.filter(booking_status = 'P', user = tmp_unm)
        if len(tmp_bk) == 0 :
            continue
                    
        bookings += [{
            "user" : Profile.objects.get(user = tmp_unm),
            "books" : tmp_bk,
            "count" : len(tmp_bk)
        }]
        # bookings[tmp_unm] = Request.objects.filter(booking_status = 'P', user = tmp_unm)
    return render(request, 'grb/see_req.html', {'booking_list' : bookings})

def user_requests(request, username):
    if str(request.user) != 'halloffice':
        return redirect('/')
    tmp_unm = User.objects.get(username = username)
    bookings = Request.objects.filter(booking_status = 'P', user = tmp_unm).order_by('-pk')
    return render(request, 'grb/indiv_req.html', {'booking_list' : bookings, "username" : username})

def delete_requests(request, pk):
    if str(request.user) != 'halloffice':
        return redirect('/')
    if Request.objects.filter(pk = pk):
        obj = Request.objects.get(pk = pk)
        username = obj.user
        obj.delete()
        messages.success(request, "Deleted Successfully")
        print("Deleted Successfully")
        return redirect('/grb/individual-requests/{0}'.format(username))
    messages.error(request, "Requested entity doesn't exist")
    print("doesnt exist")
    return redirect('/'.format(username))

def approve_requests(request, pk):
    if str(request.user) != 'halloffice':
        return redirect('/')
    if Request.objects.filter(pk = pk):
        obj = Request.objects.get(pk = pk)
        username = obj.user
        biller=Billers.objects.filter(user=request.user).first()
        Bill.objects.create(user=username,bill=250, biller=biller, reason="Guest room accepted 1 room")
        obj.booking_status = 'B'
        obj.save()
        subject = 'Hall office Approved your guest room booking request for '+ str(obj.date)
        message =   render_to_string('grb/accept1.html', {'user':username,'date': str(obj.date), 'status':'accepted'})
        username.email_user(subject, message)
        messages.success(request, " Successfull")
        print(" Successfully")
        return redirect('/grb/individual-requests/{0}'.format(username))
    messages.error(request, "Requested entity doesn't exist")
    print("doesnt exist")
    return redirect('/'.format(username))

def approve_all(request, username):
    if str(request.user) != 'halloffice':
        return redirect('/')
    if User.objects.filter(username = username) != None:
        tmp_obj = User.objects.get(username = username)
        obj = Request.objects.filter(user = tmp_obj,booking_status='P')
        cnt=obj.count()
        biller=Billers.objects.filter(user=request.user).first()
        Bill.objects.create(user=tmp_obj,bill=(int(cnt))*250, biller=biller, reason="Guest room accepted")
        obj.update(booking_status = 'B')
        subject = 'Hall office Approved all your pending guest room booking request '
        message =  'Hall office Approved all your pending guest room booking request '
        username.email_user(subject, message)
        messages.success(request, " Successfull")
        print(" Successfully")
        return redirect('/grb/individual-requests/{0}'.format(username))
    messages.error(request, "Requested entity doesn't exist")
    print("doesnt exist")
    return redirect('/'.format(username))

def delete_all(request, username):
    if str(request.user) != 'halloffice':
        return redirect('/')
    if User.objects.filter(username = username) != None:
        tmp_obj = User.objects.get(username = username)
        obj = Request.objects.filter(user = tmp_obj)
        obj.delete()
        subject = 'Hall office Declined your guest room booking request for'+ str(obj.date)
        message = render_to_string('grb/accept1.html', {'user':username,'date': str(obj.date), 'status':'declined'})
        username.email_user(subject, message)
        messages.success(request, " Successfull")
        print(" Successfully")
        return redirect('/grb/individual-requests/{0}'.format(username))
    messages.error(request, "Requested entity doesn't exist")
    print("doesnt exist")
    return redirect('/'.format(username))



def book_room(request, book_date):
    if request.method == 'POST':
        book_form = RequestForm(request.POST, q_date = book_date)
        if book_form.is_valid():
            cdata = book_form.cleaned_data

            for x in cdata:
                print("X : ",x)
        return HttpResponse("ppp")

def show_vacancies(request, start_date, end_date):
    if request.method == 'POST':
        req_data = request.POST
        req_form = RequestForm(request.POST)
        if req_form.is_valid():
            cdata = req_form.cleaned_data
            print(cdata)
            for x in cdata:
                if cdata[x] and x !="book_date":
                    if Request.objects.filter(date = cdata["book_date"], room = int(x[5:]), booking_status= "B"):
                        messages.error(request, "Guest Room {0} can't be booked for {1} as it is already booked by someone else".format(x[5:], cdata["book_date"]))

                    if Request.objects.filter(date = cdata["book_date"], room = int(x[5:]), user = request.user):
                        messages.error(request, "You have already requested for this entity".format(x[5:], cdata["book_date"]))

                    else:
                        room_obj = Request(date = cdata["book_date"],room = int(x[5:]), user = request.user)
                        room_obj.save()
                        messages.success(request, "Guest Room {0} requested for {1}".format(x[5:], cdata["book_date"]))

            return redirect('/grb/show/{0}/{1}'.format(start_date, end_date))

    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        req_forms = []
        for n in range(int ((end_date - start_date).days)+1):
            # my_date = (start_date + timedelta(n)).strftime("%Y-%m-%d")
            my_date = (start_date + timedelta(n)).date()
            req_forms += [RequestForm(q_date = my_date, q_request = request)]
        return render(request, 'grb/book_form.html', {'formset' : req_forms})



    return HttpResponse("my_date")
def select_range(request):
    if request.method == 'POST':
        range_form = GRRangeForm(request.POST)
        if range_form.is_valid():
            cdata = range_form.cleaned_data
            print("CD", cdata)
            return redirect('/grb/show/{0}/{1}'.format(cdata["start_date"], cdata["end_date"]))

    else:
        range_form = GRRangeForm()
        return render(request, 'grb/select_range.html', {'form' : range_form})
