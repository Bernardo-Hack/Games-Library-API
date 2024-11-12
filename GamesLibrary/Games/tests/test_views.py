from datetime import date
from django.urls import reverse

from Games.models import Publisher, Game
from Games.serializers import PublisherSerializer, GameSerializer

from rest_framework import status
from rest_framework.test import APITestCase

# Tests for (almost) all views in the Games app.

# -=-=- Publisher Tests -=-=-


class PublisherViewTest(APITestCase):
        
        def setUp(self):
            self.publisher = Publisher.objects.create(
                name='New Publisher',
                location='New Location',
                website='https://newpublisher.com'
            )

            self.url = reverse('publisher')


        def test_get_publishers_success(self):
            response = self.client.get(self.url)
            publishers = Publisher.objects.all()
            serializer = PublisherSerializer(publishers, many=True)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data, serializer.data)


        def test_get_publishers_empty(self):
            Publisher.objects.all().delete()

            response = self.client.get(self.url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, [])


        def test_post_publisher_success(self):
            data = {
                'name': 'Updated Publisher', 
                'location': 'Updated Location',
                'website' : 'https://updatedpublisher.com'
                }

            response = self.client.post(self.url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['name'], data['name'])
            self.assertEqual(response.data['location'], data['location'])
            self.assertEqual(response.data['website'], data['website'])


        def test_post_publisher_duplicate(self):
            data = {
                'name': 'New Publisher', 
                'location': 'Updated Location',
                'website' : 'https://updatedpublisher.com'
                }
            
            response = self.client.post(self.url, data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['error'], 'Publisher already exists.')


class PublisherViewIdTest(APITestCase):
        
        def setUp(self):
            self.publisher = Publisher.objects.create(
                name='New Publisher',
                location='New Location',
                website='https://newpublisher.com'
            )

            self.duplicate_publisher = Publisher.objects.create(
                name='Sample Publisher',
                location="Sample Location",
                website='https://samplepublisher.com'
            )

            self.url = reverse('publisher-id', args=[self.publisher.id])


        def test_get_publisher_success(self):
            response = self.client.get(self.url)
            serializer = PublisherSerializer(self.publisher)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, serializer.data)


        def test_get_publisher_not_found(self):
            url = reverse('publisher-id', args=[9999])
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data['detail'], 'Publisher with given ID(9999) not found.')


        def test_put_publisher_success(self):
            data = {'name': 'Updated Publisher', 'location': 'Updated Location'}

            response = self.client.put(self.url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['name'], 'Updated Publisher')
            self.assertEqual(response.data['location'], data['location'])


        def test_put_publisher_not_found(self):
            data = {
                'name': 'Non Existent Publisher', 
                'location': 'Non Existent Location'
                }
            
            url = reverse('publisher-id', args=[9999])
            response = self.client.put(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data['detail'], 'Publisher with given ID(9999) not found.')


        def test_delete_publisher_success(self):
            response = self.client.delete(self.url)

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            with self.assertRaises(Publisher.DoesNotExist):
                Publisher.objects.get(id=self.publisher.id)


        def test_delete_publisher_not_found(self):
            url = reverse('publisher-id', args=[9999])
            response = self.client.delete(url)

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data['detail'], 'Publisher with given ID(9999) not found.')


# -=-=- Game Urls -=-=-


class GameViewTest(APITestCase):
        
    def setUp(self):
        self.publisher = Publisher.objects.create(
            name="Sample Publisher", 
            location="Sample Location", 
            website="http://samplepublisher.com"
        )
        
        self.game = Game.objects.create(
            title="Sample Game",
            description="This is a sample game description.",
            release_date=date(2022, 1, 1),
            genre="Action",
            onWindows=True,
            onMac=False,
            onLinux=True
        )

        self.url = reverse('game')


    def test_get_games_success(self):
        response = self.client.get(self.url)
        serializer = GameSerializer(Game.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)


    def test_get_games_empty(self):
        Game.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


    def test_post_game_success(self):
        data = {
            'title': 'New Game', 
            'description': 'New description', 
            'publisher': [self.publisher.id],
            'release_date': '2022-01-01',
            'genre': 'RPG',
            'onWindows': True,
            'onMac': False,
            'onLinux': True
            }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Game')


    def test_post_game_exists(self):
        data = {
            'title': 'Sample Game', 
            'description': 'New description', 
            'publisher': [self.publisher.id],
            'release_date': '2022-01-01',
            'genre': 'RPG',
            'onWindows': False,
            'onMac': True,
            'onLinux': False
            }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Game already exists.')


class GameViewIdTestCase(APITestCase):

    def setUp(self):
        self.publisher = Publisher.objects.create(
            name="Sample Publisher", 
            location="Sample Location", 
            website="http://samplepublisher.com"
        )
        
        self.game = Game.objects.create(
            title="Sample Game",
            description="This is a sample game description.",
            release_date=date(2022, 1, 1),
            genre="Action",
            onWindows=True,
            onMac=False,
            onLinux=True
        )

        self.url = reverse('game-id', args=[self.game.id])
    

    def test_get_game_success(self):
        response = self.client.get(self.url)
        serializer = GameSerializer(self.game)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_get_game_not_found(self):
        url = reverse('game-id', args=[9999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Game with given ID(9999) not found.')


    def test_put_game_success(self):
        data = {'title': 'Updated Game Name', 'genre': 'Adventure'}
        
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Game Name')


    def test_put_game_not_found(self):
        data = {
            'title': 'Non Existent Game', 
            'description': 'New description', 
            'publisher': [self.publisher.id],
            'release_date': '2012-12-12',
            'genre': 'RPG',
            'onWindows': True,
            'onMac': False,
            'onLinux': True
            }
        
        url = reverse('game-id', args=[9999])
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Game with given ID(9999) not found.')


    def test_delete_game_success(self):
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Game.DoesNotExist):
            Game.objects.get(id=self.game.id)


    def test_delete_game_not_found(self):
        url = reverse('game-id', args=[9999])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Game with given ID(9999) not found.')
