import uuid

from django.shortcuts import render, redirect
from web import models
from django import forms
# Create your views here.
from django.shortcuts import HttpResponse
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "请输入用户名"}),
        validators=[RegexValidator(r'^\w{3,}$', '用户名格式错误')]
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "请输入密码"})
    )

    # 默认get请求


def login(request):
    """ 例如：用户名、密码 -> 数据库校验"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 校验成功拿到字典 form.cleaned_data -> {'username': '3213', 'password': '12321'}
        # 去数据库中校验，用户名和密码的合法性
        # user_object = models.UserInfo.objects.filter(name=form.cleaned_data['username'],password=form.cleaned_data['password']).first()
        user_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if user_object:
            # 如果成功
            """
                1.生成随机字符串
                2.返回到用户浏览器的cookie中
                3.存储到网站的session中 随机字符串+用户标识
            """
            request.session["info"] = {"id": user_object.id, "name": user_object.username}
            return redirect('/index/')
        else:
            # 如果失败，展示错误信息
            return render(request, "login.html", {"form": form, 'error': "用户名或密码错误"})
    else:
        return render(request, 'login.html', {'form': form})
    """老方法，改进为上面form表单方法"""
    # # 判断是get请求还是post请求
    # if request.method == "POST":
    #     # 去请求体中获取数据，再进行校验
    #     username = request.POST.get('username')
    #     password = request.POST.get('pwd')
    #     # 去数据库中校验，用户名和密码的合法性
    #     user_object = models.UserInfo.objects.filter(name=username, password=password).first()
    #     if user_object:
    #         # 如果成功
    #         """
    #             1.生成随机字符串
    #             2.返回到用户浏览器的cookie中
    #             3.存储到网站的session中 随机字符串+用户标识
    #         """
    #         request.session["info"] = {"id": user_object.id, "name": user_object.name}
    #         return redirect('/index/')
    #     else:
    #         # 如果失败，展示错误信息
    #         return render(request, "login.html", {"error": "用户名或密码错误"})
    # return render(request, "login.html")


def index(request):
    """
    判断用户是否已经登录，未登录跳转登录页面
    """
    info = request.session.get("info")
    # if not info:
    #     return redirect('/login/')
    # else:
    """首页"""
    queryset = [
        {"id": 1, 'phone': "134567812", "city": "上海"},
        {"id": 2, 'phone': "134567813", "city": "北京"},
        {"id": 3, 'phone': "134567814", "city": "杭州"},
        {"id": 4, 'phone': "134567815", "city": "南京"}
    ]
    return render(request, "index.html", {"data": queryset, "info": info})


def user(request):
    """用户列表"""
    querset = models.UserInfo.objects.all().order_by("id")  # asc升序排序
    # querset = models.Depart.objects.all().order_by("-departid")   #desc降序排序
    return render(request, 'user.html', {"querset": querset})


def add_user(request):
    """添加用户"""
    depart_list = models.Depart.objects.all().order_by("departid")
    # 判断是get请求还是post请求,get访问新增页面，post新增部门
    if request.method == "GET":
        return render(request, "user_add.html", {"depart": depart_list})
    # 去请求体中获取数据
    yhxm = request.POST.get('yhxm')
    yhpd = request.POST.get('yhpwd')
    yhnl = request.POST.get('yhnl')
    yhyx = request.POST.get('yhyx')
    lxfs = request.POST.get('lxfs')
    ssbm = request.POST.get('optionid')
    models.UserInfo.objects.create(name=yhxm, age=yhnl, email=yhyx, phonenum=lxfs, depart_id=ssbm,
                                   password=yhpd)
    # 新增成功，跳转回列表页面
    return redirect('/user/')


def update_user(request):
    """编辑用户"""
    # 去请求体中获取数据
    userid = request.GET.get('userid')
    depart_list = models.Depart.objects.all().order_by("departid")
    if request.method == "GET":
        # 查询出数据进行回显
        user = models.UserInfo.objects.filter(id=userid).first()
        return render(request, "user_update.html", {"user": user, "depart": depart_list})
    # 编辑并提交数据
    yhxm = request.POST.get('yhxm')
    yhpd = request.POST.get('yhpwd')
    yhnl = request.POST.get('yhnl')
    yhyx = request.POST.get('yhyx')
    lxfs = request.POST.get('lxfs')
    ssbm = request.POST.get('optionid')
    # 更新数据
    models.UserInfo.objects.filter(id=userid).update(name=yhxm, age=yhnl, email=yhyx, phonenum=lxfs, depart_id=ssbm,
                                                     password=yhpd)
    return redirect('/user/')


