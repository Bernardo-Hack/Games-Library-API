from django.urls import path
from . import views

# Register your urls here.

urlpatterns = [    
    path('publisher/', views.AlbumView.as_view(), name='publisher'),
    path('publisher/<int:id>', views.AlbumViewId.as_view(), name='publisher-id'),
    
    path("game/", views.FaixaView.as_view(), name="game"),
    path("game/<int:id>", views.FaixaViewId.as_view(), name="game-id"),
    path("game/<int:publisher>", views.FaixaViewPublisher.as_view(), name="game-publisher"),
    
]
