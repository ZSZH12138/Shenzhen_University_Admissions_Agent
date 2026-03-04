\# Django 项目使用说明



本项目为基于 Django 框架开发的 Web 应用。本文档将指导用户完成环境配置与项目运行。



---



\## 一、安装依赖



进入项目根目录（包含 manage.py 的目录），执行以下命令安装依赖：



代码：

pip install -r requirements.txt



---



\## 二、数据库初始化



首次运行项目时，需要执行数据库迁移命令：



代码：

python manage.py makemigrations



代码：

python manage.py migrate



---

\## 三、启动项目



在项目根目录下运行：



代码：

python manage.py runserver



默认情况下，项目将运行在：



http://127.0.0.1:8000/



在浏览器中打开上述地址即可访问项目。



---

\## 七、常见问题



1\. 端口被占用  

可指定端口运行，例如：



```bash

python manage.py runserver 8001

```



2\. 静态文件未加载  

请确保已正确配置 `STATIC\_URL` 和 `STATIC\_ROOT` 。



3\. 数据库错误  

请确认数据库配置正确，并已执行 migrate。



---



\## 八、停止服务



在终端中按 `Ctrl` + `C` 即可停止 Django 服务。

