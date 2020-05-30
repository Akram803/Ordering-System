from django.shortcuts import get_object_or_404, render, Http404
from django.views.generic import View, ListView, DetailView
from menu.models import Category, Item, AnonymouseOrder, AnonymouseOrderItems, CustomerOrder, CustomerorderItems
from django.http import HttpResponse

 
# Create your views here.

# Create your views here.

class HomeView(View):

    template_name = 'home.html'
    context = None 

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated and not request.session.session_key:
            request.session.create()
        return render(request, self.template_name, self.context)

    # @staticmethod
    # def get_context_data(**kwargs):
    #     context_ = {
    #         'cats_list': Category.objects.all(),
    #     }
    #     return context_

class CategoryListView(ListView):
    model = Category
    template_name = "menu/category-list.html"
    context_object_name = 'cats_list'
    paginate_by = 4

    # overwrite
    def get_queryset(self):
        #return Book.objects.filter(title__icontains='programin')[:10]
        
        return Category.objects.all()

    # def get_context_data(self, **kwargs): 
    #     context = super(ItemListView, self).get_context_data(**kwargs) 
    #     context['cats_list'] = Category.objects.all()
    #     return context

class ItemListView(ListView):
    model = Item 
    template_name = "menu/item-list.html"
    # paginate_by = 5
    context_object_name = 'items_list'  

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
        
    #overwrite
    def get_queryset(self):
        # get_list_or_404(Item,category__name__exact=self.kwargs['cat'])
        queryset = Item.objects.filter(category__name__exact=self.kwargs['cat'])
        if len(queryset) > 0:
            return queryset
        else:
            raise Http404

    #overwrite
    def get_context_data(self, **kwargs): 
        context = super(ItemListView, self).get_context_data(**kwargs) 
        context['this_cat'] = self.kwargs['cat']
        common.get_cats(context)
        return context

class ItemDetailView(DetailView):
    model = Item
    template_name = "menu/item-detail.html"

    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(self.model, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        common.get_cats(context)
        return context

class SearchView(View):
    model = Item 
    template_name = "menu/item-list.html"
    

    def get(self, request, *args, **kwargs):
        search_key :str = request.GET.get("q")
        if not search_key:
            raise Http404
        query = Item.objects.filter(name__icontains=search_key)
        print(query)
        return render(request, self.template_name, {"items_list":query})

    def post(self, request, *args, **kwargs):
        ...


    
class AddItemToOrder(View):

    item_id = None
    number = 1

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.item_id = request.GET.get('item')
        self.number = int(request.GET.get('n'))

    def get(self, request):
        if request.user.is_authenticated:
            return self.AddItemAsAuthonticated(request)
        else:
            return self.AddItemAsAnonymouse(request)

    def AddItemAsAnonymouse(self, request):
        # if there is no order then make it
        current_order, created = AnonymouseOrder.objects.get_or_create(
                                                            customer = request.session.session_key,
                                                            checked_out =False,
                                                            )

        try:
            bridg_record = AnonymouseOrderItems.objects.get(anonymouseorder= current_order.id, item= self.item_id)
        except:
            current_order.items.add(self.item_id)
            bridg_record = AnonymouseOrderItems.objects.get(anonymouseorder= current_order.id, item= self.item_id)
        
        bridg_record.number += self.number
        bridg_record.save()

        current_order.add_price(self.item_id, self.number)

        # print(self.request.COOKIES)
        return HttpResponse(True)

    def AddItemAsAuthonticated(self, request):
        #  get or create
        current_order, created = CustomerOrder.objects.get_or_create(
                                                                    customer = request.user, 
                                                                    checked_out = False,
                                                                )
        try:
            record = CustomerorderItems.objects.get(order= current_order.id, item= self.item_id)
        except:
            current_order.items.add(self.item_id,) # default number = 1
            record = CustomerorderItems.objects.get(order= current_order.id, item= self.item_id)
        record.number += self.number
        record.save()

        current_order.add_price(self.item_id, self.number)

        return HttpResponse(True)

class OrderListView(View):

    def get(self, request):
        
        if request.user.is_authenticated:
            orders = self.get_customer_orders()
        else:
            orders = self.get_anonymous_orders()

        return render(request,"order/order-list.html", {'orders_list': orders})
        
    def get_customer_orders(self):
        return CustomerOrder.objects.filter(customer = self.request.user.id)
    
    def get_anonymous_orders(self):
        return AnonymouseOrder.objects.filter(customer = self.request.session.session_key)

class OrderItemsListView(View):

    context = {}

    def get(self, request, id):

        if request.user.is_authenticated:
            self.get_customer_order()
        else:
            self.get_anonymous_order()

        
        return render(request,"order/order-items-list.html",self.context)

    def get_customer_order(self, ):
        try:
            self.context["order"] = CustomerOrder.objects.get(id = self.kwargs["id"], customer = self.request.user.id)
        except:
            raise Http404
        self.context["items"] = self.context["order"].items.all()

        records = CustomerorderItems.objects.filter(order = self.context["order"].id)
        for item, record in zip(self.context["items"], records):       
            item.number = record.number

    def get_anonymous_order(self):

        print(self.request.session.session_key)

        try:
            self.context["order"] = AnonymouseOrder.objects.get(id = self.kwargs["id"], customer = self.request.session.session_key)
        except:
            raise Http404
        self.context["items"] = self.context["order"].items.all()

        records = AnonymouseOrderItems.objects.filter(anonymouseorder = self.context["order"].id)
        for item, record in zip(self.context["items"], records):       
            item.number = record.number

def submit_order(request, order_id):
    if request.user.is_authenticated:
        try:
            CustomerOrder.objects.get(id = order_id, 
                                        customer = request.user.id ).submit()
        except:
            return HttpResponse(False)
                                                       
    else:
        try:
            AnonymouseOrder.objects.get(id = order_id, 
                                    customer = request.session.session_key).submit()
        except:
            return HttpResponse(False)

    return HttpResponse(True)


class common():
    @classmethod
    def get_cats(self,context):
        context['cats_list'] = Category.objects.all()












