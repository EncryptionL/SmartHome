from django.shortcuts import render

def index(request):
    context = {
        'menus':[
            ['Home','/'],
            ['Pi','/pi']
        ]
    }
    return render(request, 'index.html', context)
