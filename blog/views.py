from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from django.db.models import Q # Import Q object for complex lookups

def post_list(request, category_slug=None):
    category = None
    # Start with all published posts
    object_list = Post.objects.filter(status='published').order_by('-publish')

    # Handle category filtering (existing code)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        object_list = object_list.filter(category=category) # Filter on the already published list

    # --- ADD THIS SECTION FOR SEARCH ---
    query = request.GET.get('q') # Get the search query from the URL parameter 'q'
    if query:
        object_list = object_list.filter(
            Q(title__icontains=query) | # Search in title (case-insensitive)
            Q(body__icontains=query)    # OR search in body (case-insensitive)
        )
    # --- END ADDITION ---

    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Pass the query back to the template to persist it in the search bar
    return render(request, 'blog/post/list.html', {
        'page': page,
        'posts': posts,
        'category': category,
        'query': query # Pass the search query to the template
    })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            # Reset the form for a new comment
            comment_form = CommentForm()
        else:
            # If form is not valid, pass the form with errors back to template
            pass
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })