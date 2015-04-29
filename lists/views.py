from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.views.generic import FormView, CreateView
from django.views.generic.detail import SingleObjectMixin

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List


class HomePageView(FormView):
    form_class = ItemForm
    template_name = 'home.html'


class NewListView(CreateView, HomePageView):

    def form_valid(self, form):
        list = List.objects.create()
        Item.objects.create(text=form.cleaned_data['text'], list=list)
        return redirect('/lists/%d/' % (list.id,))


class ViewAndAddToList(CreateView, SingleObjectMixin):
    model = List
    template_name = 'list.html'
    form_class = ExistingListItemForm

    def get_form(self, form_class):
        self.object = self.get_object()
        return form_class(for_list=self.object, data=self.request.POST)


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

#def view_list(request, list_id):
#    list_ = List.objects.get(id=list_id)
#    form = ExistingListItemForm(for_list=list_)
#    if request.method == 'POST':
#        form = ExistingListItemForm(for_list=list_, data=request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect(list_)
#    return render(request, 'list.html', {'list':  list_, 'form': form})

#def new_list(request):
#    form = ItemForm(data=request.POST)
#    if form.is_valid():
#        list_ = List.objects.create()
#        form.save(for_list=list_)
#        return redirect(list_)
#    else:
#        return render(request, 'home.html', {'form': form}) 
