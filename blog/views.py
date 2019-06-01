from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Article
from django.core.paginator import Paginator

# Create your views here.
# #测试代码
# def article_content(request):
#     article = Article.objects.all()[0]
#     title = article.title
#     lable = article.lable
#     brief_content = article.brief_content
#     content = article.content
#     article_id = article.article_id
#     publish_date = article.publish_date
#     return_str = 'title: %s, lable: %s, brief_content: %s, ' \
#                  'content: %s, article_id: %s, publish_date: %s' % (title,
#                                                                     lable,
#                                                                     brief_content,
#                                                                     content,
#                                                                     article_id,
#                                                                     publish_date)
#     return HttpResponse(return_str)

#索引模块，供urls.py调用
def get_index_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    all_article = Article.objects.all()
    top6_article_list = Article.objects.order_by('-publish_date')[:6]

    paginator = Paginator(all_article, 5)
    page_num = paginator.num_pages
    print('page num:', page_num)
    page_article_list = paginator.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'blog/index.html',
                  {
                      'article_list': page_article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page,
                      'top6_article_list': top6_article_list
                  }
                )
#一级boss模块，供urls.py调用
def get_iboss_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    all_article = Article.objects.filter(lable='iboss')
    top6_article_list = Article.objects.order_by('-publish_date')[:6]

    paginator = Paginator(all_article, 5)
    page_num = paginator.num_pages
    print('page num:', page_num)
    page_article_list = paginator.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'blog/iboss.html',
                  {
                      'article_list': page_article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page,
                      'top6_article_list': top6_article_list
                  }
                  )
#渠道模块，供urls.py调用
def get_channel_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    all_article = Article.objects.filter(lable='channel')
    top6_article_list = Article.objects.order_by('-publish_date')[:6]

    paginator = Paginator(all_article, 5)
    page_num = paginator.num_pages
    print('page num:', page_num)
    page_article_list = paginator.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'blog/channel.html',
                  {
                      'article_list': page_article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page,
                      'top6_article_list': top6_article_list
                  }
                  )
#短厅模块，供urls.py调用
def get_interface_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    all_article = Article.objects.filter(lable='interface')
    top6_article_list = Article.objects.order_by('-publish_date')[:6]

    paginator = Paginator(all_article, 5)
    page_num = paginator.num_pages
    print('page num:', page_num)
    page_article_list = paginator.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'blog/interface.html',
                  {
                      'article_list': page_article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page,
                      'top6_article_list': top6_article_list
                  }
                  )
#其他模块，供urls.py调用
def get_other_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    all_article = Article.objects.filter(lable='other')
    top6_article_list = Article.objects.order_by('-publish_date')[:6]

    paginator = Paginator(all_article, 5)
    page_num = paginator.num_pages
    print('page num:', page_num)
    page_article_list = paginator.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'blog/other.html',
                  {
                      'article_list': page_article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page,
                      'top6_article_list': top6_article_list
                  }
                  )
#文章详情，供urls.py调用
def get_detail_page(request, article_id):
    all_article = Article.objects.all()
    curr_article = None
    previous_index = 0
    next_index = 0
    previous_article = None
    next_article = None
    for index, article in enumerate(all_article):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_article) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1
        if article.article_id == article_id:
            curr_article = article
            previous_article = all_article[previous_index]
            try:
                next_article = all_article[next_index]
            except:
                next_article = all_article[index]
            break

    section_list = curr_article.content.split('\n')
    return render(request, 'blog/detail.html',
                  {
                      'curr_article': curr_article,
                      'section_list': section_list,
                      'previous_article': previous_article,
                      'next_article': next_article
                  }
                  )

# 根据文章标题模糊搜索
def search(request):
    keyStr = request.GET.get('searchkey')
    search_list = Article.objects.filter(title__icontains=keyStr)
    return render(request, 'blog/result.html',
                  {'search_list': search_list, }
                  )