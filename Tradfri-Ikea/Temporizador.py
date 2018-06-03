import time
import os
import signal
import ConfigParser
import rainbowhat
import sys
import rainbowhat as rh
from tradfri import tradfriActions
from datetime import datetime

#Se obtiene del nanotexto 'tradfri.cfg' los valores de la direccion ip de la pasarela, el apiuser y la apikey.

conf = ConfigParser.ConfigParser()
script_dir = os.path.dirname(os.path.realpath(__file__))
conf.read(script_dir + '/tradfri.cfg')

hubip = conf.get('tradfri','hubip')
apiuser = conf.get('tradfri','apiuser')
apikey = conf.get('tradfri','apikey')

#Variables
bombillas = [65537,65538,131073]
bulbid=0
decimal=0
dia=1
mes=1
year=1
hora_inicial=0
minuto_inicial=0
hora_final=0
minuto_final=0
dia_semana=0
n_semana=0
contador=0
semanal=True
activado=True
dia_activado=False
mes_activado=False
m_inicial_p=False
m_final_p=False
R=[230,0,255,0,255,255,0]
G=[0,255,60,0,0,255,255]
B=[0,0,0,255,191,0,255]

#Metodo para mostrar mediante los leds del rainbow HAT un juego de luces como animacion en el mensaje inicial.
def luces_iniciales():

        num=[6,5,4,3,2,1,0]
        
        rh.rainbow.clear()

        for t in range(2):
                
                for x in num:

                        if t==0:
                                
                                rh.rainbow.set_pixel(x,R[x],G[x],B[x])

                        elif t==1:

                                x=num[x]
                                rh.rainbow.set_pixel(x,R[x],G[x],B[x])
                                
                        rh.rainbow.show()        
                        time.sleep(0.1)
                      
                for x in num:
                        
                        if t==0:
                                rh.rainbow.set_pixel(x,0,0,0)

                        elif t==1:
                                
                                x=num[x]
                                rh.rainbow.set_pixel(x,0,0,0)
                                
                        rh.rainbow.show()
                        time.sleep(0.1)
                        
        for i in range(3):
                
                rh.rainbow.set_pixel(0,R[0],G[0],B[0])
                rh.rainbow.set_pixel(1,R[1],G[1],B[1])
                rh.rainbow.set_pixel(2,R[2],G[2],B[2])
                rh.rainbow.set_pixel(3,R[3],G[3],B[3])
                rh.rainbow.set_pixel(4,R[4],G[4],B[4])
                rh.rainbow.set_pixel(5,R[5],G[5],B[5])
                rh.rainbow.set_pixel(6,R[6],G[6],B[6])
                rh.rainbow.show()
                time.sleep(0.2)
                
                if i<2:
                        rh.rainbow.clear()
                        rh.rainbow.show()
                        time.sleep(0.2)

#Metodo para pintar los leds del Rainbow HAT de 3 maneras distintas dependiendo la bombilla seleccionada. Si se selecciona la bombilla con el id=65538 entonces parpadean la mitad de los leds hacia la derecha,
#si por el contrario, el id=65537 parpadean la mitad de los leds de la izquierda, y si son ambas bombillas parpadean todo el bloque de leds del 0 al 86.                        
def luz_tipo_bombilla(bulbid):

        if bulbid == 65538:

                for i in range(3):
                
                        rh.rainbow.set_pixel(0,R[0],G[0],B[0])
                        rh.rainbow.set_pixel(1,R[1],G[1],B[1])
                        rh.rainbow.set_pixel(2,R[2],G[2],B[2])
                        rh.rainbow.set_pixel(3,R[3],G[3],B[3])
                        rh.rainbow.set_pixel(4,0,0,0)
                        rh.rainbow.set_pixel(5,0,0,0)
                        rh.rainbow.set_pixel(6,0,0,0)
                        rh.rainbow.show()
                        time.sleep(0.2)
                        
                        if i<2:
                                
                                rh.rainbow.clear()
                                rh.rainbow.show()
                                time.sleep(0.2)

        elif bulbid== 65537:

                for i in range(3):
                
                        rh.rainbow.set_pixel(0,0,0,0)
                        rh.rainbow.set_pixel(1,0,0,0)
                        rh.rainbow.set_pixel(2,0,0,0)
                        rh.rainbow.set_pixel(3,R[3],G[3],B[3])
                        rh.rainbow.set_pixel(4,R[4],G[4],B[4])
                        rh.rainbow.set_pixel(5,R[5],G[5],B[5])
                        rh.rainbow.set_pixel(6,R[6],G[6],B[6])
                        rh.rainbow.show()
                        time.sleep(0.2)
                        
                        if i<2:
                                
                                rh.rainbow.clear()
                                rh.rainbow.show()
                                time.sleep(0.2)

        else:
                for i in range(3):
                
                        rh.rainbow.set_pixel(0,R[0],G[0],B[0])
                        rh.rainbow.set_pixel(1,R[1],G[1],B[1])
                        rh.rainbow.set_pixel(2,R[2],G[2],B[2])
                        rh.rainbow.set_pixel(3,R[3],G[3],B[3])
                        rh.rainbow.set_pixel(4,R[4],G[4],B[4])
                        rh.rainbow.set_pixel(5,R[5],G[5],B[5])
                        rh.rainbow.set_pixel(6,R[6],G[6],B[6])
                        rh.rainbow.show()
                        time.sleep(0.2)
                        
                        if i<2:
                                
                                rh.rainbow.clear()
                                rh.rainbow.show()
                                time.sleep(0.2)

