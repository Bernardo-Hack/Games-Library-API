from django.urls import path
from . import views

urlpatterns = [    
    path('publishers/', views.list_publishers, name='list_publishers'),
    path('publisher/<int:id>', views.get_publisher, name='get_publisher'),
    path('create_publisher/', views.create_publisher, name='create_publisher'),
    path('update_publisher/<int:id>', views.update_publisher, name='update_publisher'),
    path('delete_publisher/<int:id>', views.delete_publisher, name='delete_publisher'),

    path('games/', views.list_games, name='list_games'),
    path('game/<int:id>', views.get_game, name='get_game'),
    path('games_by/<int:id>', views.get_games_by_publisher, name='get_games_by_publisher'),
    path('create_game/', views.create_game, name='create_game'),
    path('update_game/<int:id>', views.update_game, name='update_game'),
    path('delete_game/<int:id>', views.delete_game, name='delete_game'),
]
