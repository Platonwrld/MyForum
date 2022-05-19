from .models import *


""" Function that allow use search """
def search(request):

    context_search = {}

    posts = Post.objects.all()

    # if word from search(button) form(base) in GET request, that means if form was submited with specify word
    # то есть запрашеваемое слово, из формы(button search), на которое ссылается переменная q
    if 'search' in request.GET:
        query = request.GET.get('q')    # getting query that define like q variable, q defined in input like name, q = query

    # filter starts
        search_box = request.GET.get('search-box')      # search-box - it's div in template, that's contain key-words, that's will be query in bd

        # if query key-word == Descriptions, that's means that in db will be query for model content, and search in data from content model
        if search_box == 'Descriptions':
            objects = posts.filter(content__icontains=query)

        else:
            objects = posts.filter(title__icontains=query)
    # filter ends

        context_search = {
            'posts': posts,
            'objects': objects,
            'query': query,

        }

    return context_search