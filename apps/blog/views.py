from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Article
from django.core.paginator import Paginator
# from django.shortcuts import render_to_response
from django.conf import settings

import json
from random import randrange
from rest_framework.views import APIView
from pyecharts.charts import Bar, Pie, Line, Grid
from pyecharts import options as opts
from pyecharts.faker import Faker, Collector
from pyecharts.globals import ThemeType


# Create your views here.

class json_response(object):
    def response_as_json(data):
        json_str = json.dumps(data)
        response = HttpResponse(
            json_str,
            content_type="application/json",
        )
        response["Access-Control-Allow-Origin"] = "*"
        return response

    def json_response(data, code=200):
        data = {
            "code": code,
            "msg": "success",
            "data": data,
        }
        return json_response.response_as_json(data)

    def json_error(error_string="error", code=500, **kwargs):
        data = {
            "code": code,
            "msg": error_string,
            "data": {}
        }
        data.update(kwargs)
        return json_response.response_as_json(data)

    JsonResponse = json_response
    JsonError = json_error


def bardata(request):
    bar = (
        Bar()
            .add_xaxis(["T模块", "R模块", "S模块"])
            .add_yaxis("成功", [randrange(0, 100) for _ in range(3)])
            .add_yaxis("失败", [randrange(0, 100) for _ in range(3)])
            # .set_colors(["#343a40","#dc3545"])
            .set_global_opts(title_opts=opts.TitleOpts(title="各模块交易情况"))
            .dump_options_with_quotes()
    )
    return json_response.JsonResponse(json.loads(bar))


class BarView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/iboss_auto/ibossauto_bar.html')


def piedata(request):
    x_data = ["成功", "失败"]
    y_data = [214, 12]
    # 饼图用的数据格式是[(key1,value1),(key2,value2)]，所以先使用 zip函数将二者进行组合
    data_pair = [list(z) for z in zip(x_data, y_data)]
    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
            # .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
            .add(series_name="详情", data_pair=data_pair)
            .set_colors(["green", "red", "orange"])
            # .init_opts=opts.InitOpts(theme=ThemeType.MACARONS)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="自动化执行结果", subtitle="用例总数：227", item_gap=20,
                                      subtitle_textstyle_opts=opts.TextStyleOpts(font_style="normal", font_size="14",
                                                                                 color="tea", font_weight="bold")),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="78%", orient="vertical"), )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%", ),
                             tooltip_opts=opts.TooltipOpts(trigger='item', formatter="{a} <br/> {b}:{c} ({d}%)"), )
            .dump_options_with_quotes()
    )
    return json_response.JsonResponse(json.loads(pie))

# 访问试图
class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/iboss_auto/ibossauto.html')
class CQView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/iboss_auto/ibossauto_CQ.html')
class SDView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/iboss_auto/ibossauto_SD.html')
class HUBView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/iboss_auto/ibossauto_HUB.html')
class HEBView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/iboss_auto/ibossauto_HEB.html')


# 索引模块，供urls.py调用
def get_index_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    all_article = Article.objects.get_queryset().order_by('article_id')
    top6_article_list = Article.objects.order_by('-publish_date')[:6]

    paginator = Paginator(all_article, 5)  # 5篇文章一页
    page_num = paginator.num_pages
    print('page num:', page_num)
    page_article_list = paginator.page(page)
    if page_num <= 1:
        article_list = all_article  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取文章页码，默认第一页
        article_list = page_article_list  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第一页页码后是否需要省略号
        right_has_more = False  # 标示最后一页页码后是否需要省略号
        # 标示是否需要显示第 1 页的页码号
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False
        last = False  # 标示是否需要显示最后一页的页码号
        total_pages = page_num
        page_range = paginator.page_range
        if page == 1:
            right = page_range[page:page + 2]  # 获取右边连续号码页
            print(total_pages)
            if right[-1] < total_pages - 1:
                # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示
                right_has_more = True
            if right[-1] < total_pages:
                # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:
            left = page_range[(page - 5) if (page - 5) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
                left_has_more = True
            if left[0] > 1:
                # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 5) if (page - 5) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        if page_article_list.has_next():
            next_page = page + 1
        else:
            next_page = page
        if page_article_list.has_previous():
            previous_page = page - 1
        else:
            previous_page = page

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
            'next_page': next_page,
            'previous_page': previous_page,
            'top6_article_list': top6_article_list
        }
    return render(request, 'blog/index.html', context={
        'article_list': article_list, 'data': data
    })


