from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if response.method == "POST":
        print(response.POST)
        if response.POST.get('save'):
            
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)):
                    item.complete = True
                else:
                    item.complete = False
                item.save()

        elif response.POST.get('newItem'):
            txt = response.POST.get('new')
            
            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
            else:
                print('ERROR invalid item text')

        # Нужно делать redirect, чтобы post запрос обнулился.
        return HttpResponseRedirect(f"/{ls.id}")

    return render(response, "main/list.html", {"ls": ls})

def home(response):
    # Вывыедем в таблице текущие 5 первых списков и кол-во item в них.
    todo_lists = ToDoList.objects.all()

    context_todo = []
    for list in todo_lists[:5]:
        context_todo.append( (list.name, len(list.item_set.all()), list.id) )

    return render(response, "main/home.html", {"context_todo": context_todo})
    

def create(response):
    if response.method == "POST":
        print(response.POST)
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            
            return HttpResponseRedirect(f"/{t.id}")
        else:
            return HttpResponseRedirect(f"/create")

    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form": form})
