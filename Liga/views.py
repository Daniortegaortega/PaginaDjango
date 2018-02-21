from django.shortcuts import render
from django.http import HttpResponseRedirect
from Liga.models import Adicional,Liga,Skin,Inscriben
from django.contrib.auth.models import User
from Liga.forms import Saldo,registrar,username, contactar
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView, View

from django.core.mail import EmailMessage


class index(TemplateView):
    template_name = "index.html"

def registrarUser(request):
    if request.method == "POST":
        form=registrar(request.POST, request.FILES)
        if form.is_valid():
            cd=form.cleaned_data
            u_username = cd['username']
            u_email = cd['email']
            u_password = cd['password']
            u_nombre = cd['nombre']
            u_apellidos = cd['apellidos']
            u_telefono=cd['telefono']
            u_numero_cuenta = cd['numero_cuenta']
            u_foto=cd['foto']
            user = User.objects.create_user(u_username, u_email,u_password)
            user.save()
            usu = User.objects.get(username=u_username)
            adicional = Adicional(codigo=usu, nombre=u_nombre,apellidos=u_apellidos, telefono=u_telefono,numero_cuenta=u_numero_cuenta,foto=u_foto)
            adicional.save()
            return HttpResponseRedirect("/Liga/login/")
    else:
        form=registrar()
    return render(request,"registrar.html",{'form': form})

def usernameChange(request, user_id):
    if request.method == "POST":
        form=username(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            u_antiguo = cd['old_username']
            u_new = cd['new_username']
            user = User.objects.get(pk=user_id)
            if u_antiguo == user.username:
                user.username = u_new
                user.save()
                return HttpResponseRedirect("/Liga/index/")
            else:
                context=["El nombre de usuario actual no es correcto"]
                return render(request,"username.html",{'context':context,"form":form})

    else:
        form = username()
    return render(request,"username.html",{'form':form})


def saldoUser(request, user_id):
    usuario=Adicional.objects.all()
    inscriben = Inscriben.objects.all()
    if request.method == "POST":
        form = Saldo(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            u_numero_cuenta= cd['numero_cuenta']
            u_saldo=cd['saldo']
            usu= User.objects.get(pk=user_id)
            usuar=Adicional.objects.get(codigo=usu)
            if usuar.numero_cuenta == u_numero_cuenta:
                usuar.saldo= usuar.saldo + u_saldo
                usuar.save()
                return HttpResponseRedirect("/Liga/perfil")
            else:
                context = ["El numero de Cuenta no es correcto"]
                return render(request, "saldo.html", {'context': context, "form": form,'usuario': usuario, 'inscriben': inscriben})
    else:
        form = Saldo()
    return render(request,"saldo.html",{'form':form,'usuario': usuario, 'inscriben': inscriben})






@login_required()
def mostrarPerfil(request):
    usuario = Adicional.objects.all()
    inscritas = Inscriben.objects.all()
    return render(request, "perfilUser.html",{'usuario':usuario, 'inscritas':inscritas})

@login_required()
def borrarLiga(request, user_id, liga_id):
    user=User.objects.get(pk=user_id)
    usuario= Adicional.objects.get(codigo=user)
    liga = Liga.objects.get(pk=liga_id)
    inscriben = Inscriben.objects.get(usuario=usuario,liga=liga)
    inscriben.delete()
    return HttpResponseRedirect("/Liga/perfil")





@login_required()
def skins(request):
    skins=Skin.objects.all()
    usuario = Adicional.objects.all()
    return render(request,"skins.html",{'skins':skins,'usuario':usuario})

@login_required()
def comprarSkin(request, skin_id, user_id):
    skins = Skin.objects.all()
    usuario = Adicional.objects.all()

    u = User.objects.get(pk=user_id)
    a = Adicional.objects.get(codigo=u)
    s = Skin.objects.get(pk=skin_id)
    precio = s.precio
    saldo = a.saldo
    restante = saldo - precio
    a.skin = s
    a.saldo = restante
    a.save()
    return render(request,"skins.html",{'skins':skins,'usuario':usuario})








class vender(ListView):
    model = Adicional
    template_name = 'venderSkin.html'


def venderSkin(request, user_id):
    u = User.objects.get(pk=user_id)
    a = Adicional.objects.get(codigo=u)
    i = Inscriben.objects.all()
    for x in i:
        if x.usuario == a:
            object_list = Adicional.objects.all()
            context = ["No puedes vender la skin si estas inscrito en una liga"]
            return render(request, "venderSkin.html", {'context': context,'object_list':object_list})
    precio = a.skin.precio
    saldo = a.saldo
    total = precio + saldo
    a.saldo = total
    a.skin = None
    a.save()
    return HttpResponseRedirect("/Liga/vender")







def ligas(request):
    ligas = Liga.objects.all().order_by('coste_inscripcion')
    return render(request, "ligas.html", {'ligas':ligas})

def inscribirseLiga(request,user_id, liga_id):
    ligas = Liga.objects.all().order_by('coste_inscripcion')
    l = Liga.objects.get(pk=liga_id)
    u = User.objects.get(pk=user_id)
    a = Adicional.objects.get(codigo=u)
    i = Inscriben.objects.filter(usuario=a)
    saldo = a.saldo
    coste = l.coste_inscripcion
    total = saldo - coste
    if a.skin == None or total < 0:
        context = ["Necesitas una skin para inscribirte"]
        return render(request, "ligas.html", {'context': context, 'ligas':ligas})
    if  total < 0:
        context = ["NNo tienes saldo suficiente"]
        return render(request, "ligas.html", {'context': context, 'ligas':ligas})
    for x in i:
        if x.liga == l:
            return HttpResponseRedirect("/Liga/ligas")
    inscribe = Inscriben(usuario=a, liga=l)
    inscribe.save()
    a.saldo=total
    a.save()
    return HttpResponseRedirect("/Liga/perfil/")




class contactomail(View):

    def get(self,request):
        form=contactar()
        return render(request, "contactar.html", {'form': form})

    def post(self,request):
        form = contactar(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            correo = cd['correo']
            asunto = cd['asunto']
            mensaje = cd['mensaje']
            mail = EmailMessage(asunto, mensaje, correo, to=['cskin.django@gmail.com'])
            mail.send()
            return HttpResponseRedirect("/Liga/index")
        return render(request, "contactar.html",{'form':form})

