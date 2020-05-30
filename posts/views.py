from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Post
from .forms import PostForm

# Create your views here.
# ______________________CREATE__________________________
class PostCreatView(View): 
    template = 'posts/create.html' 

    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(request, self.template, {'form':form})

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST , request.FILES)
        if form.is_valid(): 
            the_new_post = form.save(commit=True)
            messages.success(request, "created successfuly")
            return redirect(the_new_post.get_absolute_url())
        messages.warning(request, "something went wrong")
        return render(request, self.template, {'form':form})
    
# ------------------------------------------------------
# ______________________DETAIL__________________________
class PostDetailView(View):
    template = 'posts/detail.html'
    
    def get(self, request, *args, **kwargs):

        return render(request, self.template, { 'object': self.get_queryset})

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')

    def get_queryset(self):
        _id = self.kwargs.get('id')
        return get_object_or_404(Post, id=_id)
    
# ------------------------------------------------------
# ______________________LIST____________________________
class PostListView(View):
    template = 'posts/list.html'

    def get(self, request, *args, **kwargs):
        object_list = Post.objects.all()#.order_by("-timestamp")

        page_number = request.GET.get('page')
        paginator = Paginator(object_list, 10) # Show 10 contacts per page.
        page_obj = paginator.get_page(page_number)

        return render(request, self.template, {'object_list':page_obj})

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request! are you okey')

# ------------------------------------------------------
# ______________________UPDATE__________________________
class PostUpdateView(View):
    template = 'posts/create.html'

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, id=self.kwargs.get('id'))
        form = PostForm(instance = instance)
        print(form.changed_data)
        return render(request, self.template, {'form':form})

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, id=self.kwargs.get('id'))
        form = PostForm(request.POST , request.FILES)
        if form.is_valid():
            new_instance= form.save(commit=False)
            instance.title = new_instance.title
            instance.content = new_instance.content
            instance.image = new_instance.image
            instance.save()
            messages.success(request, 'updated successfully')
            return redirect(instance.get_absolute_url())
        messages.success(request, 'something went wrong')
        return render(request, self.template, {'form':form})

# ------------------------------------------------------
# ______________________DELETE__________________________
class PostDeleteView(View):
    template = 'posts/list.html'

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, id=self.kwargs.get('id'))
        instance.delete()
        messages.success(request, 'deleted successfully')
        return redirect('posts:list')

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')

