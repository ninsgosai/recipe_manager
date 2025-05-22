from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from strawberry.django.views import GraphQLView
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication

# Configure logging
logger = logging.getLogger(__name__)

# Create your views here.

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

@method_decorator(csrf_exempt, name='dispatch')
class AuthenticatedGraphQLView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.warning(f"Authentication failed: Missing or invalid Authorization header")
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        token = auth_header.split(' ')[1]
        try:
            validated = JWTAuthentication().authenticate(request)
            if validated is not None:
                user, _ = validated
                request.user = user
            else:
                logger.error("Invalid token: Could not authenticate user")
                return JsonResponse({'error': 'Invalid token'}, status=401)
        except Exception as e:
            logger.error(f"Invalid token: {str(e)}")
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        response = super().dispatch(request, *args, **kwargs)
        
        # Log the response
        try:
            if hasattr(response, 'content'):
                response_data = json.loads(response.content)
                logger.info(f"GraphQL Response: {json.dumps(response_data, indent=2)}")
        except Exception as e:
            logger.error(f"Error logging response: {str(e)}")
        
        return response
