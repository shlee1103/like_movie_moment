from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer, TokenSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from group_movies.serializers import LikeMovieSerializer, ArticleSerializer


# 회원가입 시 DB에 추가된 필드 저장 커스텀
class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True, max_length=100)
    profile_img = serializers.ImageField(required=False)

    def custom_signup(self, request, user):
        user.name = self.validated_data['name']
        # profile_img가 제공되지 않으면 모델의 default 값이 자동으로 사용됨
        if 'profile_img' in self.validated_data:
            user.profile_img = self.validated_data['profile_img']
        user.save()
        return user


# 유저 기본 정보
class UserLoginSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'name', 'email', 'profile_img')

# 로그인 시 token 외 유저 기본 정보 제공 커스텀
class CustomTokenSerializer(TokenSerializer):
    user = UserLoginSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + ('user',)

# 프로필 이미지 수정
class UserImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('profile_img',)

# 프로필 조회
class CustomUserDetailsSerializer(UserDetailsSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True)
    is_following = serializers.SerializerMethodField() # request 객체가 필요해서 method field 사용
    liked_movies = LikeMovieSerializer(source='liked_movie', many=True, read_only=True)  
    liked_movies_count = serializers.IntegerField(source='liked_movie.count', read_only=True)  
    articles = ArticleSerializer(source='article', many=True, read_only=True)  # related_name으로 연결된 게시글들
    articles_count = serializers.IntegerField(source='article.count', read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        model = get_user_model()
        fields = (
            'id', 'username', 'email', 'name', 'profile_img',
            'followers_count', 'followings_count', 'is_following',
            'liked_movies', 'liked_movies_count',
            'articles', 'articles_count'
        )
        read_only_fields = ('email', 'username')
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        return obj.followers.filter(pk=request.user.pk).exists()

  