#Metodo que pinta de forma distinta los leds dependiendo el temporizador seleccionado.
#Si se ha elegido la programacion diaria, es decir, channel = 0, entonces los leds se pintan uno a uno borrandose el que se ha pintado anteriormente, y al final pintandose todos.
#Si se ha elegido programacion semanal, es decir, channel = 1, entonces los leds se pintan uno a uno hasta pintarse todo el bloque, sin borrarse como en la programacion diaria.
#Y si se ha elegido programacion mensual, entonces parpadea todo el bloque.
def luz_tipo_temporizador(channel):
        
        rh.rainbow.clear()
        rh.rainbow.show()
        num=[6,5,4,3,2,1,0]
        
        if channel==0:

                for x in num:

                                rh.rainbow.set_pixel(x,R[x],G[x],B[x])
                                rh.rainbow.show()
                                time.sleep(0.2)
                                rh.rainbow.clear()
                                rh.rainbow.show()
                                  
                rh.rainbow.set_pixel(0,R[0],G[0],B[0])
                rh.rainbow.set_pixel(1,R[1],G[1],B[1])
                rh.rainbow.set_pixel(2,R[2],G[2],B[2])
                rh.rainbow.set_pixel(3,R[3],G[3],B[3])
                rh.rainbow.set_pixel(4,R[4],G[4],B[4])
                rh.rainbow.set_pixel(5,R[5],G[5],B[5])
                rh.rainbow.set_pixel(6,R[6],G[6],B[6])
                rh.rainbow.show()
                time.sleep(0.2)
                
        elif channel==1:

                  for x in num:

                                rh.rainbow.set_pixel(x,R[x],G[x],B[x])
                                rh.rainbow.show()
                                time.sleep(0.2)
                
                
                
        else:

                for i in range(3):
                                
                                rh.rainbow.set_pixel(0,R[0],G[0],B[0])
                                rh.rainbow.set_pixel(1,R[1],G[1],B[1])
                                rh.rainbow.set_pixel(2,R[2],G[2],B[2])
                                rh.rainbow.set_pixel(3,R[3],G[3],B[3])
                                rh.rainbow.set_pixel(4,R[4],G[4],B[4])
                                rh.rainbow.set_pixel(5,R[5],G[5],B[5])
                                rh.rainbow.set_pixel(6,R[6],G[6],B[6])
                                rh.rainbow.show()
                                time.sleep(0.2)
                                
                                if i<2:
                                        
                                              rh.rainbow.clear()
                                              rh.rainbow.show()
                                              time.sleep(0.2)

        
        
#Metodo para mostrar al usuario un mensaje por el display informandole que bombilla/s quiere utilizar en el temporizador. Y un escuchador para saber que boton se ha pulsado y asi saber que
#temporizador ha escogido el usuario.                                                
def eleccion_bombillas():

        mensaje ="HOLA"
        display_mensaje(mensaje,0)
        luces_iniciales()
        mensaje ="ELIGE LA BOMBILLA*A->BOMBILLA 1*B->BOMBILLA 2*C->AMBAS BOMBILLAS    " 
        scroll_mensaje(mensaje)
        
        mensaje ="ABoC"
        display_mensaje(mensaje,0)
                
        #Escuchador para saber que boton se ha pulsado, si es el boton A, entonces configuramos la bombilla con el id=65537, si es el boton B configuramos la bombilla con el id=65538, y por ultimo,
        #si se ha seleccionado el boton C se seleccionaran el conjunto de bombillas cuyo id sera el del grupo que en nuestro caso es 131073
        @rainbowhat.touch.press()
        def touch(channel):
                
                  global bulbid, bombillas

                  luz_boton_on(channel)
                  luz_boton_off()

                  if channel==0:
                                        
                          bulbid=bombillas[0]
                          luz_tipo_bombilla(bulbid)
                          tipo_temporizador()
                                        

                  elif channel==1:
                          
                          bulbid=bombillas[1]
                          luz_tipo_bombilla(bulbid)
                          tipo_temporizador()
                
                                        
                  else:                   

                          bulbid=bombillas[2]
                          luz_tipo_bombilla(bulbid)
                          tipo_temporizador()
                                        

#Metodo para mostrar por display un mensaje con desplazamiento
def scroll_mensaje(mensaje):
        
        for w in mensaje:

                mensaje = mensaje[1:len(mensaje)] + mensaje[0]
                rainbowhat.display.print_str(mensaje)
                rainbowhat.display.show()
                time.sleep(0.2)                                                       