# return render(request, 'blog/index.html',
#               {
#                   'article_list': page_article_list,
#                   'page_num': range(1, page_num + 1),
#                   'curr_page': page,
#                   'next_page': next_page,
#                   'previous_page': previous_page,
#                   'top6_article_list': top6_article_list
#               }
#               )


# 一级boss模块，供urls.py调用
def get_iboss_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    all_article = Article.objects.get_queryset().order_by('article_id').filter(lable='iboss')
    top6_article_list = Article.objects.order_by('-publish_date')[:6]
    # print('top6_article_list', top6_article_list)

    paginator = Paginator(all_article, 5)  # 5篇文章一页
    page_num = paginator.num_pages
    print('page num:', page_num)
    page_article_list = paginator.page(page)
    if page_num <= 1:
        article_list = all_article  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取文章页码，默认第一页
        article_list = page_article_list  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第一页页码后是否需要省略号
        right_has_more = False  # 标示最后一页页码后是否需要省略号
        # 标示是否需要显示第 1 页的页码号
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False
        last = False  # 标示是否需要显示最后一页的页码号
        total_pages = page_num
        page_range = paginator.page_range
        if page == 1:
            right = page_range[page:page + 2]  # 获取右边连续号码页
            print(total_pages)
            if right[-1] < total_pages - 1:
                # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示
                right_has_more = True
            if right[-1] < total_pages:
                # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:
            left = page_range[(page - 5) if (page - 5) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
                left_has_more = True
            if left[0] > 1:
                # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 5) if (page - 5) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        if page_article_list.has_next():
            next_page = page + 1
        else:
            next_page = page
        if page_article_list.has_previous():
            previous_page = page - 1
        else:
            previous_page = page

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
            'next_page': next_page,
            'previous_page': previous_page
        }
    return render(request, 'blog/iboss.html', context={
        'article_list': article_list, 'data': data,
        'top6_article_list': top6_article_list
    })


# 一级boss接口协议模块，供urls.py调用
def get_protocol_page(request):
    # all_article = Article.objects.get_queryset().order_by('article_id').filter(lable='tocol')
    return render(request, 'blog/protocol/protocol.html')


# 渠道模块，供urls.py调用
def get_channel_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    all_article = Article.objects.get_queryset().order_by('article_id').filter(lable='channel')
    top6_article_list = Article.objects.order_by('-publish_date')[:6]

    paginator = Paginator(all_article, 5)  # 5篇文章一页
    page_num = paginator.num_pages
    print('page num:', page_num)
    page_article_list = paginator.page(page)
    if page_num <= 1:
        article_list = all_article  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取文章页码，默认第一页
        article_list = page_article_list  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第一页页码后是否需要省略号
        right_has_more = False  # 标示最后一页页码后是否需要省略号
        # 标示是否需要显示第 1 页的页码号
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False
        last = False  # 标示是否需要显示最后一页的页码号
        total_pages = page_num
        page_range = paginator.page_range
        if page == 1:
            right = page_range[page:page + 2]  # 获取右边连续号码页
            print(total_pages)
            if right[-1] < total_pages - 1:
                # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示
                right_has_more = True
            if right[-1] < total_pages:
                # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:
            left = page_range[(page - 5) if (page - 5) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
                left_has_more = True
            if left[0] > 1:
                # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 5) if (page - 5) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        if page_article_list.has_next():
            next_page = page + 1
        else:
            next_page = page
        if page_article_list.has_previous():
            previous_page = page - 1
        else:
            previous_page = page

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
            'next_page': next_page,
            'previous_page': previous_page
        }
    return render(request, 'blog/channel.html', context={
        'article_list': article_list, 'data': data,
        'top6_article_list': top6_article_list
    })


