from django.forms import ModelForm, Textarea
from blog.models import Article, BlogComment, User


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': Textarea(attrs={'id': 'blog_content_field', 'rows': 35})
        }


class BlogCommentForm(ModelForm):
    class Meta:
        model = BlogComment
        fields = '__all__'


class AccountRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
