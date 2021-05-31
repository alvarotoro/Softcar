from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Cliente
from .models import Repuesto
import psycopg2
from django.shortcuts import redirect
from django.contrib.auth import logout
import time
from datetime import datetime
from datetime import date


def logout_view(request):
    logout(request)
    return redirect('/')
def vista1(request):
    username = request.user.username
    username = str(username)
    print("Nombre de usuario:")
    print(username)
    try:
        db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
        db.autocommit = True
        cur = db.cursor()
        select = """  
        select 
        sc_trabajo."Tra_Fechainicio" ,sc_trabajo."Tra_Fechafin" ,sc_marca."Mar_nom",sc_vehiculo."Veh_Mod" ,sc_vehiculo."Veh_Id" ,sc_estado."Est_Nom" ,sc_trabajo."Tra_Des" 
        from 
        sc_cliente,sc_vehiculo,sc_trabajo,sc_estado,sc_marca 
        where 
        sc_cliente."Cli_Run" = %s and sc_vehiculo."Veh_Cliente_id" = %s 
        and sc_vehiculo."Veh_Id" = sc_trabajo."Tra_Vehic_id" and sc_trabajo."Tra_Est_id" = sc_estado."Est_Id" 
        and sc_vehiculo."Veh_Mar_id" = sc_marca."Mar_Id" 

        """
        cur.execute(select,(username,username,))
        datos_mantenciones = cur.fetchall()
        cur.close()

        cur = db.cursor()
        select = """  
        select 
        sc_cliente."Cli_Nom" , sc_cliente."Cli_Ap_Pat" 
        from 
        sc_cliente where sc_cliente."Cli_Run" = %s

        """
        cur.execute(select,(username,))
        datos_nombre = cur.fetchall()
        cur.close()
        db.close()
        return render(request, 'vista1.html' , {'datos':datos_mantenciones,'nombre':datos_nombre})
    except:
        return render(request, 'vista1.html')

def registrarrepuesto(request):
    db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
    db.autocommit = True
    cur = db.cursor()
    select = """  
        select 
        sc_repuesto."Rep_Can" , sc_marcarepuesto."Mar_nom" , sc_repuesto."Rep_Nom" , sc_repuesto."Rep_id"  
        from 
        sc_repuesto , sc_marcarepuesto 
        where 
        sc_marcarepuesto."Mar_ID" = sc_repuesto."Rep_Mar_id"    

        """
    cur.execute(select,)
    datos_repuestos = cur.fetchall()
    datos = {'datos':datos_repuestos}
    cur.close()
    db.close()
    print(datos)
    return render(request, 'registrarrepuesto.html' , datos)        
def modificarrepuesto(request):
    repuesto = request.GET.get('repuesto')
    print(repuesto)
    db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
    db.autocommit = True
    #AQUI SACAMOS EL REPUESTO ESPECIFICO
    cur = db.cursor()
    select = """  
        select 
        sc_repuesto."Rep_Can" , sc_marcarepuesto."Mar_nom" , sc_repuesto."Rep_Nom" , sc_repuesto."Rep_id"  
        from 
        sc_repuesto , sc_marcarepuesto 
        where 
        sc_marcarepuesto."Mar_ID" = sc_repuesto."Rep_Mar_id" and sc_repuesto."Rep_Can" != '0' and sc_repuesto."Rep_id" = %s   

        """
    cur.execute(select,(repuesto,))
    datos_repuestos = cur.fetchall()

    cur.close()

    # AQUI SACAMOS TODAS LAS MARCAS
    cur = db.cursor()
    select = """  
        select sc_marcarepuesto."Mar_ID" from sc_marcarepuesto  

        """
    cur.execute(select)
    datos_marcas = cur.fetchall()

    cur.close()
    cur = db.cursor()
    select = """  
        select * from sc_marcarepuesto  

        """
    cur.execute(select,)
    datos_marcas2 = cur.fetchall()

    cur.close()
    db.close()

    return render(request, 'modificarrepuesto.html' , {'datos':datos_repuestos,'datos2':datos_marcas,'datos3':datos_marcas2} )

