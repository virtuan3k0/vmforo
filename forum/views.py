from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Section, Category, Thread, Post, PrivateMessage, PostLike
from django.contrib.auth import get_user_model
from .forms import PrivateMessageForm
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login


User = get_user_model()

class ForumMainView(ListView):
    model = Section
    template_name = 'forum/forum_main.html'
    context_object_name = 'sections'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.all()

        if self.request.user.is_authenticated:
            context['unread_count'] = PrivateMessage.objects.filter(recipients=self.request.user, read=False).count()
        else:
            context['unread_count'] = 0

        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'forum/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['threads'] = self.object.threads.all()

        if self.request.user.is_authenticated:
            context['unread_count'] = PrivateMessage.objects.filter(recipients=self.request.user, read=False).count()
        else:
            context['unread_count'] = 0

        return context

@method_decorator(csrf_exempt, name='dispatch')
class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.get_object()
        context['category'] = thread.category

        # Set default ordering
        order_posts_by = self.request.GET.get('order_posts_by', 'created_at')
        order_posts_direction = self.request.GET.get('order_posts_direction', 'asc')
        
        if order_posts_by == 'likes_count':
            order_posts_direction = self.request.GET.get('order_posts_direction', 'desc')  # Default to likes descending

        posts_ordering = f"{'-' if order_posts_direction == 'desc' else ''}{order_posts_by}"
        context['posts'] = self.object.posts.filter(parent__isnull=True).order_by(posts_ordering)
        context['can_edit'] = self.request.user == thread.author

        if self.request.user.is_authenticated:
            context['unread_count'] = PrivateMessage.objects.filter(recipients=self.request.user, read=False).count()
            liked_posts = PostLike.objects.filter(user=self.request.user, post__thread=thread).values_list('post_id', flat=True)
            context['liked_posts'] = set(liked_posts)
        else:
            context['unread_count'] = 0
            context['liked_posts'] = set()

        # Pass ordering options to the context
        context['order_posts_by'] = order_posts_by
        context['order_posts_direction'] = order_posts_direction

        # Add ordering context for each post's replies
        for post in context['posts']:
            post.order_replies_by = self.request.GET.get(f'order_replies_by_{post.id}', 'created_at')
            post.order_replies_direction = self.request.GET.get(f'order_replies_direction_{post.id}', 'asc')

        return context

    def post(self, request, *args, **kwargs):
        thread = self.get_object()
        if 'post_id' in request.POST:
            post = get_object_or_404(Post, id=request.POST['post_id'])

            if request.user != post.author:
                return JsonResponse({'error': 'You are not the author of this post.'}, status=403)

            action = request.POST.get('action')
            if action == 'edit_post':
                post.content = request.POST.get('content')
                post.mark_as_edited()
                return JsonResponse({
                    'content': post.content,
                    'edited_at': post.updated_at.strftime('%Y-%m-%d %H:%M')
                })
            elif action == 'delete_post':
                post.delete()
                return JsonResponse({'success': True})

            return JsonResponse({'error': 'Invalid action.'}, status=400)
        
        if request.user != thread.author:
            return JsonResponse({'error': 'You are not the author of this thread.'}, status=403)

        action = request.POST.get('action')
        if action == 'edit':
            new_content = request.POST.get('content')
            thread.content = new_content
            thread.save()
            return JsonResponse({
                'content': thread.content,
                'edited_at': thread.updated_at.strftime('%Y-%m-%d %H:%M')
            })
        elif action == 'delete':
            thread.delete()
            return JsonResponse({'redirect': reverse('forum:category_detail', kwargs={'slug': thread.category.slug})})

        return JsonResponse({'error': 'Invalid action.'}, status=400)

@login_required(login_url='/forum/')
@csrf_exempt
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        
        like, created = PostLike.objects.get_or_create(post=post, user=user)
        if not created:
            like.delete()
            post.likes_count = post.likes.count()
            post.save()
            return JsonResponse({'likes_count': post.likes_count, 'liked': False})
        else:
            post.likes_count = post.likes.count()
            post.save()
            return JsonResponse({'likes_count': post.likes_count, 'liked': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

class ThreadCreateView(CreateView):
    model = Thread
    template_name = 'forum/thread_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

class UserProfileView(DetailView):
    model = User
    template_name = 'forum/user_profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['unread_count'] = PrivateMessage.objects.filter(recipients=self.request.user, read=False).count()
        else:
            context['unread_count'] = 0

        return context

@login_required(login_url='/forum/')
def add_post(request, thread_slug):
    thread = get_object_or_404(Thread, slug=thread_slug)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        parent = Post.objects.get(id=parent_id) if parent_id else None
        Post.objects.create(thread=thread, author=request.user, content=content, parent=parent)
        return redirect(thread.get_absolute_url())

    return render(request, 'forum/thread_detail.html', {'thread': thread, 'category': thread.category})

def custom_login(request):
    next_url = request.GET.get('next', 'forum:forum_main')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if 'thread' in next_url:
                try:
                    slug = next_url.split('/thread/')[1].split('/')[0]
                    return redirect('forum:thread_detail', slug=slug)
                except (IndexError, ValueError):
                    return redirect('forum:forum_main')
            else:
                return redirect(next_url)
        else:
            return render(request, 'forum/login.html', {'error': 'Invalid credentials', 'next': next_url})

    return render(request, 'forum/login.html', {'next': next_url})

def custom_logout(request):
    logout(request)
    return redirect('forum:forum_main')

@login_required(login_url='/forum/')
def inbox(request):
    messages_received = PrivateMessage.objects.filter(recipients=request.user)
    messages_sent = PrivateMessage.objects.filter(sender=request.user)
    unread_messages = messages_received.filter(read=False)
    
    for message in messages_received:
        message.content = message.decrypt()
    
    for message in messages_sent:
        message.content = message.decrypt()
    
    return render(request, 'forum/inbox.html', {
        'messages_received': messages_received,
        'messages_sent': messages_sent,
        'unread_count': unread_messages.count(),
    })

@login_required(login_url='/forum/')
def message_detail(request, pk):
    message = get_object_or_404(PrivateMessage, pk=pk)

    if request.user not in message.recipients.all() and request.user != message.sender:
        return HttpResponse('Unauthorized', status=401)

    if request.user in message.recipients.all():
        message.mark_as_read()

    message.content = message.decrypt()

    unread_count = PrivateMessage.objects.filter(recipients=request.user, read=False).count()

    return render(request, 'forum/message_detail.html', {
        'message': message,
        'unread_count': unread_count,
    })

@login_required(login_url='/forum/')
def send_message(request, username=None):
    if username:
        recipient = get_object_or_404(User, username=username)
        initial_data = {'recipients': recipient.username}
    else:
        initial_data = {}

    quoted_message = request.GET.get('quote', '')

    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            form.instance.sender = request.user
            form.save()
            return redirect('forum:inbox')
    else:
        form = PrivateMessageForm(initial={**initial_data, 'content': quoted_message})

    unread_count = PrivateMessage.objects.filter(recipients=request.user, read=False).count()

    return render(request, 'forum/send_message.html', {
        'form': form,
        'username': username,
        'unread_count': unread_count,
    })

def check_key(request):
    key = os.environ.get('MESSAGE_ENCRYPTION_KEY')
    return HttpResponse(f"The encryption key is: {key}")