def delete_user(request):
    """删除用户"""
    userid = request.GET.get('userid')
    models.UserInfo.objects.filter(id=userid).delete()
    return redirect('/user/')


def depart(request):
    # 新增单条
    # models.Depart.objects.create(departid=1,departname="新增部门",count=50)
    # 新增多条
    # depat_list = [
    #     models.Depart(departid=2,departname="新增部门2",count=30),
    #     models.Depart(departid=3, departname="新增部门3", count=40)
    # ]
    # models.Depart.objects.bulk_create(depat_list)
    # return HttpResponse("新增部门成功")
    # 查询
    # quereset = models.Depart.objects.all()     #查询所有
    # quereset = models.Depart.objects.filter(departid__gt=2)  #departid>2的数据
    # for item in quereset:
    #     print(item.departid,item.departname,item.count)
    # first = models.Depart.objects.all().first()   #查询第一条
    # print(first.departid,first.departname,first.count)
    # 删除
    # models.Depart.objects.filter(departid=1).delete()
    # 更新
    # models.Depart.objects.filter(departid=2).update(count=66)
    """部门列表"""
    querset = models.Depart.objects.all()  # asc升序排序
    # querset = models.Depart.objects.all().order_by("-departid")   #desc降序排序
    return render(request, 'depart.html', {"querset": querset})


class DepartModelForm(forms.ModelForm):
    class Meta:
        model = models.Depart
        # 有自增字段的时候会更新失败
        # fields = '__all__'
        fields = ['departname', 'count']


def add_depart(request):
    """添加部门"""
    is_edit = False
    # 判断是get请求还是post请求,get访问新增页面，post新增部门
    if request.method == "GET":
        form = DepartModelForm()
        return render(request, "depart_form.html", {'form': form})
    # 去请求体中获取数据 两种方式
    # departname = request.POST.get('bmmc')
    # count = request.POST.get('bmrs')
    form = DepartModelForm(request.POST)
    # models.Depart.objects.create(departname=form.cleaned_data['departname'], count=form.cleaned_data['count'])
    if form.is_valid():
        form.save()
        # 新增成功，跳转回列表页面
        return redirect('/depart/')
    else:
        return render(request, 'depart_form.html', {'form': form, 'is_edit': is_edit})


def delete_depart(request):
    """删除部门"""
    departid = request.GET.get('departid')
    # 走get请求，进编辑页面
    models.Depart.objects.filter(departid=departid).delete()
    return redirect('/depart/')


def update_depart(request):
    """编辑部门"""
    is_edit = True
    departid = request.GET.get('departid')
    depart_object = models.Depart.objects.filter(departid=departid).first()
    if request.method == "GET":
        form = DepartModelForm(instance=depart_object)
        return render(request, "depart_form.html", {'form': form})
    # 更新之前查出来的对象
    form = DepartModelForm(request.POST)
    if form.is_valid():
        form.save()
        # 修改成功，跳转回列表页面
        return redirect('/depart/')
    else:
        return render(request, 'depart_form.html', {'form': form, 'is_edit': is_edit})

    # # 去请求体中获取数据
    # departid = request.GET.get('departid')
    # if request.method == "GET":
    #     # 查询出数据进行回显
    #     depart = models.Depart.objects.filter(departid=departid).first()
    #     return render(request, "depart_update.html", {"depart": depart})
    # 编辑并提交数据
    # departname = request.POST.get('bmmc')
    # count = request.POST.get('bmrs')
    # # 更新数据
    # models.Depart.objects.filter(departid=departid).update(departname=departname, count=count)
    # return redirect('/depart/')


def phone_list(request):
    # 1.获取数据
    queryset = [
        {"id": 1, 'phone': "134567812", "city": "上海"},
        {"id": 2, 'phone': "134567813", "city": "北京"},
        {"id": 3, 'phone': "134567814", "city": "杭州"},
        {"id": 4, 'phone': "134567815", "city": "南京"}
    ]
    return render(request, "phone_list.html", {"data": queryset})
