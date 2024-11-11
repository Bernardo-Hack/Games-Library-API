import logging

from django.shortcuts import get_object_or_404
from .models import Game, Publisher
from .serializers import GameSerializer, PublisherSerializer 
from .exceptions import PublisherIDNotFoundException, GameIDNotFoundException

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from drf_spectacular.utils import extend_schema

# Create your views here.

logger = logging.getLogger('Test: ')

# -=-=- Publisher Urls -=-=-

@extend_schema(tags=['Publisher'])
class PublisherView(APIView):
    def get(self, request):
        try:

            publishers = Publisher.objects.all()

            if not publishers:
                logger.debug('No publisher found.')
                return Response('Error while fetching publishers.', status=status.HTTP_400_BAD_REQUEST)
            
            serializer = PublisherSerializer(publishers, many=True)
            return Response(serializer.data)
        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while listing publishers.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        try:

            serializer = PublisherSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                logger.error('Publisher already exists.')
                return Response(
                    {
                        'error': 'Publisher already exists.'
                    }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while creating publisher.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(tags=['Publisher'])
class PublisherViewId(APIView):
    def get(self, request, id):
        try:

            publisher = Publisher.objects.get(id=id)
            serializer = PublisherSerializer(publisher)
            return Response(serializer.data)
        
        except Publisher.DoesNotExist:

            logger.debug('Publisher with given ID not found.')
            raise PublisherIDNotFoundException('Publisher with given ID not found.')
        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while listing publishers.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def put(self, request, id):
        try:

            publisher = get_object_or_404(Publisher, id=id)

            serializer = PublisherSerializer(publisher, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while updating publisher.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, id):
        try:

            publisher = get_object_or_404(Publisher, id=id)
            publisher.delete()
            
            return Response(
                {'message': 'Publisher deleted successfully.'},
                status=status.HTTP_204_NO_CONTENT
            )
        
        except Exception as e:
            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while deleting publisher.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# -=-=- Games Urls -=-=-

@extend_schema(tags=['Games'])
class GamesView(APIView):
    def get(self, request):
        try:

            games = Game.objects.all()
            
            if not games:
                logger.debug('No publisher found.')
                return Response('Error while fetching games.', status=status.HTTP_400_BAD_REQUEST)
            
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data)
        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while listing games.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        try:

            serializer = GameSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                logger.error('Game already exists.')
                return Response(
                    {
                        'error': 'Game already exists.'
                    }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while creating game.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(tags=['Games'])
class GamesViewId(APIView):
    def get(self, request, id):
        try:

            game = Game.objects.get(id=id)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        
        except Game.DoesNotExist:

            logger.debug('Game with given ID not found.')
            raise GameIDNotFoundException('Game with given ID not found.')
        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while listing games.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, id):
        try:

            game = get_object_or_404(Game, id=id)

            serializer = GameSerializer(game, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while updating publisher.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, id):
        try:

            game = get_object_or_404(Game, id=id)
            game.delete()
            
            return Response(
                {'message': 'Game deleted successfully.'},
                status=status.HTTP_204_NO_CONTENT
            )
        
        except Exception as e:
            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while deleting game.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(tags=['Games'])
class GamesViewPublisher(APIView):
    def get(self, request, publisher):
        try:

            games = Game.objects.filter(publisher=publisher)
            
            if not games:
                logger.debug('No games found for the given publisher ID.')
                return Response('Error while fetching games.', status=status.HTTP_400_BAD_REQUEST)
            
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data)
        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while listing games.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