#Metodo para mostrar por display un mensaje sin desplazamiento. Si al llamar al metodo la segunda variable que se le pasa por parametro es distinta de 0, se mostrara en el display un punto decimal
#que sera para el menu si decimal es igual a 1, o para el reloj si es distinto de 0 y 1.                
def display_mensaje(mensaje,decimal):

        if decimal==0: 
                                
                rainbowhat.display.print_str(mensaje)
                rainbowhat.display.show() 
                time.sleep(0.2)
                
        elif decimal==1:
                
                rainbowhat.display.print_str(mensaje)
                rainbowhat.display.set_decimal(0,True)
                rainbowhat.display.show() 
                time.sleep(0.2)
                
        else:

                rainbowhat.display.print_str(mensaje)
                rainbowhat.display.set_decimal(1,True)
                rainbowhat.display.show() 
                time.sleep(0.2)
                
#Metodo para encender el led del boton que se haya pulsado y hacer un zumbido piezoelectrico.
def luz_boton_on(channel):
                                              
          if channel == 0:
                     rainbowhat.lights.rgb(1,0,0)
                     rh.buzzer.midi_note(65,0.2) 
                        
          elif channel == 1:

                     rainbowhat.lights.rgb(0,1,0)
                     rh.buzzer.midi_note(60,0.2) 

          else:

                     rainbowhat.lights.rgb(0,0,1)
                     rh.buzzer.midi_note(75,0.2)

#Metodo para apagar el led del boton que se ha pulsado despues de haberse encendido.  
def luz_boton_off():
        
              time.sleep(0.15)   
              rainbowhat.lights.rgb(0,0,0)

#Metodo para encender una o varias bombillas dependiendo el identificador que se le pase por uno de los parametros que contiene el metodo.                        
def switch_on(hubip, apiuser, apikey, bulbid):
        
        if bulbid!=131073:
                
                tradfriActions.tradfri_power_light(hubip, apiuser, apikey, bulbid, 'on')

	elif bulbid==131073:
                
                tradfriActions.tradfri_power_group(hubip,apiuser,apikey, bulbid ,'on')
                
#Metodo para apagar una o varias bombillas dependiendo el identificador que se le pase por uno de los parametros que contiene el metodo. 
def switch_off(hubip, apiuser, apikey, bulbid):
        
        if bulbid!=131073:
                
                tradfriActions.tradfri_power_light(hubip, apiuser, apikey, bulbid, 'off')
                
        elif bulbid==131073:
                
                tradfriActions.tradfri_power_group(hubip, apiuser, apikey, bulbid, "off")

#Metodo que le muestra al usuario un mensaje para que elija entre los 3 tipos de temporizadores: Diario, Semanal o Mensual.
def tipo_temporizador():
        
        mensaje ="ELIGE ENTRE 3 OPCIONES*A TEMPORIZADOR DIARIO*B TEMPORIZADOR SEMANAL*C TEMPORIZADOR MENSUAL    "       
        scroll_mensaje(mensaje)
                        
        mensaje ="ABoC"
        display_mensaje(mensaje,0)
                
        @rainbowhat.touch.press()
        def touch(channel):

                global semanal, dia_activado
                
                luz_boton_on(channel)
                luz_boton_off()

                if channel==0:
                        
                       semanal=False                                      
                       display_mensaje("1DIA",1)
                       time.sleep(1.0)
                       luz_tipo_temporizador(channel)
                       elegir_dia(dia_activado)

                elif channel==1:
                                        
                       semanal=True
                       display_mensaje("2SEM",1)
                       time.sleep(1.0)
                       luz_tipo_temporizador(channel)
                       elegir_dia(dia_activado)
                                        
                else:
                        
                       display_mensaje("3MES",1)
                       time.sleep(1.0)
                       luz_tipo_temporizador(channel)
                       elegir_mes(dia_activado,semanal)
                       
