from django.shortcuts import redirect, render
from django.views import View
from users.forms import UserRegistrationForm , AuthenticationForm
from django.http import HttpResponse


# Create your views here.
class register(View):

    def get(self, request):
        form = UserRegistrationForm
        return render(request, 'users/register.html', {'form': form,})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Valid data')
            # if username is not exsist
            form.save()
            return redirect('menu:home')

        return self.get(request)


class StuffOrderListView(View):
    
    def get(self, request):
        
        return HttpResponse("0")
    
















