from django.urls import path
from . import views

# Register your urls here.

urlpatterns = [    
    path('publisher/', views.PublisherView.as_view(), name='publisher'),
    path('publisher/<int:id>', views.PublisherViewId.as_view(), name='publisher-id'),
    path("game/<str:location>", views.PublisherViewLocation.as_view(), name="publisher-location"),
    
    path("game/", views.GamesView.as_view(), name="game"),
    path("game/<int:id>", views.GamesViewId.as_view(), name="game-id"),
    path("game/<int:publisher>", views.GamesViewPublisher.as_view(), name="game-publisher"),
    
]