#Metodo donde se elige el dia que quiere el usuario utilizar el temporizador. Con los botones B y C decrementan y aumentan el dia respectivamente, y con el boton A pasa a la siguiente fase.
def elegir_dia(dia_activado):
        
                rh.rainbow.clear()
                rh.rainbow.show()
        
                rh.rainbow.set_pixel(0,R[0],G[0],B[0])
                rh.rainbow.show()
                time.sleep(0.2)
                mensaje="ELIGE EL DIA CON B Y C    "
                scroll_mensaje(mensaje)

                rainbowhat.display.clear()
                valor="{dia}".format(dia=dia)
                
                
                if 0<dia<10:

                          valor="D- {dia}".format(dia=dia)
                          display_mensaje(valor,0)
                          time.sleep(0.2)
                                       
                else:
                          valor="D-{dia}".format(dia=dia)
                          display_mensaje(valor,0)
                          time.sleep(0.2)
               

                @rainbowhat.touch.C.press()
                def touch_c(channel):
                        
                        global dia
                        global dia_activado
                        
                        luz_boton_on(channel)
                        luz_boton_off()

                        if 0<dia<31:
                                        
                                 dia=dia + 1

                                 if 0<dia<10:

                                          valor="D- {dia}".format(dia=dia)
                                          display_mensaje(valor,0)
                                          time.sleep(0.2)

                                 else:

                                          valor="D-{dia}".format(dia=dia)
                                          display_mensaje(valor,0)
                                          time.sleep(0.2)

                                 dia_activado=True
                                        
                        else:

                                 mensaje="ERROR ES EL MAXIMO****"
                                 scroll_mensaje(mensaje)
                                 dia=31
                                 valor="{dia}".format(dia=dia)
                                        
                                 if 0<dia<10:
                                                
                                       valor="D- {dia}".format(dia=dia)
                                       display_mensaje(valor,0)
                                       time.sleep(0.2)
                                               
                                 else:

                                       valor="D-{dia}".format(dia=dia)
                                       display_mensaje(valor,0)
                                       time.sleep(0.2)
                                       
                                 dia_activado=True
                        
                @rainbowhat.touch.B.press()
                def touch_b(channel):
                        
                        global contador
                        global dia
                        global dia_activado
                        
                        contador=0
                        luz_boton_on(channel)
                        luz_boton_off()
                        rainbowhat.display.clear()
                        
                        if 1<dia<32:

                                dia=dia - 1

                                if 0<dia<10:

                                       valor="D- {dia}".format(dia=dia)
                                       display_mensaje(valor,0)
                                       time.sleep(0.2)
                                       
                                else:
                                        
                                       valor="D-{dia}".format(dia=dia)
                                       display_mensaje(valor,0)
                                       time.sleep(0.2)
                                       
                                dia_activado=True 
                                        
                        else:
                                
                                contador=1
                                mensaje="ERROR ES EL MINIMO****"
                                scroll_mensaje(mensaje)
                                dia=1
                                valor="{dia}".format(dia=dia)

                                if 0<dia<10:
                                       valor="D- {dia}".format(dia=dia)
                                       display_mensaje(valor,0)
                                       time.sleep(0.2)

                                else:
                                       valor="D-{dia}".format(dia=dia)
                                       display_mensaje(valor,0)
                                       time.sleep(0.2)
                                dia_activado=True
                        
                @rainbowhat.touch.A.press()
                def touch_a(channel):
                        
                        global dia_activado
                        global semanal

                        luz_boton_on(channel)
                        luz_boton_off()
                       
                        elegir_mes(dia_activado,semanal)

#Metodo donde se elige el mes que quiere el usuario utilizar el temporizador. Con los botones B y C decrementan y aumentan el mes respectivamente, y con el boton A pasa a la siguiente fase.
def elegir_mes(dia_activado, semanal):

                          if dia_activado==False:
                                  rh.rainbow.clear()
                                  rh.rainbow.show()      
                                  rh.rainbow.set_pixel(0,R[0],G[0],B[0])      
                                  rh.rainbow.set_pixel(1,R[1],G[1],B[1])
                                  
                          else:

                                  rh.rainbow.set_pixel(1,R[1],G[1],B[1])
                                  
                          rh.rainbow.show()
                          time.sleep(0.2)
                        
                        
                          mensaje="ELIGE MES    "
                          
                          scroll_mensaje(mensaje)
                                                 
                          if 0<mes<10:

                                       valor="M- {mes}".format(mes=mes)
                                       display_mensaje(valor,0)
                                       time.sleep(0.2)

                          else:   

                                       valor="M-{mes}".format(mes=mes)
                                       display_mensaje(valor,0)
                                       time.sleep(0.2) 

                          @rainbowhat.touch.B.press()
                          def touch_b(channel):
                                  
                                    global dia
                                    global mes
                                    
                                    luz_boton_on(channel)
                                    luz_boton_off()

                                    if 1<mes<13:
                                            
                                                mes=mes - 1
                                                valor="{mes}".format(mes=mes)
                                                rainbowhat.display.clear()

                                                if 0<mes<10:

                                                       valor="M- {mes}".format(mes=mes)
                                                       display_mensaje(valor,0)
                                                       time.sleep(0.2)

                                                else:   
                                                       valor="M-{mes}".format(mes=mes)
                                                       display_mensaje(valor,0)
                                                       time.sleep(0.2)

                                    else:

                                                mensaje="ERROR ES EL MINIMO    "
                                                scroll_mensaje(mensaje)
                                                mes=1
                                                
                                                if 0<mes<10:
                                                       valor="M- {mes}".format(mes=mes)
                                                       display_mensaje(valor,0)
                                                       time.sleep(0.2)
                                                else:   
                                                       valor="M-{mes}".format(mes=mes)
                                                       display_mensaje(valor,0)
                                                       time.sleep(0.2)
                                                  
                          @rainbowhat.touch.C.press()
                          def touch_c(channel):

                                global mes
                                global contador

                                luz_boton_on(channel)
                                luz_boton_off()
                                
                                if 0<mes<12:
                                                
                                                mes=mes + 1
                                                rainbowhat.display.clear()

                                                if 0<mes<10:
                                                        
                                                       valor="M- {mes}".format(mes=mes)
                                                       display_mensaje(valor,0)
                                                       time.sleep(0.2)
                                                       
                                                else:   
                                                       valor="M-{mes}".format(mes=mes)
                                                       display_mensaje(valor,0)
                                                       time.sleep(0.2)
                                                        

                                else:
                                        
                                                mensaje="ERROR ES EL MAXIMO    "
                                                scroll_mensaje(mensaje)
                                                mes=12
                                                rainbowhat.display.clear()
                                                
                                                if 0<mes<10:
                                                        
                                                       valor="M- {mes}".format(mes=mes)
                                                       display_mensaje(valor,0)
                                                       time.sleep(0.2)
                                                       
                                                else:   
                                                       valor="M-{mes}".format(mes=mes)
                                                       display_mensaje(valor,0)
                                                       time.sleep(0.2)
                                                       
                          @rainbowhat.touch.A.press()
                          def touch_a(channel):
                                  
                                        global dia_activado
                                        global mes_activado
                                        global semanal
                                        
                                        luz_boton_on(channel)
                                        luz_boton_off()
                                        
                                        if dia_activado==False:
                                              
                                                semanal=False
                                                
                                        mes_activado=True
                                        temp_eleccion(dia_activado,mes_activado,semanal)                          

