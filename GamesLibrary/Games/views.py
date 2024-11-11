import logging

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .models import Game, Publisher
from .serializers import GameSerializer, PublisherSerializer 

from .exceptions import PublisherIDNotFoundException, GameIDNotFoundException
from .validation import validate_data

# Create your views here.

logger = logging.getLogger('Test: ')

# <=-=> Publisher Urls <=-=>


@extend_schema(methods=['GET'], tags=['Publisher'])
@api_view(['GET'])
def list_publishers(request):
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


@extend_schema(methods=['GET'], tags=['Publisher'])
@api_view(['GET'])
def get_publisher(request, id):
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


@extend_schema(methods=['POST'], tags=['Publisher'])
@api_view(['POST'])
def create_publisher(request):
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
    

@extend_schema(methods=['PUT'], tags=['Publisher'])
@api_view(['PUT'])
def update_publisher(request, id):
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
    

@extend_schema(methods=['DELETE'], tags=['Publisher'])
@api_view(['DELETE'])
def delete_publisher(request, id):
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


# <=-=> Games Urls <=-=>


@extend_schema(methods=['GET'], tags=['Publisher'])
@api_view(['GET'])
def list_games(request):
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


@extend_schema(methods=['GET'], tags=['Game'])
@api_view(['GET'])
def get_game(request, id):
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


@extend_schema(methods=['GET'], tags=['Game'])
@api_view(['GET'])
def get_games_by_publisher(request, id):
    try:
        
        games = Game.objects.filter(publisher=id)

        if not games.exists():

            logger.debug('No games found for the given publisher ID.')

            return Response(
                {'error': 'No games found for the given publisher ID.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    except Exception as e:

        logger.error(e)
        return Response(
            {
                'status': 'error',
                'message': 'Error while listing games for publisher.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(methods=['POST'], tags=['Game'])
@api_view(['POST'])
def create_game(request):
    try:

        serializer = GameSerializer (data=request.data)

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


@extend_schema(methods=['PUT'], tags=['Game'])
@api_view(['PUT'])
def update_game(request, id):
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


@extend_schema(methods=['DELETE'], tags=['Game'])
@api_view(['DELETE'])
def delete_game(request, id):
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
    