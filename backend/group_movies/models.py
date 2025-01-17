from django.db import models
from django.conf import settings

# 그룹
class Group(models.Model):
    include_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='include_groups')
    group_name = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    category = models.CharField(max_length=10)
    group_img = models.ImageField(blank=True, upload_to='group_images/', default='default/group.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 영화
class Movie(models.Model):
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    release_date = models.DateField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=255, null=True)
    backdrop_path = models.CharField(max_length=255, null=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    runtime = models.IntegerField()
    genres = models.JSONField()  # 또는 ManyToManyField
    production_countries = models.JSONField()
    director = models.CharField(max_length=255, null=True)
    cast = models.JSONField()
    trailer = models.CharField(max_length=255, null=True)


# 그룹에서 본 영화
class GroupMovie(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='watched_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watched_by_groups')
    watched_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

# 타임라인
class TimeLine(models.Model):
    group_movie = models.ForeignKey(GroupMovie, on_delete=models.CASCADE, related_name='timeline')
    time = models.TimeField()
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['time']

# 한줄평
class Review(models.Model):
    group_movie = models.ForeignKey(GroupMovie, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='review')
    review = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 게시글
class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='article')
    group_movie = models.ForeignKey(GroupMovie, on_delete=models.CASCADE, related_name='article')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 갤러리(여러장 가능)
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    group_movie = models.ForeignKey(GroupMovie, on_delete=models.CASCADE, related_name='article_img')
    image = models.ImageField(upload_to='article_imges/')


# 좋아요한 영화 정보
class LikeMovie(models.Model):
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    poster_path = models.CharField(max_length=200, null=True, blank=True)


# 게시글의 댓글
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name='comment')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,  related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)