#Metodo donde se establece tanto la hora y minuto inicial como la hora y minuto final. Ademas se realizan una serie de comprobaciones como que Febrero solo tenga 28 dias 
#o que si el usuario ha elegido el temporizador semanal el dia seleccionado debe ser lunes sino debera de escoger otro dia.
def temp_eleccion(dia_activado,mes_activado,semanal):
               
                                 global hora_inicial
                                 global year, dia, mes
                                 global dia_semana
                                 global n_semana
                                 
                                 t=datetime.now()
                                 mes_sistema=t.month
                                 year=t.year
                                 
                                 if (mes==4 or mes==6 or mes==9 or mes==11) and dia==31:

                                                 mensaje="EL DIA NO ES VALIDO    "
                                                 scroll_mensaje(mensaje)
                                                 dia_activado=False
                                                 mes_activado=False
                                                 elegir_dia(dia_activado)
                                                 
                                 elif mes==2 and dia>28:
                                                 
                                                mensaje="EL DIA NO ES VALIDO    "
                                                scroll_mensaje(mensaje)
                                                dia_activado=False
                                                mes_activado=False
                                                elegir_dia(dia_activado)
                                                
                                 else:
                                                 
                                         if semanal==True:
                                                 
                                                 fecha_semanal=datetime(year,mes,dia,0,0,0)
                                                 tupla_valores=datetime.isocalendar(fecha_semanal)
                                                 dia_semana=tupla_valores[2]
                                                 n_semana=tupla_valores[1]
                                           
                                                 if dia_semana!=1:
                                                         
                                                         mensaje="EL DIA INTRODUCIDO NO ES LUNES    "
                                                         scroll_mensaje(mensaje)
                                                         dia_activado=False
                                                         mes_activado=False
                                                         elegir_dia(dia_activado)
                                                         
                                                 else:
                                                         
                                                         rh.rainbow.set_pixel(2,R[2],G[2],B[2])
                                                         rh.rainbow.show()
                                                         time.sleep(0.2)
                                                         mensaje="SELECCIONE HORA INICIAL    "
                                                         scroll_mensaje(mensaje)
                                                         rainbowhat.display.clear()
                                                                                                                          
                                                         if -1<hora_inicial<10:
                                                                 
                                                                      valor="H- {hora_inicial}".format(hora_inicial=hora_inicial)
                                                                      rainbowhat.display.clear()
                                                                      display_mensaje(valor,0)
                                                                      time.sleep(0.2)

                                                         else:   
                                                                      valor="H-{hora_inicial}".format(hora_inicial=hora_inicial)
                                                                      display_mensaje(valor,0)
                                                                      time.sleep(0.2)
                                                         
                                                                                                                                         
                                                        
                                         elif semanal==False:

                                                 rh.rainbow.set_pixel(2,R[2],G[2],B[2])
                                                 rh.rainbow.show()
                                                 time.sleep(0.2)
                                                 mensaje="SELECCIONE HORA INICIAL    "
                                                 scroll_mensaje(mensaje)
                                                 rainbowhat.display.clear()
                                                         
                                                 if -1<hora_inicial<10:

                                                                valor="H- {hora_inicial}".format(hora_inicial=hora_inicial)
                                                                rainbowhat.display.clear()
                                                                display_mensaje(valor,0)
                                                                time.sleep(0.2)

                                                 else:   
                                                                valor="H-{hora_inicial}".format(hora_inicial=hora_inicial)
                                                                display_mensaje(valor,0)
                                                                time.sleep(0.2)

                                 if mes<mes_sistema:
                                         
                                         year=year+1
                                         
                                 if dia_activado==True or mes_activado==True:        

                                         @rainbowhat.touch.C.press()
                                         def touch_C(channel):
                                                 
                                                global hora_inicial

                                                luz_boton_on(channel)
                                                luz_boton_off()
                                                                                              
                                                hora_inicial=hora_inicial + 1
                                                rainbowhat.display.clear()

                                                if -1<hora_inicial<24:

                                                        if -1<hora_inicial<10:
                                                                
                                                               valor="H- {hora_inicial}".format(hora_inicial=hora_inicial)
                                                               rainbowhat.display.clear()
                                                               display_mensaje(valor,0)
                                                               time.sleep(0.2)

                                                        else:   

                                                               valor="H-{hora_inicial}".format(hora_inicial=hora_inicial)
                                                               display_mensaje(valor,0)
                                                               time.sleep(0.2)
                                                                
                                                else:

                                                                hora_inicial=0
                                                                valor="H- {hora_inicial}".format(hora_inicial=hora_inicial)
                                                                rainbowhat.display.clear()
                                                                display_mensaje(valor,0)
                                                                time.sleep(0.2)
                                                                
                                         @rainbowhat.touch.B.press()
                                         def touch_b(channel):
                                                 
                                                 global minuto_inicial

                                                 luz_boton_on(channel)
                                                 luz_boton_off()

                                                 rh.rainbow.set_pixel(3,R[3],G[3],B[3])
                                                 rh.rainbow.show()
                                                 time.sleep(0.2)
                                                 
                                                 mensaje="SELECCIONE MINUTO INICIAL    "
                                                 scroll_mensaje(mensaje)
                                                                                                          
                                                 rainbowhat.display.clear()
                                         
                                                 if -1<minuto_inicial<10:
                                                         
                                                               valor="M- {minuto_inicial}".format(minuto_inicial=minuto_inicial)
                                                               rainbowhat.display.clear()
                                                               display_mensaje(valor,0)
                                                               time.sleep(0.2)

                                                 else:   

                                                               valor="M-{minuto_inicial}".format(minuto_inicial=minuto_inicial)
                                                               display_mensaje(valor,0)
                                                               time.sleep(0.2)
                                         
                                                 @rainbowhat.touch.C.press()
                                                 def touch_c(channel):
                                                         
                                                        global minuto_inicial

                                                        luz_boton_on(channel)
                                                        luz_boton_off()
                                                                                                      
                                                        minuto_inicial=minuto_inicial + 5
                                                        rainbowhat.display.clear()

                                                        if -1<minuto_inicial<57:

                                                                if -1<minuto_inicial<10:

                                                                       valor="M- {minuto_inicial}".format(minuto_inicial=minuto_inicial)
                                                                       rainbowhat.display.clear()
                                                                       display_mensaje(valor,0)
                                                                       time.sleep(0.2)

                                                                else:   

                                                                       valor="M-{minuto_inicial}".format(minuto_inicial=minuto_inicial)
                                                                       display_mensaje(valor,0)
                                                                       time.sleep(0.2)
                                                                        
                                                        else:

                                                                        minuto_inicial=0
                                                                        valor="M- {minuto_inicial}".format(minuto_inicial=minuto_inicial)
                                                                        rainbowhat.display.clear()
                                                                        display_mensaje(valor,0)
                                                                        time.sleep(0.2)
                                       
                                         @rainbowhat.touch.A.press()  
                                         def touch_a(channel):
                                                 
                                                 global hora_final
                                                 
                                                 luz_boton_on(channel)
                                                 luz_boton_off()
                                                 rh.rainbow.set_pixel(3,R[3],G[3],B[3])
                                                 rh.rainbow.set_pixel(4,R[4],G[4],B[4])
                                                 rh.rainbow.show()
                                                 time.sleep(0.2)
                                                 mensaje="SELECCIONE HORA FINAL    "
                                                 scroll_mensaje(mensaje)
                                                 
                                                 rainbowhat.display.clear()
                                         
                                                 if -1<hora_final<10:
                                                         
                                                               valor="H- {hora_final}".format(hora_final=hora_final)
                                                               rainbowhat.display.clear()
                                                               display_mensaje(valor,0)
                                                               time.sleep(0.2)

                                                 else:   

                                                               valor="H-{hora_final}".format(hora_final=hora_final)
                                                               display_mensaje(valor,0)
                                                               time.sleep(0.2)
                                                               
                                                 @rainbowhat.touch.C.press()
                                                 def touch_C(channel):
                                                         
                                                        global hora_final

                                                        luz_boton_on(channel)
                                                        luz_boton_off()
                                                                                                      
                                                        hora_final=hora_final + 1
                                                        rainbowhat.display.clear()

                                                        if -1<hora_final<24:

                                                                if -1<hora_final<10:

                                                                       valor="H- {hora_final}".format(hora_final=hora_final)
                                                                       rainbowhat.display.clear()
                                                                       display_mensaje(valor,0)
                                                                       time.sleep(0.2)

                                                                else:   

                                                                       valor="H-{hora_final}".format(hora_final=hora_final)
                                                                       display_mensaje(valor,0)
                                                                       time.sleep(0.2)
                                                                        
                                                        else:

                                                                       hora_final=0
                                                                       valor="H- {hora_final}".format(hora_final=hora_final)
                                                                       rainbowhat.display.clear()
                                                                       display_mensaje(valor,0)
                                                                       time.sleep(0.2)
                                                                       
                                                 @rainbowhat.touch.B.press()
                                                 def touch_b(channel):
                                                         
                                                         global minuto_final

                                                         luz_boton_on(channel)
                                                         luz_boton_off()
                                                         rh.rainbow.set_pixel(5,R[5],G[5],B[5])
                                                         rh.rainbow.show()
                                                         time.sleep(0.2)

                                                         mensaje="SELECCIONE MINUTO FINAL    "
                                                         scroll_mensaje(mensaje)                                                         
                                                                 
                                                         rainbowhat.display.clear()
                                         
                                                         if -1<minuto_final<10:
                                                                 
                                                               valor="M- {minuto_final}".format(minuto_final=minuto_final)
                                                               rainbowhat.display.clear()
                                                               display_mensaje(valor,0)
                                                               time.sleep(0.2)

                                                         else:   

                                                               valor="M-{minuto_final}".format(minuto_final=minuto_final)
                                                               display_mensaje(valor,0)
                                                               time.sleep(0.2)
                                         

                                                         @rainbowhat.touch.C.press()
                                                         def touch_c(channel):
                                                                 
                                                                global contador_diario
                                                                global minuto_final

                                                                luz_boton_on(channel)
                                                                luz_boton_off()
                                                                                                              
                                                                minuto_final=minuto_final + 5
                                                                rainbowhat.display.clear()

                                                                if -1<minuto_final<57:

                                                                        if -1<minuto_final<10:

                                                                               valor="M- {minuto_final}".format(minuto_final=minuto_final)
                                                                               rainbowhat.display.clear()
                                                                               display_mensaje(valor,0)
                                                                               time.sleep(0.2)

                                                                        else:   

                                                                               valor="M-{minuto_final}".format(minuto_final=minuto_final)
                                                                               display_mensaje(valor,0)
                                                                               time.sleep(0.2)
                                                                                
                                                                else:

                                                                                minuto_final=0
                                                                                valor="M- {minuto_final}".format(minuto_final=minuto_final)
                                                                                rainbowhat.display.clear()
                                                                                display_mensaje(valor,0)
                                                                                time.sleep(0.2)
                                                 @rainbowhat.touch.A.press()
                                                 def touch_a(channel):
                                                         
                                                       global minuto_final, hora_final, hora_inicial, minuto_inicial
                                                       global mes
                                                       global year
                                                       global dia

                                                       luz_boton_on(channel)
                                                       luz_boton_off()

                                                       if semanal==True:
                                                               
                                                               p_semanal()

                                                       elif dia_activado==True and mes_activado==True and semanal==False:
                                                               
                                                                p_diaria()

                                                       else:
                                                               p_mensual()

