from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class loginForm(forms.Form):
    username = forms.CharField(label="用户名",
                                widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"请输入用户名"}))
    password = forms.CharField(label="密码",
                                widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"请输入密码"}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            print("错误")
            raise forms.ValidationError("用户名或密码错误")
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class regForm(forms.Form):
    username = forms.CharField(label="用户名",
                                min_length = 3,
                                max_length = 15,
                                widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-15位用户名'}))
    email = forms.EmailField(label="邮箱",
                            widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    password = forms.CharField(label="密码",
                                min_length=6,
                                max_length=20,
                                widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入6-20位密码'}))
    password_again = forms.CharField(label="再输入一次密码",
                            min_length=6,
                            max_length=20,
                            widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))    

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("该用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(
        label = '新的昵称',
        max_length = 20,
        widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入20位以内的新的昵称'})
    )

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise ValidationError("新的昵称不能为空！")
        return nickname_new

    # 判断用户是否登录，若没有登录不能修改
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱',widget=forms.EmailInput(
            attrs={'class':'form-control','placeholder':'请输入邮箱'}
        )
    )

    verification_code = forms.CharField(label='验证码',widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'获取验证码'}
        )
    )