from ..models import WatchList, StreamPlatform, Review   
from .serializers import WatchlistSerializer, StreamPlatformSerializer, ReviewSerializer
from ..api.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly
from .throttling import ReviewListThrottle, ReviewCreateThrottle
from .pagination import WatchlistPagination, WatchlistLimitOffsetPagination, WatchlistCursorPagination


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
# from rest_framework.decorators import api_view  
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework import filters

from django.core.exceptions import ObjectDoesNotExist


class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):  
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    #In this we are using query params that is ?username=niharsh 
    # and in above we are using url params that is /user/niharsh/
    def get_queryset(self):
        username=self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes=[IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user=self.request.user
        review_queryset=Review.objects.filter(watchlist=watchlist,review_user=review_user)

        if(review_queryset.exists()):
            raise ValidationError("you already review this movie!")
        
        if(watchlist.number_rating==0):
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating+serializer.validated_data['rating'])/2
        watchlist.number_rating+=1
        watchlist.save()

        serializer.save(watchlist=watchlist,review_user=review_user)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    filter_backends=[DjangoFilterBackend]   #review/?active=true&review_user__username=niharsh
    filterset_fields=['review_user__username','active']

    def get_queryset(self):  
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
        
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


class StreamPlatformAV(APIView):
    permission_classes=[IsAdminOrReadOnly]
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        



class StreamPlatformDetailAV(APIView):
    permission_classes=[IsAdminOrReadOnly]
    def get(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
  
    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors)
        
    
    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status="204")
    
class watchlistGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchlistSerializer
    filter_backends=[filters.OrderingFilter]
    ordering_fields=['avg_rating'] #to sort by avg_rating use ?ordering=avg_rating or ?ordering=-avg_rating for descending order
    pagination_class=WatchlistCursorPagination


    
class WatchlistAV(APIView):
    permission_classes=[IsAdminOrReadOnly]
    def get(self, request):
        watchlist = WatchList.objects.all()
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class WatchDetailAV(APIView):
    permission_classes=[IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
            serializer = WatchlistSerializer(watchlist)
            return Response(serializer.data) 
        except ObjectDoesNotExist:
            return Response({"detail": "Watchlist not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        watchlist = WatchList.objects.get(pk=pk)
        serializer = WatchlistSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors)
        
    
    def delete(self,request,pk):
       watchlist = WatchList.objects.get(pk=pk)
       watchlist.delete()
       return Response(status="204")
     



# def movie_list(request): 
#     movies = Movie.objects.all()
#     movie_data = {
#         'movies': list(movies.values())
#     }
#     return JsonResponse(movie_data, safe=False)


# def movie_detail(request, pk):
#     try:
#        movie = Movie.objects.get(pk=pk)
#        movie_data = {
#             "name": movie.name,
#             "description": movie.description,
#             "release_year": movie.release_year,
#             "rating": movie.rating
#         }
#     except Movie.DoesNotExist:
#         movie_data = {"error": "Movie not found"}   
#     return JsonResponse(movie_data)

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#     #return JsonResponse(serializer.data, safe=False)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             # Normally, you would save the data to the database here.
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)



# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#             serializer = MovieSerializer(movie)
#         except Movie.DoesNotExist:
#             return Response({"error": "Movie not found"}, status=404)
#         #return JsonResponse(serializer.data) 
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({"error": "Movie not found"}, status=404)
        
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
    
#     if request.method == 'DELETE':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({"error": "Movie not found"}, status=404)
        
#         movie.delete()
#         return Response(status=204)




# class ReviewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin , generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class ReviewtList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