def modificarestado(request):
    db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
    db.autocommit = True
    cur = db.cursor()
    select = """  
        select * 
        from 
        sc_trabajo , sc_estado 
        where 
        sc_trabajo."Tra_Est_id" = sc_estado."Est_Id"   

        """
    cur.execute(select,)
    datos_estado = cur.fetchall()
    datos = {'datos':datos_estado}
    cur.close()
    db.close()
    print(datos)
    return render(request, 'modificarestado.html' , datos)
def registrarcliente(request):
    return render(request, 'registrarcliente.html')
def registrarcliente2(request):
    try:
        rut = request.GET.get('rut')
        nombre = request.GET.get('nombre')
        paterno = request.GET.get('paterno')
        materno = request.GET.get('materno')
        email = request.GET.get('email')
        celular = request.GET.get('celular')
        Cliente.objects.create(Cli_Run=rut, Cli_Nom=nombre, Cli_Ap_Pat=paterno, Cli_Ap_Mat=materno,
                                     Cli_Email=email, Cli_Tel=celular)
        User.objects.create_user(username=rut,
                                     password=celular)
        print(rut)
        print(nombre)
        print(paterno)
        print(materno)
        print(email)
        print(celular)
        return render(request, 'vista1.html' , {'nombrecln':nombre,'rutcln':rut,'paternocln':paterno,'clavecln':celular})
    except:
        error = {'error':"error"}
        return render(request, 'registrarcliente.html',error)

def modificarestado2(request):
    
    idestado = request.GET.get('id')
    idestado = str(idestado)
    print(idestado)
    db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
    db.autocommit = True
    cur = db.cursor()
    select = """  
        select * 
        from 
        sc_trabajo , sc_estado 
        where 
        sc_trabajo."Tra_Est_id" = sc_estado."Est_Id" 
        and 
        sc_trabajo."Tra_Id" = %s   

        """
    cur.execute(select,(idestado,))
    datos_estado = cur.fetchall()
    cur.close()

    cur = db.cursor()
    select = """  
        select * 
        from 
        sc_estado   

        """
    cur.execute(select,)
    datos_estado2 = cur.fetchall()
    cur.close()

    db.close()
    return render(request, 'modificarestado2.html' , {'datos':datos_estado,'datos2':datos_estado2})

def addYears(d, years):
    try:
#Return same day of the current year        
        return d.replace(year = d.year + years)
    except ValueError:
#If not same day, it will return other, i.e.  February 29 to March 1 etc.        
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))


def modificarestado3(request):
    estadonuevo = request.GET.get('estadonuevo')
    idtrabajo = request.GET.get('idtrabajo')
    estadonuevo = str(estadonuevo)
    idtrabajo = str(idtrabajo)
    db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
    db.autocommit = True
    cur = db.cursor()
    select = """  
        UPDATE sc_trabajo 
        SET "Tra_Est_id" = %s
        WHERE sc_trabajo."Tra_Id" = %s;  

        """
    print(select)    
    cur.execute(select,(estadonuevo,idtrabajo,))
    cur.close()
    cur = db.cursor()
    select = """  
        select * 
        from 
        sc_trabajo , sc_estado 
        where 
        sc_trabajo."Tra_Est_id" = sc_estado."Est_Id"   

        """
    cur.execute(select,)
    datos_estado = cur.fetchall()
    cur.close()

    db.close()
    return render(request, 'modificarestado.html' , {'datos':datos_estado,'cambios':estadonuevo})
