from django.urls import URLPattern, path
from .views import *
from django.conf.urls.static import static
from forum import settings

# вызов функции as_view 

urlpatterns = [
    path('', home_page, name='home_page'),
    path('posts-page/<slug>/', posts_page, name='posts_page'),
    path('detail-page/<slug>/', detail_page, name='detail_page'),
    path('create-post/', create_post, name="create_post"),
    path('latests-posts/', latests_posts, name='latests_post'),
    path('search-results/', search_page, name='search_page')
]

if settings.DEBUG:      #для того, чтобы в режиме отладки ко всем маршрутам добавлялся маршрут с графическими файлами
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)