#Metodo que se le llama cuando el temporizador diario ha sido activado. En este metodo se ejecuta el encendido y apagado de las bombillas en el dia y hora establecido.     

def p_diaria():

               global activado
               global bulbid

               rh.rainbow.set_pixel(5,R[5],G[5],B[5])
               rh.rainbow.set_pixel(6,R[6],G[6],B[6])
               rh.rainbow.show()
               time.sleep(0.2)
               mensaje="TEMPORIZADOR DIARIO ACTIVADO    DIA->{dia}/{mes}/{year}    ".format(dia=dia,mes=mes,year=year)
               scroll_mensaje(mensaje)
               rainbowhat.display.clear()
               ajustar_tiempo()
               
               while activado==True:
                                                         
                          t=datetime.now()
                          hora_sistema=t.hour
                          minuto_sistema=t.minute
                                                        
                          if (t.hour==hora_inicial and t.minute==minuto_inicial):
                                                                 
                                    switch_on(hubip, apiuser, apikey, bulbid)
                                                                         
                                    while activado==True:
                                                                                 
                                           t=datetime.now()
                                           hora_sistema=t.hour
                                           minuto_sistema=t.minute
                                           tiempo_sistema(hora_sistema,minuto_sistema)
                                                                                 
                                           if(t.hour==hora_final and t.minute==minuto_final):

                                                             switch_off(hubip,apiuser, apikey,bulbid)
                                                             activado=False
                          tiempo_sistema(hora_sistema,minuto_sistema)
             
               final()
               