def registrartrabajo(request):
    now = datetime.now()
    dt_ano = now.strftime("%Y")
    dt_mes = now.strftime("%m")
    dt_dia = now.strftime("%d")
    anosig = int(dt_ano) + 5
    stringfecha1 = str(dt_ano+'-'+dt_mes+'-'+dt_dia)
    stringfecha2 = str(str(anosig)+'-'+dt_mes+'-'+dt_dia)
    db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
    db.autocommit = True
    cur = db.cursor()
    select = """  
        select * from sc_estado    

        """
    cur.execute(select,)
    datos_estado = cur.fetchall()
    cur.close()
    cur = db.cursor()
    select = """  
        select sc_vehiculo."Veh_Id",sc_vehiculo."Veh_Mod" from sc_vehiculo   

        """
    cur.execute(select,)
    datos_vehiculo = cur.fetchall()
    cur.close()
    cur = db.cursor()
    select = """  
        select 
        sc_repuesto."Rep_id",sc_repuesto."Rep_Nom",sc_marcarepuesto."Mar_nom" 
        from 
        sc_repuesto, sc_marcarepuesto 
        where 
        sc_repuesto."Rep_Mar_id" = sc_marcarepuesto."Mar_ID"    

        """
    cur.execute(select,)
    datos_repuestos = cur.fetchall()
    cur.close() 
    db.close()
    return render(request, 'registrartrabajo.html',{'datos':datos_estado,'datos2':datos_vehiculo,'datos3':datos_repuestos,'fecha':stringfecha1,'fecha2':stringfecha2})

def crearepuesto(request):
    db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
    db.autocommit = True 
    # AQUI SACAMOS TODAS LAS MARCAS
    cur = db.cursor()
    select = """  
        select sc_marcarepuesto."Mar_ID" from sc_marcarepuesto  

        """
    cur.execute(select)
    datos_marcas = cur.fetchall()

    cur.close()
    cur = db.cursor()
    select = """  
        select * from sc_marcarepuesto  

        """
    cur.execute(select,)
    datos_marcas2 = cur.fetchall()

    cur.close()
    db.close()
    return render(request, 'crearepuesto.html' , {'datos':datos_marcas2})
def crearepuesto2(request):
    try:
        idrepuesto = request.GET.get('idrepuesto')
        nombre = request.GET.get('nombre')
        cantidad = request.GET.get('cantidad')
        idmarca = request.GET.get('idmarca')
        db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
        db.autocommit = True
        cur = db.cursor()
        select = """  
            INSERT INTO sc_repuesto ("Rep_id" , "Rep_Nom" , "Rep_Can" , "Rep_Mar_id")
            VALUES (%s, %s, %s, %s);    

            """
        cur.execute(select,(idrepuesto,nombre,cantidad,idmarca,))
        cur.close()


        cur = db.cursor()
        select = """  
            select 
            sc_repuesto."Rep_Can" , sc_marcarepuesto."Mar_nom" , sc_repuesto."Rep_Nom" , sc_repuesto."Rep_id"  
            from 
            sc_repuesto , sc_marcarepuesto 
            where 
            sc_marcarepuesto."Mar_ID" = sc_repuesto."Rep_Mar_id"   

            """
        cur.execute(select,)
        datos_repuestos = cur.fetchall()
        cur.close()
        db.close()
        creado = "creado exitosamente"
        return render(request, 'registrarrepuesto.html' , {'datos':datos_repuestos,'creado':creado})
    except:
        db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
        db.autocommit = True 
        # AQUI SACAMOS TODAS LAS MARCAS
        cur = db.cursor()
        select = """  
            select sc_marcarepuesto."Mar_ID" from sc_marcarepuesto  

            """
        cur.execute(select)
        datos_marcas = cur.fetchall()

        cur.close()
        cur = db.cursor()
        select = """  
            select * from sc_marcarepuesto  

            """
        cur.execute(select,)
        datos_marcas2 = cur.fetchall()

        cur.close()
        db.close()
        error = "error"
        return render(request, 'crearepuesto.html' , {'datos':datos_marcas2,'error':error})    

