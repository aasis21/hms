from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum,F
from django.contrib.auth.models import User
from .tables import *
from django_tables2 import RequestConfig

from .models import *
from .forms import *
# Create your views here.
@login_required
def bill(request):
    if Billers.objects.filter(user=request.user).exists():
        biller=Billers.objects.filter(user=request.user).first()
        x=Bill.objects.filter(biller=biller).values(name=F('user__username')).annotate(total_bill=-1*Sum('bill'))
        table=BillTable(x)
        RequestConfig(request).configure(table)
        return render(request, 'bill/bill.html', {'table': table})
    else:
        x=Bill.objects.filter(user=request.user).values(name=F('biller__name')).annotate(total_bill=Sum('bill'))
        table=BillTable(x)
        RequestConfig(request).configure(table)
        return render(request, 'bill/bill.html', {'table': table})

@login_required
def transiction(request):
    if Billers.objects.filter(user=request.user).exists():
        biller=Billers.objects.filter(user=request.user).first()
        transictions=Bill.objects.filter(biller=biller)
        f=TransictionFilter1(request.GET, queryset=transictions)
        table=TransictionTable1(f.qs)
        RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
        return render(request, 'bill/bill.html', {'table': table,'filter':f})
    else:
        transictions=Bill.objects.filter(user=request.user)
        f=TransictionFilter2(request.GET, queryset=transictions)
        table=TransictionTable(f.qs)
        RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
        return render(request, 'bill/bill.html', {'table': table,'filter':f})

@login_required
def addbill(request):
    if Billers.objects.filter(user=request.user).exists():
        biller=Billers.objects.filter(user=request.user).first()
        if request.method == 'POST':
            form = BillForm(request.POST)

            if form.is_valid():
                user=User.objects.filter(username=form.cleaned_data['user'])
                if user.exists():
                    Bill.objects.create(user=user.first(),bill=int(form.cleaned_data['bill']), biller=biller, reason=form.cleaned_data['reason'] )
                return HttpResponseRedirect(reverse('bills:addbill'))
        else:
            form = BillForm()

        return render(request, 'bill/billform.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('bills:bill'))
        
@login_required
def mess_rembursement(request):
    if Billers.objects.filter(user=request.user).exists():
        biller=Billers.objects.filter(user=request.user).first()
        if(request.user.username=='mess'):
            rem=Messrem.objects.filter(status=0)
            f=MessFilter(request.GET, queryset=rem)
            table=MessTable(f.qs)
            RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
            return render(request, 'bill/mess.html', {'table': table,'filter':f})
        else:
            return HttpResponseRedirect(reverse('bills:bill'))
    else:
        if request.method == 'POST':
            form = MessForm(request.POST)
            if form.is_valid():
                Messrem.objects.create(user=request.user,start=form.cleaned_data['start_data'],end=form.cleaned_data['end_data'])
                return HttpResponseRedirect(reverse('bills:messrem'))
        else:
            form = MessForm()
            return render(request, 'bill/messremform.html', {'form': form})


@login_required
def rmremb(request,id):
    if(request.user.username=='mess'):
        rem=Messrem.objects.filter(id=id)
        if rem.exists():
            rem=rem.first()
            rem.status=-1
            rem.save()
    return HttpResponseRedirect(reverse('bills:messrem'))

@login_required
def accept(request):
    if(request.user.username=='mess'):
        rem=Messrem.objects.filter(status=0)
        biller=Billers.objects.filter(user=request.user).first()
        if rem.exists():
            for x in rem:
                amount=x.end-x.start
                amount=amount.days
                amount=int(amount)*50
                Bill.objects.create(user=x.user,bill=-amount, biller=biller, reason="Rembursement cleared" )
                x.status=1
                x.save()
                
    return HttpResponseRedirect(reverse('bills:messrem'))