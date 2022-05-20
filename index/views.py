from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from index.models import Manga, Slider, Viewer
from next_prev import next_or_prev_in_order
from index.utils import get_client_ip
from django.db.models import Count, Q
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

sort_queries = {
    "most_popular": "-views",
    "trending_now": "-daily_views",
    "popular_manga": "-weekly_views",
    "recently_added": "-created_at"
}


def redirect_to_language(request):
    language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if Manga.objects.filter(language=language).exists():
        return redirect(language)
    else:
        return redirect('/en/')


def index(request, language):
    day_ago = timezone.now() - timezone.timedelta(days=1)
    week_ago = timezone.now() - timezone.timedelta(days=7)
    manga_query = Manga.objects.filter(language=language).annotate(
        views=Count('viewer__chapter'),
        daily_views=Count('viewer__chapter', filter=Q(viewer__created_at__gte=day_ago)),
        weekly_views=Count('viewer__chapter', filter=Q(viewer__created_at__gte=week_ago))
    )
    return render(
        request, 'index.html',
        context={
            'meta_title': 'MangaRed - Read Manga Online For Free',
            'meta_description': 'Reading manga free with latest chapter, '
                                'free with high-quality pages, read manga on mobile, '
                                'read comic online for free.',
            'current_page': 'index',
            'language': language,
            'most_popular': manga_query.order_by('-views')[:9],
            'trending_now': manga_query.order_by('-daily_views')[:9],
            'popular_manga': manga_query.order_by('-weekly_views')[:9],
            'recently_added': manga_query.order_by('-created_at')[:9],
            'sliders': get_list_or_404(Slider, language=language)
        })


def manga(request, language):
    day_ago = timezone.now() - timezone.timedelta(days=1)
    week_ago = timezone.now() - timezone.timedelta(days=7)
    manga_obj = Manga.objects.annotate(
        views=Count('viewer__chapter'),
        daily_views=Count('viewer__chapter', filter=Q(viewer__created_at__gte=day_ago)),
        weekly_views=Count('viewer__chapter', filter=Q(viewer__created_at__gte=week_ago))
    )
    search = request.GET.get('search')
    queries = {'language': language}
    if search is not None:
        queries['title__icontains'] = search
    category = request.GET.get('category')
    if category is not None:
        queries['categories__overlap'] = [category]
    most_popular = manga_obj.order_by('-views')[:9]
    manga_obj = manga_obj.filter(**queries)
    sort_by = request.GET.get('sort_by')
    sort_by_query = sort_queries.get(sort_by)
    if sort_by is not None:
        manga_obj = manga_obj.order_by(sort_by_query)
    paginator = Paginator(manga_obj, 18)
    page = request.GET.get('page', 1)
    try:
        manga_elements = paginator.page(page)
    except PageNotAnInteger:
        manga_elements = paginator.page(1)
    except EmptyPage:
        manga_elements = paginator.page(paginator.num_pages)
    title = f'Search by "{search}"' if search else "Manga"
    return render(
        request, 'manga.html',
        context={
            'meta_title': title,
            'meta_description': f'Search for {title}',
            'current_page': sort_by,
            'language': language,
            'manga_elements': manga_elements,
            'most_popular': most_popular,
            'title': title
        })


def manga_details(request, language, manga_slug):
    manga_obj = get_object_or_404(Manga, language=language, slug=manga_slug)
    chapters_obj = manga_obj.chapters.values('title', 'slug').order_by('pk').annotate(views=Count('viewer__chapter'))
    return render(
        request, 'manga_details.html',
        context={
            'meta_title': f'{manga_obj.title} - MangaRed',
            'meta_description': f'{manga_obj.description[:150]}...',
            'language': language,
            'manga': manga_obj,
            'chapters': chapters_obj,
            'total_views': sum(chapter['views'] for chapter in chapters_obj)
        })


def manga_chapter(request, language, manga_slug, chapter_slug):
    manga_obj = get_object_or_404(Manga, language=language, slug=manga_slug)
    chapter_obj = manga_obj.chapters.get(slug=chapter_slug)
    ip = get_client_ip(request)
    Viewer.objects.get_or_create(ip=ip, manga=manga_obj, chapter=chapter_obj)
    chapters_obj = manga_obj.chapters.all()
    return render(
        request, 'manga_chapter.html',
        context={
            'meta_title': f'{manga_obj.title} - {chapter_obj.title} - MangaRed',
            'meta_description': f'{manga_obj.description[:150]}...',
            'language': language,
            'manga': manga_obj,
            'chapter': chapter_obj,
            'next_chapter': next_or_prev_in_order(chapter_obj, qs=chapters_obj, prev=False),
            'prev_chapter': next_or_prev_in_order(chapter_obj, qs=chapters_obj, prev=True)
        })
