from django.urls import path
from menu.views import (
                        HomeView, 
                        CategoryListView, 
                        ItemListView, 
                        ItemDetailView, 
                        AddItemToOrder, 
                        SearchView, 
                        OrderListView,
                        OrderItemsListView,
                        submit_order, 
                        CategoryCreateView,
                        ItemCreateView
                        )



app_name = 'menu'
urlpatterns = [
    path('', HomeView.as_view(),  name='home'),
    path('search/', SearchView.as_view(),  name='search'),

    path('menu/', CategoryListView.as_view(), name='menu'),
    path('category/create',CategoryCreateView.as_view(), name='category-create'),
    
    path('<slug:cat>',ItemListView.as_view(), name='item-list'),
    path('<slug:cat>/additem',ItemCreateView.as_view(), name='item-create'),

    
    path('item/<int:id>',ItemDetailView.as_view(), name='item-details'), 

    path('add/', AddItemToOrder.as_view(), name='add' ),
    path('myorders/', OrderListView.as_view(), name='order-list' ),
    path('myorder/<int:id>', OrderItemsListView.as_view(), name='order-items-list' ),

    path('submit/<int:order_id>', submit_order, name='submit-order')


]