def modificarrespuesto2(request):
    try:
        cantidad = request.GET.get('cantidad')
        idrepuesto = request.GET.get('idrepuesto')
        db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
        db.autocommit = True
        cur = db.cursor()
        select = """  
            UPDATE sc_repuesto 
            SET "Rep_Can" =%s
            WHERE "Rep_id" = %s; 

            """
        print(select)    
        cur.execute(select,(cantidad,idrepuesto,))
        cur.close()
        cur = db.cursor()
        select = """  
            select 
            sc_repuesto."Rep_Can" , sc_marcarepuesto."Mar_nom" , sc_repuesto."Rep_Nom" , sc_repuesto."Rep_id"  
            from 
            sc_repuesto , sc_marcarepuesto 
            where 
            sc_marcarepuesto."Mar_ID" = sc_repuesto."Rep_Mar_id"   

            """
        cur.execute(select,)
        datos_repuestos = cur.fetchall()
        cur.close()
        db.close()
        return render(request, 'registrarrepuesto.html' , {'datos':datos_repuestos,'cambios':"transaccion exitosa"})
    except:
        db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
        db.autocommit = True
        cur = db.cursor()
        select = """  
            select 
            sc_repuesto."Rep_Can" , sc_marcarepuesto."Mar_nom" , sc_repuesto."Rep_Nom" , sc_repuesto."Rep_id"  
            from 
            sc_repuesto , sc_marcarepuesto 
            where 
            sc_marcarepuesto."Mar_ID" = sc_repuesto."Rep_Mar_id"   

            """
        cur.execute(select,)
        datos_repuestos = cur.fetchall()
        cur.close()
        db.close()
        error = "error"
        return render(request, 'registrarrepuesto.html' , {'datos':datos_repuestos,'error':error})    

def registrarvehiculo(request):
    db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
    db.autocommit = True
    cur = db.cursor()
    select = """  
        select 
        sc_cliente."Cli_Run",sc_cliente."Cli_Nom",sc_cliente."Cli_Ap_Pat",sc_cliente."Cli_Ap_Mat" 
        from 
        sc_cliente    

        """
    cur.execute(select,)
    datos_cliente = cur.fetchall()
    cur.close()
    cur = db.cursor()
    select = """  
        select * from sc_marca  

        """
    cur.execute(select,)
    datos_marca = cur.fetchall()
    cur.close()

    cur = db.cursor()
    select = """  
        select * from sc_tipo  

        """
    cur.execute(select,)
    datos_tipo = cur.fetchall()
    cur.close()
    db.close()
   
    return render(request, 'registrarvehiculo.html',{'datos':datos_cliente,'datos2':datos_marca,'datos3':datos_tipo})

def registrarvehiculo2(request):
    try:
        idcliente = request.GET.get('idcliente')
        idpatente = request.GET.get('id')
        agno = request.GET.get('agno')
        modelo = request.GET.get('modelo')
        idmarca = request.GET.get('idmarca')
        idtipo = request.GET.get('idtipo')
        db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
        db.autocommit = True
        cur = db.cursor()
        select = """  
            INSERT INTO sc_vehiculo ("Veh_Id" , "Veh_Mod" , "Veh_Mar_id" , "Veh_Tip_id" , "Veh_Agno" , "Veh_Cliente_id" )
            VALUES (%s, %s, %s, %s, %s, %s);   

            """
        cur.execute(select,(idpatente,modelo,idmarca,idtipo,agno,idcliente,))
        cur.close()
        db.close()
        return render(request, 'vista1.html',{'registrovehiculo':modelo,'registrovehiculo2':idpatente})
    except:
        db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
        db.autocommit = True
        cur = db.cursor()
        select = """  
            select 
            sc_cliente."Cli_Run",sc_cliente."Cli_Nom",sc_cliente."Cli_Ap_Pat",sc_cliente."Cli_Ap_Mat" 
            from 
            sc_cliente    

            """
        cur.execute(select,)
        datos_cliente = cur.fetchall()
        cur.close()
        cur = db.cursor()
        select = """  
            select * from sc_marca  

            """
        cur.execute(select,)
        datos_marca = cur.fetchall()
        cur.close()

        cur = db.cursor()
        select = """  
            select * from sc_tipo  

            """
        cur.execute(select,)
        datos_tipo = cur.fetchall()
        cur.close()
        db.close()
        error = "error"
        return render(request, 'registrarvehiculo.html',{'datos':datos_cliente,'datos2':datos_marca,'datos3':datos_tipo,'error':error})
            

