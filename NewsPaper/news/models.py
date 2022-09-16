from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rank_author = models.IntegerField(default=0)

    def update_rating(self):
        sum_rating_author = self.post_set.all().aggregate(Sum('rating_post'))['rating_post__sum'] * 3
        sum_rating_comment = self.author_user.comment_set.all().aggregate(Sum('rating_comment'))['rating_comment__sum']
        sum_rating = self.post_set.all().aggregate(Sum('comment__rating_comment'))['comment__rating_comment__sum']
        self.rating_author = sum_rating_author + sum_rating_comment + sum_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    post = 'pt'
    news = 'nw'

    POSITIONS = [
        (post, 'Статья'),
        (news, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE,)
    post = models.CharField(max_length=30, choices=POSITIONS, default='news')
    data = models.DateTimeField(auto_now_add=True)
    head = models.CharField(max_length=255)
    text = models.TextField()
    rank = models.IntegerField(default=0)

    post_category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rank += 1
        self.save()

    def dislike(self):
        self.rank -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    com_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    com_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_com = models.TextField()
    com_data = models.DateField(auto_now_add=True)
    rank_com = models.IntegerField(default=0)

    def like(self):
        self.rank_com += 1
        self.save()

    def dislike(self):
        self.rank_com -= 1
        self.save()
