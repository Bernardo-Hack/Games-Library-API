import logging

from .models import Game, Publisher
from .serializers import GameSerializer, PublisherSerializer 

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from drf_spectacular.utils import extend_schema

# Create your views here.

logger = logging.getLogger('ViewsLog: ')

# TODO : Improve the logging, error handling, and response consistency.

# -=-=- Publisher Urls -=-=-


# Views for Publisher
@extend_schema(tags=['Publisher'])
class PublisherView(APIView):
    @extend_schema(summary='List all publishers')
    def get(self, request):
        try:

            publishers = Publisher.objects.all()

            if not publishers:
                logger.debug('No publishers found.')
                return Response([], status=status.HTTP_200_OK)

            serializer = PublisherSerializer(publishers, many=True)
            return Response(serializer.data)

        except Exception as e:

            logger.error(f"Error while listing publishers: {e}")
            return Response(
                {'status': 'error', 'message': 'Error while listing publishers', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

    @extend_schema(summary='Create a new publisher')
    def post(self, request):
        try:

            serializer = PublisherSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                logger.error(f'Publisher validation failed: {serializer.errors}')
                return Response({'error': 'Publisher already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:

            logger.error(f"Error while creating publisher: {e}")
            return Response(
                {'status': 'error', 'message': 'Error while creating publisher', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Views for Publisher with Id
@extend_schema(tags=['Publisher'])
class PublisherViewId(APIView):
    @extend_schema(summary='Get a publisher by ID')
    def get(self, request, id):
        try:

            publisher = Publisher.objects.get(id=id)
            serializer = PublisherSerializer(publisher)
            return Response(serializer.data)

        except Publisher.DoesNotExist:

            logger.debug(f'Publisher with given ID {id} not found.')
            return Response({'detail': f'Publisher with given ID({id}) not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:

            logger.error(f"Error while fetching publisher with ID {id}: {e}")
            return Response(
                {
                    'status': 'error', 
                    'message': 
                    'Error while fetching publisher', 'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    @extend_schema(summary='Update a publisher by ID')
    def put(self, request, id):
        try:

            publisher = Publisher.objects.get(id=id)
            serializer = PublisherSerializer(publisher, data=request.data, partial=True)
        
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        
            else:
                logger.error('Error while updating publisher.')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Publisher.DoesNotExist:

            logger.error(f'Publisher with given ID({id}) not found.')
            return Response({'detail': f'Publisher with given ID({id}) not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error('Error while updating publisher.')
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while updating publisher.',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @extend_schema(summary='Delete a publisher by ID')
    def delete(self, request, id):
        try:

            publisher = Publisher.objects.get(id=id)
            publisher.delete()
            
            return Response(
                {'message': 'Publisher deleted successfully.'},
                status=status.HTTP_204_NO_CONTENT
            )
        
        except Publisher.DoesNotExist:

            logger.error(f'Publisher with given ID({id}) not found.')
            return Response({'detail': f'Publisher with given ID({id}) not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while deleting publisher.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(tags=['Publisher'])
# View for Publisher with Location
class PublisherViewLocation(APIView):
    @extend_schema(summary='Get a publisher by Location')
    def get(self, request, location):
        try:

            publishers = Publisher.objects.filter(location=location)

            if not publishers:
                raise(Publisher.DoesNotExist)

            serializer = PublisherSerializer(publishers, many=True)
            return Response(serializer.data)
        
        except Publisher.DoesNotExist:

            logger.debug(f'Publisher with given Location({location}) not found.')
            return Response({'detail': f'Publisher with given Location({location}) not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while listing publishers.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(tags=['Publisher'])
# View for Publisher with Location
class PublisherViewGames(APIView):
    @extend_schema(summary='Get games from a publisher by ID')
    def get(self, request, id):
        try:

            publisher = Publisher.objects.get(id=id)
            games = publisher.games.all()
            serializer = GameSerializer(games, many=True)
            return Response(serializer.data)
        
        except Publisher.DoesNotExist:

            logger.debug(f'Publisher with given ID({id}) not found.')
            return Response({'detail': f'Publisher with given ID({id}) not found.'}, status=status.HTTP_404_NOT_FOUND)

        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while listing publishers.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

# -=-=- Games Urls -=-=-

# Views for Game
@extend_schema(tags=['Games'])
class GameView(APIView):
    @extend_schema(summary='List all games')
    def get(self, request):
        try:

            games = Game.objects.all()
            
            if not games:
                logger.debug('No games found.')
                return Response([], status=status.HTTP_200_OK)
            
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
    

    @extend_schema(summary='Create a new game')
    def post(self, request):
        try:

            serializer = GameSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            logger.error(f'Game validation failed: {serializer.errors}')
            return Response({'error': 'Game already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while creating game.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Views for Game with Id
@extend_schema(tags=['Games'])
class GameViewId(APIView):
    @extend_schema(summary='Get a game by ID')
    def get(self, request, id):
        try:

            game = Game.objects.get(id=id)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        
        except Game.DoesNotExist:

            logger.debug(f'Game with given ID ({id}) not found.')
            return Response({'detail': f'Game with given ID({id}) not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while listing games.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

    @extend_schema(summary='Update a game by ID')
    def put(self, request, id):
        try:

            game = Game.objects.get(id=id)
            serializer = GameSerializer(game, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                logger.error('Error while updating game.')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Game.DoesNotExist:

            logger.error(f'Game with given ID({id}) not found.')
            return Response({'detail': f'Game with given ID({id}) not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while updating game.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

    @extend_schema(summary='Delete a game by ID')
    def delete(self, request, id):
        try:

            game = Game.objects.get(id=id)
            game.delete()
            
            return Response(
                {'message': 'Game deleted successfully.'},
                status=status.HTTP_204_NO_CONTENT
            )
        
        except Game.DoesNotExist:

            logger.error(f'Game with given ID({id}) not found.')
            return Response({'detail': f'Game with given ID({id}) not found.'}, status=status.HTTP_404_NOT_FOUND)
        
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
# Views for Game with Genre
class GameViewGenre(APIView):
    @extend_schema(summary='Get games by Genre')
    def get(self, request, genre):
        try:

            games = Game.objects.filter(genre=genre)

            if not games:
                raise(Game.DoesNotExist)

            serializer = GameSerializer(games, many=True)
            return Response(serializer.data)
        
        except Game.DoesNotExist:

            logger.debug(f'No games found with given genre({genre}).')
            return Response({'detail': f'No games found with given genre({genre}).'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:

            logger.error(e)
            return Response(
                {
                    'status': 'error',
                    'message': 'Error while listing publishers.',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