# 短厅模块，供urls.py调用
def get_interface_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    all_article = Article.objects.get_queryset().order_by('article_id').filter(lable='interface')
    top6_article_list = Article.objects.order_by('-publish_date')[:6]

    paginator = Paginator(all_article, 5)  # 5篇文章一页
    page_num = paginator.num_pages
    print('page num:', page_num)
    page_article_list = paginator.page(page)
    if page_num <= 1:
        article_list = all_article  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取文章页码，默认第一页
        article_list = page_article_list  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第一页页码后是否需要省略号
        right_has_more = False  # 标示最后一页页码后是否需要省略号
        # 标示是否需要显示第 1 页的页码号
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False
        last = False  # 标示是否需要显示最后一页的页码号
        total_pages = page_num
        page_range = paginator.page_range
        if page == 1:
            right = page_range[page:page + 2]  # 获取右边连续号码页
            print(total_pages)
            if right[-1] < total_pages - 1:
                # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示
                right_has_more = True
            if right[-1] < total_pages:
                # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:
            left = page_range[(page - 5) if (page - 5) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
                left_has_more = True
            if left[0] > 1:
                # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 5) if (page - 5) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        if page_article_list.has_next():
            next_page = page + 1
        else:
            next_page = page
        if page_article_list.has_previous():
            previous_page = page - 1
        else:
            previous_page = page

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
            'next_page': next_page,
            'previous_page': previous_page
        }
    return render(request, 'blog/interface.html', context={
        'article_list': article_list, 'data': data,
        'top6_article_list': top6_article_list
    })


# 其他模块，供urls.py调用
def get_other_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    all_article = Article.objects.get_queryset().order_by('article_id').filter(lable='other')
    top6_article_list = Article.objects.order_by('-publish_date')[:6]

    paginator = Paginator(all_article, 5)  # 5篇文章一页
    page_num = paginator.num_pages
    print('page num:', page_num)
    page_article_list = paginator.page(page)
    if page_num <= 1:
        article_list = all_article  # 直接返回所有文章
        data = ''  # 不需要分页按钮
    else:
        page = int(request.GET.get('page', 1))  # 获取文章页码，默认第一页
        article_list = page_article_list  # 返回指定页码的页面
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第一页页码后是否需要省略号
        right_has_more = False  # 标示最后一页页码后是否需要省略号
        # 标示是否需要显示第 1 页的页码号
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False
        last = False  # 标示是否需要显示最后一页的页码号
        total_pages = page_num
        page_range = paginator.page_range
        if page == 1:
            right = page_range[page:page + 2]  # 获取右边连续号码页
            print(total_pages)
            if right[-1] < total_pages - 1:
                # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
                # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示
                right_has_more = True
            if right[-1] < total_pages:
                # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
                # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:
            left = page_range[(page - 5) if (page - 5) > 0 else 0:page - 1]  # 获取左边连续号码页
            if left[0] > 2:
                # 如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
                left_has_more = True
            if left[0] > 1:
                # 如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  # 如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page - 5) if (page - 5) > 0 else 0:page - 1]  # 获取左边连续号码页
            right = page_range[page:page + 2]  # 获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        if page_article_list.has_next():
            next_page = page + 1
        else:
            next_page = page
        if page_article_list.has_previous():
            previous_page = page - 1
        else:
            previous_page = page

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
            'next_page': next_page,
            'previous_page': previous_page
        }
    return render(request, 'blog/other.html', context={
        'article_list': article_list, 'data': data,
        'top6_article_list': top6_article_list
    })


# 文章详情，供urls.py调用
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


# 接口协议详情，供urls.py调用
def get_standardetail_page(request, article_id):
    all_article = Article.objects.get_queryset().order_by('article_id').filter(lable='tocol')
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
    return render(request, 'blog/protocol/standardetail.html',
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


def PageNotFound(request):
    return render(request, 'error/404.html')
