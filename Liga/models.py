from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.
class Skin(models.Model):
    CATEGORIA_TIPO = (
        ('Covert Sniper Rifle','Covert Sniper Rifle'),
        ('Covert Knife', 'Covert Knife'),
        ('Covert Rifle','Covert Rifle'),
    )
    CATEGORIA_TIPO2 = (
        ('Gamma2','Gamma2'),
        ('Cobblestone', 'Cobblestone'),
        ('Breakout','Breakout'),
    )
    nombre=models.CharField(max_length=50,unique=True)
    tipo=models.CharField(max_length=30,choices=CATEGORIA_TIPO)
    precio=models.FloatField()
    coleccion=models.CharField(max_length=13,choices=CATEGORIA_TIPO2)
    imagen=models.ImageField(upload_to='imgSkins/', blank=True, null=True, default='imgSkins/default.png')
    def __str__(self):
        return self.nombre

class Liga(models.Model):
    CATEGORIA_TIPO = (
        ('PLATA','Plata'),
        ('NOVA', 'Nova'),
        ('AK','AK'),
        ('SUPREME','Supreme'),
        ('GLOBAL','Global'),
    )
    nombre=models.CharField(max_length=30, unique=True)
    coste_inscripcion=models.FloatField()
    categoria=models.CharField(max_length=10, choices=CATEGORIA_TIPO, default='PLATA')
    imagenLiga = models.ImageField(upload_to='imgLigas/', default='imgLigas/default.png')
    def __str__(self):
        return self.nombre


class Adicional(models.Model):
    codigo = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    nombre= models.CharField(max_length=25)
    apellidos = models.CharField(max_length=40)
    telefono = models.CharField(max_length=9, validators=[MinLengthValidator(9)])
    saldo=models.FloatField(default=0)
    numero_cuenta = models.CharField(max_length=10 ,help_text="Compuesto del IBAN (ES) MAS 8 digitos",unique=True)
    foto=models.ImageField(upload_to='imgUsuarios/', default='imgUsuarios/default.jpg')
    skin=models.ForeignKey(Skin,on_delete=models.CASCADE,null=True)
    liga=models.ManyToManyField(Liga,through='Inscriben')


class Inscriben(models.Model):
    usuario=models.ForeignKey(Adicional,on_delete=models.CASCADE)
    liga=models.ForeignKey(Liga,on_delete=models.CASCADE)
    fecha=models.DateField(auto_now=True)
    class Meta:
        unique_together = (("usuario", "liga","fecha"),)
    def __str__(self):
        return "Id usuario: "+str(self.usuario)+" Id liga: "+str(self.liga)+" fecha: "+str(self.fecha)

