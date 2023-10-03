from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Post
from .serializers import UserSerializer, PostSerializer, UserLoginSerializer, PostDetailSerializer
from rest_framework import permissions

class UserRegistrationView(APIView):
    """
    API View for user registration.

    This view allows users to register by providing their information through a POST request.
    Upon successful registration, a new User object is created and returned as a JSON response.

    Usage:
    - To register a new user, send a POST request to this view with the required user data.

    Example:
    ```
    POST /api/register/
    {
        "username": "newuser",
        "password": "mypassword",
        "email": "newuser@example.com"
    }
    ```

    Response:
    ```
    HTTP 201 Created
    {
        "id": 1,
        "username": "newuser",
        "email": "newuser@example.com"
    }
    ```
    """
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
    API view for user login functionality.

    Handles the POST request to log in a user and returns a response with the appropriate status and data.
    """

    serializer_class = UserLoginSerializer

    def post(self, request):
        """
        Handles the POST request to log in a user.

        Args:
            request (Request): The request object containing the user login data.

        Returns:
            Response: The response object with the appropriate status and data.
        """
        try:
            data = request.data
            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                return Response(
                    status=status.HTTP_200_OK,
                    data={'message': "Successfully logged in", "data": serializer.data},
                )
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'msg': 'Invalid data provided', 'errors': serializer.errors},
                )

        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={'msg': 'Internal server error'},
            )

class PostListView(APIView):
    """
    A view that allows users to list and create posts.

    Example Usage:
    - To list all posts: GET /posts/
    - To create a new post: POST /posts/
        {
          "title": "New Post",
          "content": "This is the content of the new post"
        }
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostCreateView(APIView):
    """
    A view that allows users to list and create posts.

    Example Usage:
    - To list all posts: GET /posts/
    - To create a new post: POST /posts/
        {
          "title": "New Post",
          "content": "This is the content of the new post"
        }
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """
    A view that allows users to retrieve, update, and delete a specific post.

    Example Usage:
    - To retrieve a specific post: GET /posts/<post_id>/
    - To update a specific post: PUT /posts/<post_id>/
        {
          "title": "Updated Title",
          "content": "Updated content"
        }
    - To partially update a specific post: PATCH /posts/<post_id>/
        {
          "title": "Updated Title"
        }
    - To delete a specific post: DELETE /posts/<post_id>/
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if post.author != request.user:
            return Response(
                {"detail": "You do not have permission to update this post."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PostDetailSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if post.author != request.user:
            return Response(
                {"detail": "You do not have permission to update this post."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PostDetailSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if post.author != request.user:
            return Response(
                {"detail": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)