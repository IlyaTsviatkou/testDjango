import hashlib
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Course,City,Number,Player,Organisation,Profile
from .forms import StudentForm,AuthUserForm,RegisterUserForm
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from hello.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone, dateformat
from django.contrib.postgres.search import SearchVector

def about(request):
    return HttpResponse("<h2>О сайте</h2>")
 
def index(request):
    return render(request, "index.html")

def org(request):
    search = request.GET.get('search','')
    select = request.GET.get('select','')
    if search:
        if select=='1':
            search_org_vector = SearchVector('name','age','city','number')
            org= Organisation.objects.annotate(search=search_org_vector).filter(search=search)
        if select=='2':
            org= Organisation.objects.filter(number__name=search)
        if select=='3':
            org= Organisation.objects.filter(city__name=search)
    else:
        org = Organisation.objects.all()
    return render(request, "org.html", {"org": org})
    
 

def create(request):
    if request.method == "POST":
        tom = Organisation()
        tom.name = request.POST.get("name")
        tom.age = request.POST.get("age")
        tom.save()
        number = Number(name= request.POST.get("number"))
        number.save()
        auth = City(name = request.POST.get("city1"))
        auth.save()
        tom.city.add(auth)
        tom.number.add(number)
        return HttpResponseRedirect("/org")



def player_out(request):
    players = Player.objects.all()
    if request.method == 'POST':
        user=request.user
        form = StudentForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = user
            player.stbool = True
            #player.user.save()
            player.save() # Now you can send it to DB
            form.save_m2m()
            return redirect("/")
        else :
            return render(request,'player.html',{'form':form,'players':players})
    else:
        form=StudentForm()
        return render(request,"player.html",{'form':form,'players':players})
   

class MyprojectLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = '/'
    def get_success_url(self):
        return self.success_url

class RegisterUserView(CreateView):
    model = User
    template_name = 'register_page.html'
    form_class = RegisterUserForm
    success_url = '/'
    success_msg = 'Пользователь успешно создан'
    def form_valid(self,form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        aut_user = authenticate(username=username,password=password,email=email)
        login(self.request, aut_user)
        sha = hashlib.md5(username.encode())
        send_mail(
                'Подтверждение почты',
                render_to_string('message/message.txt', {
                    'name': username,
                    'email': email,
                    'text': 'http://127.0.0.1:8000/confirmation/' + sha.hexdigest(),
                    'time': str(dateformat.format(timezone.now(), 'Y-m-d H:i:s')),
                }), EMAIL_HOST_USER, [email])
        return form_valid

class MyProjectLogout(LogoutView):
    next_page = '/'

def page_confirmation(request, name):
    users = User.objects.all()
    context = {"information": "Активация прошла успешно"}
    for user in users:
        sha = hashlib.md5(user.username.encode())
        if sha.hexdigest() == name:
            user.profile.verified = True
            context["information"] = "Активация прошла успешно"
            user.save()
            break
    return render(request, 'confirmation.html', context) 

def put_org(request):
    try:
        player=request.user.player
        org= Organisation.objects.create(name='null',age=0)
        user = player.user
        stbool=player.stbool
        courses = player.course.all()
        list=[]
        for co in courses:
            list.append(co)
        player.delete()
        newplayer=Player.objects.create(name=player.name,age=player.age,stbool=stbool,org=org,user=user)
        newplayer.course.set(courses)
        newplayer.save()
        return redirect("/org")
    except Organisation.DoesNotExist:
        return HttpResponseNotFound("<h2>Organisation not found</h2>")

def take_org(request, id):
    org = Organisation.objects.get(id=id)
    player=request.user.player
    user = player.user
    stbool=player.stbool
    org0=player.org
    courses = player.course.all()
    list=[]
    for co in courses:
        list.append(co)
    if player.org.name=='null':
        player.org.delete()
    else:
        player.delete()
    newplayer=Player.objects.create(name=player.name,age=player.age,stbool=stbool,org=org,user=user)
    newplayer.course.set(courses)
    newplayer.save()
    return HttpResponseRedirect("/org")

def kabinet(request):
    search = request.GET.get('search','')
    mycourse = request.user.player.course.all()
    if search:
        search_course_vector = SearchVector('name','stage')
        course= Course.objects.annotate(search=search_course_vector).filter(search=search)
    else:
        course = Course.objects.all()
        x= course.difference(mycourse)
        course=x
    return render(request, "kab.html", {"course": course,"mycourse":mycourse})

def take_course(request,id):
    try:
        course = Course.objects.get(id=id)
        request.user.player.course.add(course)
        request.user.player.save()
        return HttpResponseRedirect("/kab")
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Course not found</h2>")

def put_course(request,id):
    try:
        course = Course.objects.get(id=id)
        request.user.player.course.remove(course)
        request.user.player.save()
        return HttpResponseRedirect("/kab")
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Course not found</h2>")