def registrartrabajo2(request):
    try:
        idtrabajo = request.GET.get('idtrabajo')
        descripcion = request.GET.get('descripcion')
        calend1 = request.GET.get('calend1')
        calend2 = request.GET.get('calend2')
        estado = request.GET.get('estado')
        vehiculo = request.GET.get('vehiculo')
        repuesto = request.GET.get('repuesto')
        cantidad = request.GET.get('cantidad')
        db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
        db.autocommit = True
        cur = db.cursor()
        select = """  
            INSERT INTO sc_trabajo ("Tra_Id" , "Tra_Des" , "Tra_Fechainicio" , "Tra_Fechafin" , "Tra_Est_id" , "Tra_Vehic_id" )
            VALUES (%s, %s, %s, %s, %s, %s);    
         
            """
        cur.execute(select,(idtrabajo,descripcion,calend1,calend2,estado,vehiculo))
        cur.close()
        cur = db.cursor()
        select = """  
            INSERT INTO sc_tra_rep ( "Trep_Trabajo_id" , "Trep_Repuesto_id" , "Trep_Cant" )
            VALUES (%s, %s, %s);    
      
            """
        cur.execute(select,(idtrabajo,repuesto,cantidad))
        cur.close()
        cur = db.cursor()
        select = """  
            select sc_repuesto."Rep_Can" from sc_repuesto where sc_repuesto."Rep_id" = %s  

            """
        cur.execute(select,(repuesto,))
        datos_marca = cur.fetchall()
        valor = int(datos_marca[0][0])
        print(valor)
        valor = valor - int(cantidad)
        valor = int(valor)
        if valor < 0 :
            valor = 0
        print(valor)    
        cur.close()
        cur = db.cursor()
        select = """  
            UPDATE sc_repuesto 
            SET "Rep_Can" = %s
            WHERE "Rep_id" = %s;  
      
            """
        cur.execute(select,(str(valor),repuesto))
        cur.close()
        db.close()
        return render(request, 'vista1.html',{'idtrabajo':idtrabajo,'vehiculo':vehiculo})
    except:
        db = psycopg2.connect(host="db-postgresql-nyc1-25666-do-user-7789068-0.b.db.ondigitalocean.com", port=25060, database="defaultdb", user="doadmin", password="rmukqrgvx1f6f6ap",sslmode='require')
        db.autocommit = True
        cur = db.cursor()
        select = """  
            select * from sc_estado    

            """
        cur.execute(select,)
        datos_estado = cur.fetchall()
        cur.close()
        cur = db.cursor()
        select = """  
            select sc_vehiculo."Veh_Id",sc_vehiculo."Veh_Mod" from sc_vehiculo   

            """
        cur.execute(select,)
        datos_vehiculo = cur.fetchall()
        cur.close()
        cur = db.cursor()
        select = """  
            select 
            sc_repuesto."Rep_id",sc_repuesto."Rep_Nom",sc_marcarepuesto."Mar_nom" 
            from 
            sc_repuesto, sc_marcarepuesto 
            where 
            sc_repuesto."Rep_Mar_id" = sc_marcarepuesto."Mar_ID"    

            """
        cur.execute(select,)
        datos_repuestos = cur.fetchall()
        cur.close() 
        db.close()
        error = "error"
        return render(request, 'registrartrabajo.html',{'datos':datos_estado,'datos2':datos_vehiculo,'datos3':datos_repuestos,'error':error})
                
    




# Create your views here.
