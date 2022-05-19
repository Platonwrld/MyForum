from tabnanny import verbose
from unicodedata import category
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.urls import reverse


User = get_user_model()


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(blank=True, max_length=40)
    slug = models.SlugField(unique=True, blank=True, max_length=400)
    profile_pic = ResizedImageField(size=[50, 80], quality=100, upload_to='authors', default=None, null=True)
    bio = HTMLField()   #tinymce
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        """ Метод для сохранения title как slug, если нету slug """
        if not self.slug:
            self.slug = slugify(self.fullname)
        super(Author, self).save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, max_length=400)
    description = models.TextField(max_length=250, default='description')

    class Meta:
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """ Метод для сохранения title как slug, если нету slug """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('posts_page', kwargs={'slug': self.slug})

    @property
    def get_numbers_posts(self):
        return Post.objects.filter(cat=self).count()

    @property
    def get_last_post(self):
        return Post.objects.filter(cat=self).latest('date')


""" Replay on commentary """
class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.content[:100]

    class Meta:
        verbose_name = 'replies'


""" Commentary """
class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True )

    def __str__(self):
        return self.content[:100]


class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(unique=True, blank=True, max_length=400)
    cat = models.ManyToManyField(Category)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = HTMLField()
    date = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    tags = TaggableManager()    # use taggs
    comments = models.ManyToManyField(Comment, blank=True)
    closed = models.BooleanField(default=False)
    state = models.CharField(max_length=40, default='zero')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """ Метод для сохранения title как slug, если нету slug """
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail_page', kwargs={'slug': self.slug})

    @property
    def get_numbers_comments(self): 
        return self.comments.count()

    @property
    def last_replay(self): 
        return self.comments.latest('date')

    @property
    def last_replay(self): 
        return self.comments.latest('date')


