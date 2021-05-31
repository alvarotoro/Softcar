from django.db import models
from django.utils import timezone
from datetime import datetime   
# Create your models here.
class Cliente(models.Model):
    Cli_Run = models.IntegerField(primary_key=True,blank=False)
    Cli_Nom = models.CharField(max_length=20,blank=False)
    Cli_Ap_Pat = models.CharField(max_length=30,blank=False)
    Cli_Ap_Mat = models.CharField(max_length=30,blank=False)
    Cli_Email = models.CharField(max_length=50,blank=True)
    Cli_Tel = models.IntegerField(blank=False)

class MarcaRepuesto(models.Model):
    Mar_ID =  models.CharField(max_length=10,primary_key=True,blank=False)
    Mar_nom =  models.CharField(max_length=50,blank=False)
   

class Estado(models.Model):
    Est_Id = models.IntegerField(primary_key=True,blank=False)
    Est_Nom = models.CharField(max_length=30,blank=False)

class Marca(models.Model):
    Mar_Id = models.IntegerField(primary_key=True,blank=False)
    Mar_nom = models.CharField(max_length=30,blank=False)

class Tipo(models.Model):
    Tip_Id = models.IntegerField(primary_key=True,blank=False)
    Tip_nom = models.CharField(max_length=30,blank=False)

class Vehiculo(models.Model):
    Veh_Id = models.CharField(max_length=8,primary_key=True,blank=False)
    Veh_Mod = models.CharField(max_length=20,blank=False)
    Veh_Mar = models.ForeignKey(Marca, on_delete=models.CASCADE)
    Veh_Tip = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    Veh_Agno = models.IntegerField(blank=False)
    Veh_Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class Trabajo(models.Model):
    Tra_Id = models.CharField(max_length=20,primary_key=True,blank=False)
    Tra_Des = models.CharField(max_length=500,blank=False)  
    Tra_Fechainicio = models.DateTimeField(default=datetime.now, blank=False)
    Tra_Fechafin = models.DateTimeField(blank=True)
    Tra_Est = models.ForeignKey(Estado, on_delete=models.CASCADE)
    Tra_Vehic = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
   
class Repuesto(models.Model):
    Rep_id = models.CharField(max_length=20,primary_key=True,blank=False)          	 		
    Rep_Nom = models.CharField(max_length=30,blank=False) 
    Rep_Can = models.IntegerField(blank=False)
    Rep_Mar = models.ForeignKey(MarcaRepuesto, on_delete=models.CASCADE)

class Tra_rep(models.Model):
    Trep_Trabajo = models.ForeignKey(Trabajo,primary_key=True, on_delete=models.CASCADE)
    Trep_Repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    Trep_Cant = models.IntegerField(blank=False)

