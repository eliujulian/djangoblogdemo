from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from blog.models import Article, BlogComment
from blog.forms import ArticleForm, BlogCommentForm
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from django.shortcuts import get_object_or_404, reverse


class BlogView(ListView):
    model = Article
    template_name = "blog/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['model'] = self.model
        return context

    def get_queryset(self):
        return Article.objects.filter(publish=True).order_by('-date')


class ArticleListView(UserPassesTestMixin, ListView):
    model = Article
    template_name = "blog/article_list.html"

    def get_queryset(self):
        return Article.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['model'] = self.model
        return context

    def test_func(self):
        return self.request.user.is_superuser


class ArticleCreateView(UserPassesTestMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog/blog_create.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.timestamp_created = timezone.now()
        form.instance.timestamp_changed = timezone.now()
        form.instance.id_slug = self.model.get_id_slug(10)
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        for field in self.form_class().fields:
            if self.request.GET.get(field, False):
                initial[field] = self.request.GET.get(field)
        return initial

    def test_func(self):
        return self.request.user.is_superuser  # Only superuser (== blog owner can create articles)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['url'] = self.model.get_create_url()
        return context


class ArticleDetailView(UserPassesTestMixin, DetailView):
    model = Article
    slug_field = 'id_slug'
    template_name = "blog/article-detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id_slug=self.kwargs['slug'])

    def test_func(self):  # only superuser can see not published articles
        if self.get_object().publish:
            return True
        else:
            return self.request.user.is_superuser  # Only superuser can see articles that are not yet published.


class ArticleUpdateView(UserPassesTestMixin, UpdateView):
    model = Article
    slug_field = 'id_slug'
    form_class = ArticleForm
    template_name = "blog/blog_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['url'] = self.model.get_update_url(self.object)
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id_slug=self.kwargs['slug'])

    def test_func(self):
        return self.request.user.is_superuser  # Only superuser can change articles.


class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    model = Article
    slug_field = 'id_slug'
    template_name = "blog/confirm_delete.html"

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id_slug=self.kwargs['slug'])

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse("article-list")


class BlogCommentCreateView(CreateView):
    model = BlogComment
    form_class = BlogCommentForm
    http_method_names = ['post']

    def form_valid(self, form):
        article = Article.objects.get(id_slug=self.kwargs['slug'])
        form.instance.created_by = self.request.user
        form.instance.timestamp_created = timezone.now()
        form.instance.timestamp_changed = timezone.now()
        form.instance.id_slug = self.model.get_id_slug(10)
        form.instance.article = article
        form.instance.counter = article.blogcomment_set.all().count() + 1
        return super().form_valid(form)


class BlogCommentUpdateView(UserPassesTestMixin, UpdateView):
    model = BlogComment
    slug_field = 'id_slug'
    form_class = BlogCommentForm
    template_name = 'blog/comment_update.html'

    def test_func(self):
        # superuser can change comments for compliance purposes
        return self.request.user.is_superuser


class ImprintView(TemplateView):
    template_name = 'blog/imprint.html'


class PrivacyView(TemplateView):
    template_name = 'blog/privacy.html'


class ContactView(TemplateView):
    template_name = 'blog/contact.html'
