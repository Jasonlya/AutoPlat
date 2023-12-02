
# Django+bootstrap+jqurey+mysql
## Django基础
### 1.新建django项目
### 2.创建app
    python manage.py startapp xx
### 3.注册app
    settings.py中INSTALLED_APPS中 xx.app.xxConfig
### 4.配置数据库
    settings.py中DATABASES
### 5.创建表
    写models
    注册表 python manage.py makemigrations
    迁移表 python manage.py migrate
### 6.写功能代码
    urls.py配置路由
    view.py 接口进行数据操作
    templates 静态文件
### 7.静态文件配置（css、js、图片）
    static  css、js、图片

## Django进阶
### 1.Cookie和Session
![img.png](img.png)
### 2.中间件
    settings.py中MIDDLEWARE
    所有的请求均会经过中间件，请求数据走一遍中间件，响应数据再走一遍中间件
#### 3.自定义中间件
![img_2.png](img_2.png)

#### 4.模板的概念
![img_4.png](img_4.png)

#### 5.表连接
    # 表关联  级联删除 on_delete=models.CASCADE    级联为空 on_delete=models.SET_NULL,null=True,blank=True
    depart = models.ForeignKey(verbose_name="关联部门", to="Depart", on_delete=models.CASCADE)
![img_5.png](img_5.png)

#### 6.Form和ModelForm
    django中的form组件有两大作用：
        生成HTML表单标签
        数据校验
![img_6.png](img_6.png)
![img_7.png](img_7.png)

    django中ModelForm组件作用：
![img_8.png](img_8.png)
## 问题
### 1.中间件进行鉴权过多。对于不需要鉴权的页面，中间件进行特殊处理
![img_3.png](img_3.png)