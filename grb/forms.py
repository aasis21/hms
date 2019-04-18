from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from hms.settings import GR_COUNT
from .models import Request
def get_roomstat(my_date, i, q_request):
        if Request.objects.filter(date = my_date, room = i, booking_status= "B"):
            return "B"
        elif Request.objects.filter(date = my_date, room = i, user = q_request.user):
            return "R"
        elif Request.objects.filter(date = my_date, room = i, booking_status= "P"):
            return "P"
        else:
            return "V"



class RequestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # if kwargs.get('q_date'):
        #     self.q_date =
        q_date = None
        if kwargs.get('q_date'):
            q_date = kwargs.pop('q_date')
            q_request = kwargs.pop('q_request')

        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['book_date'] = forms.DateField()
        self.fields['book_date'].widget = forms.HiddenInput()
        if q_date:
            self.fields["book_date"].initial = q_date
            self.fields['book_date'].widget.attrs['readonly'] = True
        for x in range(1, GR_COUNT + 1):
            self.fields['room_' + str(x)] = forms.BooleanField(required=False)
            if q_date:
                print("PP ",type(q_date))
                self.q_date = q_date
                if get_roomstat(q_date , x, q_request) == "B":
                    self.fields['room_' + str(x)].disabled = True
                    self.fields['room_' + str(x)].label = "Room {0} (booked)".format(x)

                elif get_roomstat(q_date , x, q_request) == "R":
                    self.fields['room_' + str(x)].label = "Room {0} (requested)".format(x)
                    self.fields['room_' + str(x)].disabled = True
                    print(888888888)
                elif get_roomstat(q_date , x, q_request) == "P":
                    self.fields['room_' + str(x)].label = "Room {0} (pending)".format(x)

                elif get_roomstat(q_date , x, q_request) == "V":
                    self.fields['room_' + str(x)].label = "Room {0} (available)".format(x)

class GRRangeForm(forms.Form):
    start_date = forms.DateField(widget = forms.SelectDateWidget(),required=True)
    end_date = forms.DateField(widget = forms.SelectDateWidget(),required=True)

class DeleteReqForm(forms.Form):
    pk = forms.IntegerField()

# class MessForm(forms.Form):
#     start_data=forms.DateField(widget = forms.SelectDateWidget(),required=True)
#     end_data=forms.DateField(widget = forms.SelectDateWidget(),required=True)
