import time
import os
import sys
import signal
import ConfigParser
import rainbowhat
import rainbowhat as rh
from tradfri import tradfriActions
from tqdm import tqdm

#Se obtiene del nanotexto 'tradfri.cfg' los valores de la direccion IP de la pasarela, apiuser y la apikey.

conf = ConfigParser.ConfigParser()
script_dir = os.path.dirname(os.path.realpath(__file__))
conf.read(script_dir + '/tradfri.cfg')
hubip = conf.get('tradfri','hubip')
apiuser = conf.get('tradfri','apiuser')
apikey = conf.get('tradfri','apikey')

#Variables

pulsacion=0
bombillas = [65537,65538,131073]
bulbid=0
color=["warm","normal","cold"]
intensidad_bombilla=50
contador=0
contador_color=0
estado=0
menu_decimal=0
minimo=0
maximo=0
intensidad_bombilla_1=0
intensidad_bombilla_2=0

#Metodo para mostrar por display un mensaje con desplazamiento
def scroll_mensaje(mensaje):
        
        for w in mensaje:

                mensaje = mensaje[1:len(mensaje)] + mensaje[0]
                rainbowhat.display.print_str(mensaje)
                rainbowhat.display.show()
                time.sleep(0.2)                                                       

#Metodo para mostrar por display un mensaje sin desplazamiento. Si al llamar al metodo la segunda variable que se le pasa por parametro es distinta de 0, se mostrara en el display un punto decimal.                      
def display_mensaje(mensaje,menu_decimal):

        if menu_decimal==0: 
                                
                rainbowhat.display.print_str(mensaje)
                rainbowhat.display.show() 
                time.sleep(0.2)
                
        else:
                rainbowhat.display.print_str(mensaje)
                rainbowhat.display.set_decimal(0,True)
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

#Metodo para encender una o varias bombillas dependiendo el identificador que se le pase por el cuarto parametro del metodo.                        
def switch_on(hubip, apiuser, apikey, bulbid):

        if bulbid!=131073:
                      
                tradfriActions.tradfri_power_light(hubip, apiuser, apikey, bulbid, 'on')

	elif bulbid==131073:
                tradfriActions.tradfri_power_group(hubip,apiuser,apikey, bulbid ,'on')
                
#Metodo para apagar una o varias bombillas dependiendo el identificador que se le pase por el cuarto parametro del metodo. 
def switch_off(hubip, apiuser, apikey, bulbid):
        
        if bulbid!=131073:
                tradfriActions.tradfri_power_light(hubip, apiuser, apikey, bulbid, 'off')
                
        elif bulbid==131073:
                tradfriActions.tradfri_power_group(hubip, apiuser, apikey, bulbid, "off")
	
#Metodo para cambiar la intensidad de la bombilla/s seleccionadas.
def intensity(hubip, apiuser, apikey, bulbid, value):
        
        if bulbid!=131073:
                
                tradfriActions.tradfri_dim_light(hubip, apiuser, apikey, bulbid, value)
                
        else:
                tradfriActions.tradfri_dim_group(hubip, apiuser, apikey, bulbid, value)
        
#Metodo que sirve para cambiar el color de la bombilla/s en 3 tipos de estado: warm, norm, cold.
def colour(hubip, apiuser, apikey ,bulbid, value):

        if bulbid!=131073:

                if value=="warm":
                        tradfriActions.tradfri_color_light(hubip, apiuser, apikey, bulbid, "warm")
                        
                elif value=="normal":
                        tradfriActions.tradfri_color_light(hubip, apiuser, apikey, bulbid, "normal")
                        
                elif value=="cold":
                        tradfriActions.tradfri_color_light(hubip, apiuser, apikey, bulbid, "cold")
        else:

                for x in range(2):
                        
                        bulbid=bombillas[x]
                        
                        if value=="warm":
                                tradfriActions.tradfri_color_light(hubip, apiuser, apikey, bulbid, "warm")
                                
                        elif value=="normal":
                                tradfriActions.tradfri_color_light(hubip, apiuser, apikey, bulbid, "normal")
                                
                        elif value=="cold":
                                tradfriActions.tradfri_color_light(hubip, apiuser, apikey, bulbid, "cold")
                
