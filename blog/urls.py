from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import IndexPageView, PostDetailView, PostCreateView, EditPostView, DeletePostView, SearchResultsView

urlpatterns = [
    path('', IndexPageView.as_view(), name='index-page'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/update/<int:pk>/', EditPostView.as_view(), name='edit-post'),
    path('posts/delete/<int:pk>/', DeletePostView.as_view(), name='delete-post'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