#Metodo que se le llama cuando el temporizador semanal ha sido activado. En este metodo se ejecuta el encendido y apagado de las bombillas durante la semana y hora establecida.                                           
def p_semanal():
        
        global activado
        global n_semana
        global dia_semana
        global bulbid

        rh.rainbow.set_pixel(5,R[5],G[5],B[5])
        rh.rainbow.set_pixel(6,R[6],G[6],B[6])
        rh.rainbow.show()
        time.sleep(0.2)
        mensaje="TEMPORIZADOR SEMANAL ACTIVADO    SEMANA->{n_semana}  DIA->{dia}/{mes}/{year}    ".format(n_semana=n_semana,dia=dia,mes=mes,year=year)
        scroll_mensaje(mensaje)
        rainbowhat.display.clear()
        ajustar_tiempo()
        activo=False
        numero=n_semana
        contador=0
        print("numero",numero)
        print("n_semana",n_semana)

        while activado==True:
                                                                         
                               t=datetime.now()
                               fecha_semanal=datetime(year,mes,dia,0,0,0)
                               tupla_valores=datetime.isocalendar(fecha_semanal)
                               dia_semana=tupla_valores[2]
                               n_semana=tupla_valores[1]
                               hora_sistema=t.hour
                               minuto_sistema=t.minute
                               print("numero1",numero)
                               print("n_semana1",n_semana)

                               if (n_semana==numero and t.hour==hora_inicial and t.minute==minuto_inicial):
                               
                                          switch_on(hubip, apiuser, apikey, bulbid)
                                          activo=True
                                          contador=1
                                          
                                          while activo==True:

                                                          t=datetime.now()
                                                          hora_sistema=t.hour
                                                          minuto_sistema=t.minute
                                                          tiempo_sistema(hora_sistema,minuto_sistema)
                                                         
                                                          if(n_semana==numero and t.hour==hora_final and t.minute==minuto_final):
                                                                        
                                                                        switch_off(hubip,apiuser, apikey,bulbid)
                                                                        numero=15
                                                                        activo=False
                               elif (n_semana!=numero and contador==1):
                                        
                                        activado=False
                                                                        
                            

                               tiempo_sistema(hora_sistema,minuto_sistema)
        final()
             
