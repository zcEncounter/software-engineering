from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import SignUpForm
from .models import FishNumber
from .models import FishData
from .models import Information
from django.db.models import Count
import json
import csv
from django.http import HttpResponse
import io

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('system')  # 管理员登录后跳转到系统界面
            else:
                return redirect('usersystem')  # 普通用户登录后跳转到用户系统界面
        else:
            messages.error(request, '用户名或密码错误！')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # 注册成功后重定向到登录页面
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # 处理注册成功后的逻辑
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def system_view(request):
    return render(request, 'system.html')

def usersystem_view(request):
    return render(request, 'usersystem.html')

def main_info_view(request):
    # 获取最新的一条 Information 数据记录
    latest_info = Information.objects.latest('id')
    # 将数据传递给模板
    return render(request, 'main_info.html', {'latest_info': latest_info})

#def underwater_system_view(request):
#    return render(request, 'underwater_system.html')

def data_center_view(request):
    return render(request, 'data_center.html')

def smart_center_view(request):
    return render(request, 'smart_center.html')

def admin_management_view(request):
    users = User.objects.all()  # 获取所有用户信息
    return render(request, 'admin_management.html', {'users': users})

'''
def underwater_system_view(request):
    # 获取最新的一条数据
    fishnumber = FishNumber.objects.latest('id')
    context = {
        'total': fishnumber.total if fishnumber else 0,
        'add': fishnumber.add if fishnumber else 0,
        'minus': fishnumber.minus if fishnumber else 0,
        'score': fishnumber.score if fishnumber else 0
    }
    return render(request, 'underwater_system.html', context)

def fish_data_view(request):
    # 获取所有的 FishData 数据
    fish_data = FishData.objects.all()

    # 统计每种鱼类的数量
    fish_counts = fish_data.values('kind').annotate(count=Count('kind'))

    # 将数据组织成前端需要的格式
    data = {
        'kinds': [fish['kind'] for fish in fish_counts],  # 获取所有不同的鱼类种类
        'attributes': ['weight', 'length', 'height', 'width'],  # 属性列表
        'fish_data': {fish['kind']: {'weight': [], 'length': [], 'height': [], 'width': []} for fish in fish_counts}
    }

    for fish in fish_data:
        data['fish_data'][fish.kind]['weight'].append(fish.weight)
        data['fish_data'][fish.kind]['length'].append(fish.length)
        data['fish_data'][fish.kind]['height'].append(fish.height)
        data['fish_data'][fish.kind]['width'].append(fish.width)

    return render(request, 'underwater_system.html', {'data': data})
'''

def underwater_system_view(request):
    # 处理文件上传
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)  # 跳过标题行
        for row in csv.reader(io_string, delimiter=',', quotechar='"'):
            FishData.objects.create(
                kind=row[0],
                weight=row[1],
                length=row[2],
                height=row[3],
                width=row[4]
            )
        return redirect('underwater_system_view')

    # 获取数据
    fishnumber = FishNumber.objects.latest('id')
    fish_data = FishData.objects.all()
    fish_counts = fish_data.values('kind').annotate(count=Count('kind'))

    data = {
        'total': fishnumber.total if fishnumber else 0,
        'add': fishnumber.add if fishnumber else 0,
        'minus': fishnumber.minus if fishnumber else 0,
        'score': fishnumber.score if fishnumber else 0,
        'kinds': [fish['kind'] for fish in fish_counts],
        'attributes': ['weight', 'length', 'height', 'width'],
        'fish_data': {fish['kind']: {'weight': [], 'length': [], 'height': [], 'width': []} for fish in fish_counts},
        # 'fish_counts': [{'kind': fish['kind'], 'count': fish['count']} for fish in fish_counts],  # 转换为列表并改变格式
        'fish_counts': {fish['kind']:{'count':fish['count']} for fish in fish_counts}
    }

    for fish in fish_data:
        data['fish_data'][fish.kind]['weight'].append(fish.weight)
        data['fish_data'][fish.kind]['length'].append(fish.length)
        data['fish_data'][fish.kind]['height'].append(fish.height)
        data['fish_data'][fish.kind]['width'].append(fish.width)

    json_data = json.dumps(data)

    return render(request, 'underwater_system.html', {'json_data': json_data, 'fish_counts': fish_counts})

def export_fish_data_csv(request):
    # 创建 HttpResponse 对象并设置其内容类型
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fish_data.csv"'

    # 创建 CSV writer
    writer = csv.writer(response)
    writer.writerow(['kind', 'weight', 'length', 'height', 'width'])

    # 获取所有 FishData 对象并写入 CSV 文件
    fish_data = FishData.objects.all().values_list('kind', 'weight', 'length', 'height', 'width')
    for fish in fish_data:
        writer.writerow(fish)

    return response