#Metodo que se le pasa el parametro "estado" para encender los 7 leds del Rainbow HAT de manera creciente o decreciente dependiendo de si se pulsa el boton de encender o apagar la luz respectivamente.
def leds_luces(estado):
        
        if estado==1:
                
                array_on=[0,1,2,3,4,5,6]
               
                rh.rainbow.clear()
                
                for x in array_on:
                        
                        rh.rainbow.set_pixel(x,3,46,250)
                        rh.rainbow.show()
                        time.sleep(0.1)
                
        if estado==0:

                array_off=[6,5,4,3,2,1,0]
                
                rh.rainbow.set_all(3,46,250)
                
                for x in array_off:
                        
                        rh.rainbow.set_pixel(x,0,0,0)
                        rh.rainbow.show()
                        time.sleep(0.1)

#Metodo que sirve de animacion en el saludo inicial al encenderse el mando remoto mediante un juego de colores con los leds del Rainbow HAT.
def leds_inicio():
                        
                for x in range(7):
                                                                            
                                rh.rainbow.clear()
                                
                                if x==0:

                                        rh.rainbow.set_pixel(x,52,243,239)
                                        rh.rainbow.set_pixel(x+6,52,243,239)
                                        rh.rainbow.show()
                                        time.sleep(0.3)

                                elif x==1:

                                        rh.rainbow.set_pixel(x,31,214,4)
                                        rh.rainbow.set_pixel(x+4,31,214,4)
                                        rh.rainbow.show()
                                        time.sleep(0.3)
                                        
                                elif x==2:
                                        
                                        rh.rainbow.set_pixel(x,249,5,182)
                                        rh.rainbow.set_pixel(x+2,249,5,182)
                                        rh.rainbow.show()
                                        time.sleep(0.3)
                                        
                                elif x==3:
                                        
                                        rh.rainbow.set_pixel(x,249,112,5)
                                        rh.rainbow.show()
                                        time.sleep(0.3)
                                        
                                elif x==4:
                                        
                                        rh.rainbow.set_pixel(x,31,214,4)
                                        rh.rainbow.set_pixel(x-2,31,214,4)
                                        rh.rainbow.show()
                                        time.sleep(0.3)
                                        
                                elif x==5:
                                        
                                        rh.rainbow.set_pixel(x,249,5,182)
                                        rh.rainbow.set_pixel(x-4,249,5,182)
                                        rh.rainbow.show()
                                        time.sleep(0.3)
                                        
                                elif x==6:
                                        
                                        rh.rainbow.set_pixel(x,249,112,5)
                                        rh.rainbow.set_pixel(x-6,249,112,5)
                                        rh.rainbow.show()
                                        time.sleep(0.3)

#Metodo que pinta cada led de un color y parpadea 3 veces indicando que se ha acabado la configuracion que se haya seleccionado.
def leds_final():
              
                for x in range(3):
                        
                                rh.rainbow.clear()
                                rh.rainbow.show()
                                time.sleep(0.2)
                                rh.rainbow.set_pixel(6,1,1,35)
                                rh.rainbow.set_pixel(5,7,35,1)
                                rh.rainbow.set_pixel(4,35,1,12)
                                rh.rainbow.set_pixel(3,222,45,6)
                                rh.rainbow.set_pixel(0,1,1,35)
                                rh.rainbow.set_pixel(1,7,35,1)
                                rh.rainbow.set_pixel(2,35,1,12)
                                rh.rainbow.show()
                                time.sleep(0.2)
                                                                