#Metodo que se le llama cuando el temporizador mensual ha sido activado. En este metodo se ejecuta el encendido y apagado de las bombillas en el mes y hora establecida.                               
def p_mensual():
        
        global activado,mes
        global n_semana
        global dia_semana
        global bulbid

        rh.rainbow.set_pixel(5,R[5],G[5],B[5])
        rh.rainbow.set_pixel(6,R[6],G[6],B[6])
        rh.rainbow.show()
        time.sleep(0.2)
        mensaje="TEMPORIZADOR MENSUAL ACTIVADO EN EL MES->{mes}/{year}    ".format(mes=mes,year=year)

        scroll_mensaje(mensaje)
        rainbowhat.display.clear()
        ajustar_tiempo()
        
        activo=False
        contador=0

        while activado==True:
                                                                         
                               t=datetime.now()
                               mes_sistema=t.month
                               hora_sistema=t.hour
                               minuto_sistema=t.minute

                               if (mes_sistema==mes and t.hour==hora_inicial and t.minute==minuto_inicial):
                                          
                                          switch_on(hubip, apiuser, apikey, bulbid)
                                          activo=True
                                          contador=1
                                          
                                          while activo==True:

                                                          t=datetime.now()
                                                          hora_sistema=t.hour
                                                          minuto_sistema=t.minute
                                                          mes_sistema=t.month
                                                          tiempo_sistema(hora_sistema,minuto_sistema)
                                                          
                                                          if(mes_sistema==mes and t.hour==hora_final and t.minute==minuto_final):
                                                                        mes=5
                                                                        switch_off(hubip,apiuser, apikey,bulbid)
                                                                        activo=False
                                                                        
                               elif (mes_sistema!=mes and contador==1):
                                        
                                        activado=False
                                                                        

                               tiempo_sistema(hora_sistema, minuto_sistema)
        final()

#Metodo para mostrar por el display la hora correcta cuando la hora inicial y final seleccionada es en punto.  
def ajustar_tiempo():

               global m_inicial_p, m_final_p
               global minuto_inicial, minuto_final

               if minuto_inicial==0 or minuto_inicial==5:
                                              
                       m_inicial_p =True
                                      
               if minuto_final==0 or minuto_final==5:
                       
                       m_final_p=True
                
               if m_inicial_p==True:

                        mensaje="HORA INICIAL *{hora_inicial}-0{minuto_inicial}    ".format(hora_inicial=hora_inicial,minuto_inicial=minuto_inicial)
               else:
                        
                       mensaje="HORA INICIAL *{hora_inicial}-{minuto_inicial}    ".format(hora_inicial=hora_inicial,minuto_inicial=minuto_inicial)

               if m_final_p==True:
                        
                        mensaje1="HORA FINAL *{hora_final}-0{minuto_final}    ".format(hora_final=hora_final,minuto_final=minuto_final)
                
               else:
                       
                       mensaje1="HORA FINAL {hora_final}-{minuto_final}    ".format(hora_final=hora_final,minuto_final=minuto_final)
     

               scroll_mensaje(mensaje)
               scroll_mensaje(mensaje1)

#Metodo para mostrar por el display la hora correcta cuando la hora del sistema es en punto.                        
def tiempo_sistema(hora_sistema, minuto_sistema):
        
        if minuto_sistema<10:
                
                 valor="{hora_sistema}0{minuto_sistema}".format(hora_sistema=hora_sistema,minuto_sistema=minuto_sistema)
                 
        else:
                 valor="{hora_sistema}{minuto_sistema}".format(hora_sistema=hora_sistema,minuto_sistema=minuto_sistema)

        display_mensaje(valor,2)

#Metodo para indicar que el temporizador se ha acabado.
def final():

        mensaje="FIN DEL TEMPORIZADOR    "
        scroll_mensaje(mensaje)
        sys.exit(0)

#Comienza el programa                                                        
eleccion_bombillas()
signal.pause()
              
