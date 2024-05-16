"""
from django.shortcuts import render, redirect
from .models import MyModel
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from app.models import CustomUser  # CustomUser 모델 임포트
"""
"""
def my_view(request):
    objects = MyModel.objects.all()
    return render(request, 'app/my_template.html', {'objects': objects})

class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('my-view')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('option')  # 회원가입 정보와 함께 옵션 페이지로 이동
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

def option(request):
    # 옵션 페이지 로직 작성
    return render(request, 'app/option.html')
    """

from django.shortcuts import render
from .models import ExerciseRecord
import datetime

def view_calendar(request):
    return render(request, 'app/calendar_template.html')

def exercise_record(request):
    selected_date = request.GET.get('selected_date')
    if selected_date:
        # 유닉스 타임스탬프를 밀리초로 나타내는 경우
        timestamp_milliseconds = int(selected_date)
        # 밀리초를 초로 변환하고 datetime으로 변환
        timestamp_seconds = timestamp_milliseconds / 1000
        selected_date = datetime.datetime.fromtimestamp(timestamp_seconds).strftime('%Y-%m-%d')
        exercise_records = ExerciseRecord.objects.filter(date=selected_date)
    else:
        exercise_records = None  # 선택된 날짜가 없는 경우
    return render(request, 'app/exercise_record.html', {'selected_date': selected_date, 'exercise_records': exercise_records})