#Metodo donde dependiendo el nivel de intensidad que tenga la bombilla/s entonces se pintara el display como un limitador.                       
def limitador():
        
                        if intensidad_bombilla==0:
        
                                rh.rainbow.set_pixel(6,0,0,0)
                                rh.rainbow.set_pixel(5,0,0,0)
                                rh.rainbow.set_pixel(4,0,0,0)
                                rh.rainbow.set_pixel(3,0,0,0)
                                rh.rainbow.set_pixel(2,0,0,0)
                                rh.rainbow.set_pixel(1,0,0,0)
                                rh.rainbow.set_pixel(0,0,0,0)
                                rh.rainbow.show()
                                
                        if intensidad_bombilla==10:
        
                                rh.rainbow.set_pixel(6,41,210,216)
                                rh.rainbow.set_pixel(5,0,0,0)
                                rh.rainbow.set_pixel(4,0,0,0)
                                rh.rainbow.set_pixel(3,0,0,0)
                                rh.rainbow.set_pixel(2,0,0,0)
                                rh.rainbow.set_pixel(1,0,0,0)
                                rh.rainbow.set_pixel(0,0,0,0)
                                rh.rainbow.show()
                                
                        elif intensidad_bombilla==30:
                                
                                rh.rainbow.set_pixel(6,41,210,216)
                                rh.rainbow.set_pixel(5,41,216,128)
                                rh.rainbow.set_pixel(4,0,0,0)
                                rh.rainbow.set_pixel(3,0,0,0)
                                rh.rainbow.set_pixel(2,0,0,0)
                                rh.rainbow.set_pixel(1,0,0,0)
                                rh.rainbow.set_pixel(0,0,0,0)
                                rh.rainbow.show()
                                
                        elif intensidad_bombilla==40:
                                
                                rh.rainbow.set_pixel(6,41,210,216)
                                rh.rainbow.set_pixel(5,41,216,128)
                                rh.rainbow.set_pixel(4,53,216,41)
                                rh.rainbow.set_pixel(3,0,0,0)
                                rh.rainbow.set_pixel(2,0,0,0)
                                rh.rainbow.set_pixel(1,0,0,0)
                                rh.rainbow.set_pixel(0,0,0,0)
                                rh.rainbow.show()
                                
                        elif intensidad_bombilla==50:
                                
                                rh.rainbow.set_pixel(6,41,210,216)
                                rh.rainbow.set_pixel(5,41,216,128)
                                rh.rainbow.set_pixel(4,53,216,41)
                                rh.rainbow.set_pixel(3,238,249,6)
                                rh.rainbow.set_pixel(2,0,0,0)
                                rh.rainbow.set_pixel(1,0,0,0)
                                rh.rainbow.set_pixel(0,0,0,0)
                                rh.rainbow.show()
                                
                        elif intensidad_bombilla==70:
                                
                                rh.rainbow.set_pixel(6,41,210,216)
                                rh.rainbow.set_pixel(5,41,216,128)
                                rh.rainbow.set_pixel(4,53,216,41)
                                rh.rainbow.set_pixel(3,238,246,6)
                                rh.rainbow.set_pixel(2,249,131,6)
                                rh.rainbow.set_pixel(1,0,0,0)
                                rh.rainbow.set_pixel(0,0,0,0)
                                rh.rainbow.show()
                                
                        elif intensidad_bombilla==80:
                                
                                rh.rainbow.set_pixel(6,41,210,216)
                                rh.rainbow.set_pixel(5,41,216,128)
                                rh.rainbow.set_pixel(4,53,216,41)
                                rh.rainbow.set_pixel(3,238,246,6)
                                rh.rainbow.set_pixel(2,249,131,6)
                                rh.rainbow.set_pixel(1,249,21,6)
                                rh.rainbow.set_pixel(0,0,0,0)
                                rh.rainbow.show()
                                
                        elif intensidad_bombilla==100:
                                
                                rh.rainbow.set_pixel(6,41,210,216)
                                rh.rainbow.set_pixel(5,41,216,128)
                                rh.rainbow.set_pixel(4,53,216,41)
                                rh.rainbow.set_pixel(3,238,246,6)
                                rh.rainbow.set_pixel(2,249,131,6)
                                rh.rainbow.set_pixel(1,249,21,6)
                                rh.rainbow.set_pixel(0,255,0,0)
                                rh.rainbow.show()
                              
#Metodo con el que se inicia el mando remoto mostrando un mensaje inicial y seleccionando la bombilla/s que se desea configurar.
def inicio(pulsacion):
                        
        mensaje ="PULSE A PARA CONFIGURAR BOMBILLA 1*B CONFIGURA BOMBILLA 2*C CONFIGURA AMBAS    "
        
        rh.rainbow.set_pixel(6,1,1,35)
        rh.rainbow.set_pixel(5,7,35,1)
        rh.rainbow.set_pixel(4,35,1,12)
        rh.rainbow.set_pixel(3,222,45,6)
        rh.rainbow.set_pixel(0,1,1,35)
        rh.rainbow.set_pixel(1,7,35,1)
        rh.rainbow.set_pixel(2,35,1,12)
        rh.rainbow.show()
        time.sleep(0.1)
        
        if pulsacion==0: #Si no se ha pulsado todavia ningun boton para seleccionar una bombilla/s entonces le aparece el siguiente mensaje en el display.
                
                scroll_mensaje(mensaje)       
                mensaje ="ABoC"
                display_mensaje(mensaje,0)
                
        #Si ya se ha pulsado anteriormente entonces ya no te aparece el texto inicial, sino un texto mas abreviado.
        else:
                
                mensaje="ELIGE BOMBILLA    "
                scroll_mensaje(mensaje)
                mensaje ="ABoC"
                display_mensaje(mensaje,0)
                
        #Escuchador para saber que boton se ha pulsado, si es el boton A, entonces configuramos la bombilla con el id=65537, si es el boton B configuramos la bombilla con el id=65538, y por ultimo,
        #si se ha pulsado el boton C se seleccionaran el conjunto de bombillas cuyo id sera el del grupo que en nuestro caso es 131073.
        @rainbowhat.touch.press()
        def touch(channel):

                                luz_boton_on(channel)
                                luz_boton_off()
                                                  
                                global pulsacion
                                pulsacion=1                

                                if channel==0:
                                        
                                        bulbid=bombillas[0]
                                        display_mensaje("MENU",0)
                                        menu_luces(bulbid)

                                elif channel==1:
                                        
                                        bulbid=bombillas[1]
                                        display_mensaje("MENU",0)
                                        menu_luces(bulbid)
                                        
                                else:
                                        
                                        bulbid=bombillas[2]
                                        display_mensaje("MENU",0)
                                        menu_luces(bulbid)
                        
