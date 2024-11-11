from django.urls import path
from . import views

# Register your urls here.

urlpatterns = [    
    path('publisher/', views.PublisherView.as_view(), name='publisher'),
    path('publisher/<int:id>', views.PublisherViewId.as_view(), name='publisher-id'),
    path('publisher/<str:location>', views.PublisherViewLocation.as_view(), name='publisher-location'),
    path('publisher/<int:id>/games', views.PublisherViewGames.as_view(), name='publisher-games'),
    
    path('game/', views.GameView.as_view(), name='game'),
    path('game/<int:id>', views.GameViewId.as_view(), name='game-id'),
    path('game/<str:genre>', views.GameViewGenre.as_view(), name='game-genre'),
    
]
