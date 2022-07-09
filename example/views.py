from rest_framework import viewsets, generics, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404 # get_object_or_404 불러오기
from .models import Book                # 모델 불러오기
from .serializers import BookSerializer # 시리얼라이저 불러오기


class HelloAPI(APIView):
    def get(self, request):
        return Response('Hello World!')


class BooksAPI(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookAPI(APIView):
    def get(self, request, bid):
        book = get_object_or_404(Book, bid=bid)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BooksAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):            # GET 메소드 처리 함수 (전체 목록)
        return self.list(request, *args, **kwargs)      # mixins.ListModelMixin과 연결
    
    def post(self, request, *args, **kwargs):           # POST 메소드 처리 함수 (1권 등록)
        return self.create(request, *args, **kwargs)    # mixins.CreateModelMixin과 연결


class BookAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'
    # 우리는 Django 기본 모델 pk가 아닌 bid를 pk로 사용하고 있으니 lookup_field로 설정합니다.

    def get(self, request, *args, **kwargs):            # GET 메소드 처리 함수 (1권)
        return self.retrieve(request, *args, **kwargs)  # mixins.RetrieveModelMixin과 연결

    def put(self, request, *args, **kwargs):            # PUT 메소드 처리 함수 (1권 수정)
        return self.update(request, *args, **kwargs)    # mixins.UpdateModelMixin과 연결

    def delete(self, request, *args, **kwargs):         # DELETE 메소드 처리 함수 (1권 삭제)
        return self.destroy(request, *args, **kwargs)   # mixins.DestroyModelMixin과 연결


class BooksAPIGenerics(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookAPIGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer