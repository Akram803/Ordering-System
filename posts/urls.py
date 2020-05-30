from django.urls import path, include
from .views import (
    PostCreatView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
)
 
 
app_name = 'posts'
urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('create', PostCreatView.as_view(), name='create'),
    path('<int:id>', PostDetailView.as_view(), name='detail'),
    path('<int:id>/edit', PostUpdateView.as_view(), name='update'),
    path('<int:id>/delete', PostDeleteView.as_view(), name='delete'),
]