#Metodo que realiza las funciones del menu del mando remoto controlando en primer lugar el encendido o apagado de las bombillas, en segundo lugar, la intensidad y por ultimo, el color.
def menu_luces(bulbid):

        #En el menu, pulsando el boton A nos dirige a la primera opcion del menu, la LUZ. 
        @rainbowhat.touch.A.press()
        def press_a(channel):
                
                rh.rainbow.clear()
                rh.rainbow.show()
                luz_boton_on(channel)
                luz_boton_off()
                
                display_mensaje("1LUZ",1)

                #Pulsando la B dentro de esta primera opcion, se encendera la bombilla/s                
                @rainbowhat.touch.B.press()
                def press_b(channel):
                      
                    global estado
                    
                    luz_boton_on(channel)
                    luz_boton_off()

                    switch_on(hubip, apiuser, apikey, bulbid)
                    display_mensaje("ON  ",0)
                    estado=1
                    leds_luces(estado)

                #Pulsando el boton C se apagara la bombilla/s
                @rainbowhat.touch.C.press()
                def press_c(channel):
                        
                    global estado
                    luz_boton_on(channel)
                    luz_boton_off()
                    
                    switch_off(hubip, apiuser, apikey, bulbid)      
                    display_mensaje("OFF ",0)
                    estado=0
                    leds_luces(estado)
                        
                #Pulsando la A nuevamente, aparecera la segunda opcion del menu, la INTENSIDAD.
                @rainbowhat.touch.A.press()
                def touch_a(channel):

                    luz_boton_on(channel)
                    luz_boton_off()
                    display_mensaje("2INT",1)
                    rh.rainbow.clear()
                    rh.rainbow.show()
                   
                    #Pulsando la B disminuiremos la intensidad de la bombilla/s en un intervalo de 10 por ciento por cada pulsacion. Segun se vaya decrementando la intensidad se iran apagando los leds del rainbow HAT.
                    #Si se llegase por debajo del minimo, es decir, el valor 0, entonces, aparecera un mensaje de error. 
                    @rainbowhat.touch.B.press()
                    def touch_b(channel):

                        global estado
                        global contador
                        global intensidad_bombilla
                        global minimo
                        
                        minimo=0
                        luz_boton_on(channel)
                        luz_boton_off()                                             
                        
                        estado=1

                        if contador==0:

                                intensidad_bombilla=intensidad_bombilla                              
                              
                        else:

                                intensidad_bombilla=intensidad_bombilla-10
                                
                        limitador()
                                
                        if intensidad_bombilla==100:

                                valor="{intensidad_bombilla}".format(intensidad_bombilla=intensidad_bombilla)
                                rainbowhat.display.clear()
                                rainbowhat.display.print_str(valor)
                                rainbowhat.display.show()
                                time.sleep(0.1)

                        elif 9<intensidad_bombilla<100:

                                valor="{intensidad_bombilla}".format(intensidad_bombilla=intensidad_bombilla)
                                rainbowhat.display.clear()
                                rainbowhat.display.print_str(valor)
                                rainbowhat.display.show()
                                time.sleep(0.1)
                                
                        elif -1<intensidad_bombilla<10:

                                valor="{intensidad_bombilla}".format(intensidad_bombilla=intensidad_bombilla)
                                rainbowhat.display.clear()
                                rainbowhat.display.print_str(valor)
                                rainbowhat.display.show()
                                time.sleep(0.1)
                                
                        else:
                               mensaje ="ERROR ES EL MINIMO****"
                               longitud=len(mensaje)
                               minimo=1
                               
                               scroll_mensaje(mensaje)
                                       
                        if minimo!=1:
                                                        
                                intensity(hubip, apiuser, apikey, bulbid, intensidad_bombilla)
                                estado=1
                        else :
                                
                                intensity(hubip, apiuser, apikey, bulbid, 0)
                                estado=0
                                intensidad_bombilla=0
                                valor="{intensidad_bombilla}".format(intensidad_bombilla=intensidad_bombilla)
                                rainbowhat.display.clear()
                                rainbowhat.display.print_str(valor)
                                rainbowhat.display.show()
                                
                        contador=1

                    #Pulsando la C aumentaremos la intensidad de la bombilla/s un 10 por ciento por cada pulsacion. Segun se vaya aumentando la intensidad se iran encendiendo los leds del rainbow HAT.
                    #Si se llegase por encima del maximo, es decir, el valor 100, entonces, aparecera un mensaje de error.                         
                    @rainbowhat.touch.C.press()
                    def touch_c(channel):
                            
                        luz_boton_on(channel)
                        luz_boton_off()
                        global intensidad_bombilla
                        global contador
                        global estado
                        global maximo
                        estado=1
                        maximo=0
                        
                        limitador()
                                              
                        if contador==0:

                                intensidad_bombilla=intensidad_bombilla
                        else:

                                intensidad_bombilla=intensidad_bombilla+10
                        limitador()
                        
                        if intensidad_bombilla==100:

                                valor="{intensidad_bombilla}".format(intensidad_bombilla=intensidad_bombilla)
                                rainbowhat.display.clear()
                                rainbowhat.display.print_str(valor)
                                rainbowhat.display.show()
                                time.sleep(0.1)
                                
                        elif 9<intensidad_bombilla<100:
                                
                                valor="{intensidad_bombilla}".format(intensidad_bombilla=intensidad_bombilla)
                                rainbowhat.display.clear()
                                rainbowhat.display.print_str(valor)
                                rainbowhat.display.show()
                                time.sleep(0.1)
                                
                        elif -1<intensidad_bombilla<10:

                                valor="{intensidad_bombilla}".format(intensidad_bombilla=intensidad_bombilla)
                                rainbowhat.display.clear()
                                rainbowhat.display.print_str(valor)
                                rainbowhat.display.show()
                                time.sleep(0.1)
                                
                        else:

                               mensaje ="ERROR ES EL MAXIMO****"
                               longitud=len(mensaje)

                               scroll_mensaje(mensaje)
                               maximo=1
                                       
                        if maximo!=1:
                                
                                intensity(hubip, apiuser, apikey, bulbid, intensidad_bombilla)
                                
                        else :
                                
                                intensity(hubip, apiuser, apikey, bulbid, 100)
                                intensidad_bombilla=100
                                valor="{intensidad_bombilla}".format(intensidad_bombilla=intensidad_bombilla)
                                rainbowhat.display.clear()
                                rainbowhat.display.print_str(valor)
                                rainbowhat.display.show()
                                
                        contador=1
                        
                    #Si se vuelve a pulsar el boton A, aparecera la ultima opcion del menu, el COLOR.
                    @rainbowhat.touch.A.press()
                    def touch_a(channel):
                            
                        luz_boton_on(channel)
                        luz_boton_off()
                        rh.rainbow.clear()
                        rh.rainbow.show()
                        
                        display_mensaje("3COL",1)
                        menu_luces(bulbid)

                        #Pulsando el boton B cambiara la bombilla/s de color entre tres opciones: Warm, Norm o Cold. Siempre debe de estar la luz encendida antes, sino aparecera un error.
                        @rainbowhat.touch.B.press()
                        def touch_b(channel):
                                    global color
                                    global contador_color
                                    luz_boton_on(channel)
                                    luz_boton_off()

                                    if estado==1:
                                            
                                            if contador_color==0:
                                                    
                                                    colour(hubip, apiuser, apikey, bulbid,color[0])
                                                    rh.rainbow.set_all(222,45,6)
                                                    rh.rainbow.show()
                                                    display_mensaje("WARM",0)
                                                    contador_color=1
                                                    
                                            elif contador_color==1:
                                                    
                                                    colour(hubip, apiuser, apikey, bulbid,color[1])
                                                    rh.rainbow.set_all(222,169,6)
                                                    rh.rainbow.show()
                                                    display_mensaje("NORM",0)
                                                    contador_color=2
                                                    
                                            elif contador_color==2:
                                                    
                                                    colour(hubip, apiuser, apikey, bulbid,color[2])
                                                    rh.rainbow.set_all(249,249,247)
                                                    rh.rainbow.show()
                                                    display_mensaje("COLD",0)
                                                    contador_color=0
                                                    
                                    elif estado==0:
                                            
                                         mensaje ="ERROR*PRIMERO DEBE ENCENDER LA LUZ****"
                                         luz_boton_on(channel)
                                         luz_boton_off()
                                         
                                         scroll_mensaje(mensaje)
                                         display_mensaje("3COL",1)

                                            
                        #Pulsando el boton C acabaremos con el menu de esa bombilla y el programa nos dirigira a la opcion de elegir otra bombilla para su posible configuracion.
                        @rainbowhat.touch.C.press()
                        def touch_c(channel):
                                         
                                         rh.rainbow.clear()
                                         rh.rainbow.show()
                                         mensaje ="FIN DEL MENU    "
                                         longitud=len(mensaje)
                                         luz_boton_on(channel)
                                         luz_boton_off()
                                         scroll_mensaje(mensaje)
                                                 
                                         leds_final()
                                         rainbowhat.lights.rgb(0,0,0)
                                         
                                         inicio(pulsacion)
                                

#Llamada a los metodos para empezar a configurar las bombillas mediante el mando remoto
display_mensaje("HOLA",0)
leds_inicio()  
inicio(pulsacion)                          
signal.pause()


