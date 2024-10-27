from django.shortcuts import render, redirect, get_object_or_404
from forum.models import Post, Comment
from forum.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def forum_view(request):
    post_entries = Post.objects.all()
    context = {
        'post_entries': post_entries,
    }
    return render(request, "forum.html", context)

@login_required(login_url='/login')
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('forum:forum_view')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required(login_url='/login')
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comment_set.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('forum:post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    
    return render(request, 'post_detail.html', context)

@login_required(login_url='/login')
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('forum:forum_view')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required(login_url='/login')
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('forum:forum_view')

@login_required(login_url='/login')
def edit_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    post = comment.post
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('forum:post_detail', post_id=post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form, 'post': post})

@login_required(login_url='/login')
def delete_comment_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    post_id = comment.post.id
    comment.delete()
    return redirect('forum:post_detail', post_id=post_id)
