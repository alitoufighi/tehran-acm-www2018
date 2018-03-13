from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView

from account.models import Notification
from blog.forms import NewCommentForm, AddPostForm
from blog.forms import NewCommentForm, AddPostForm, AddTagToPostForm
from blog.models import Post, Comment, UserLikesPost, UserDislikesPost, Tag
from blog.models import Post, Comment, UserLikesPost, UserDislikesPost, ReportPost


def show_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    add_tag_form = AddTagToPostForm()
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.post = post
        comment.text = request.POST.get('text')
        comment.save()

        text = comment.text
        mentions = list()
        words = str(text).split()
        for word in words:
            if word[0] == '@':
                if User.objects.filter(username=word[1:]).exists():
                    user = User.objects.filter(username=word[1:]).first()
                    notif = Notification()
                    notif.text = 'شما در پست جدیدی منشن شده اید' + \
                                 '<a class="ui animated small right floated button" href="' + reverse('blog:show_post',
                                                                                                      args=[
                                                                                                          post_id]) + '">' \
                                 + '<div class="visible content">' + 'مشاهده پست' + '</div>' \
                                 + '<div class="hidden content"> \
                                    <i class="right arrow icon"></i> \
                                    </div>' + '</a>'
                    notif.user = user
                    notif.seen = False
                    notif.save()

    comments = Comment.objects.filter(post=post)
    return render(request, 'blog/single_post.html', {
        'post': post,
        'comments': comments,
        'new_comment_form': NewCommentForm(),
        'add_tag_form': add_tag_form
    })


class LikeView(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        id = self.kwargs['post_id']

        if not UserLikesPost.objects.filter(post_id=id, user=self.request.user).exists():
            l = UserLikesPost(user=self.request.user)
            l.post_id = id
            l.save()
        return HttpResponseRedirect(reverse('blog:show_post', args=[id]))


class DislikeView(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        id = self.kwargs['post_id']

        if not UserDislikesPost.objects.filter(post_id=id, user=self.request.user).exists():
            l = UserDislikesPost(user=self.request.user)
            l.post_id = id
            l.save()
        return HttpResponseRedirect(reverse('blog:show_post', args=[id]))


class DeleteView(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        id = self.kwargs['post_id']

        try:
            p = Post.objects.get(id=id)
            if p.author == self.request.user:
                p.delete()
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse('account:my_profile'))


class ReportView(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        id = self.kwargs['post_id']
        try:
            r = ReportPost(user=self.request.user)
            r.post_id = id
            r.save()
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse('blog:show_post', args=[id]))


class AddPostView(FormView):
    template_name = 'blog/add_post.html'
    form_class = AddPostForm
    success_url = reverse_lazy('account:my_profile')

    def get_success_url(self):
        if self.anon:
            return reverse_lazy('blog:show_post', args=[self.post_id])
        else:
            return reverse_lazy('account:my_profile')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()

        self.post_id = post.id
        self.anon = post.anon

        return super(FormView, self).form_valid(form)


class AddTagView(View, LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        id = self.kwargs['post_id']
        try:
            t = Tag.objects.get(id=self.request.POST.get('tag'))
            p = Post.objects.get(id=id)
            p.tags.add(t)
            p.save()
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse('blog:show_post', args=[id]))
