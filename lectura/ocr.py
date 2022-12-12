from distutils.config import PyPIRCCommand
import pytesseract as tess
from PIL import Image
import cv2

from collections import Counter




#my_image = cv2.imread("1111.jpg")

#my_image = Image.open('1111.jpg')

#print(txt)
listado = []

# Funcion para interpretar Imagen y pasarlo a xml
def getImagenTexto(imagen):
    #my_image = Image.open(imagen).convert('L')
    gray = cv2.imread(imagen)
    #gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (2,1))
    custom_oem_psm_config = r'--oem 3 --psm 3'
    xml = tess.image_to_alto_xml(gray, config=custom_oem_psm_config, lang = "spa")
    texto = getXmlATexto(xml)
    #txto = tess.image_to_string(gray, config=custom_oem_psm_config, lang = "spa")
    #print(txto)
    return texto

# Funcion para obtener todo el archivo xml en txt
def getXmlATexto(xml):
    #txt = open("eje5.txt", "w")
    #txt.write(str(xml))
    #txt.close()
    y = str(xml)
    return y
  
# Función para obtener por párrafos
def getParrafos(texto):
    parrafos = []
    parrafos = texto.split(sep= "<TextBlock")
    parrafos.pop(0)
    return parrafos
    
#  Funcion para capturar las palabras 
def getPalabras(parrafo):
    palabras = []
    for texto in parrafo:
        #p = []
        x = texto.split(sep = 'CONTENT="')
        
        for i in range(1, len(x)):
            #print(x[i])
            y = x[i].split(sep = '"', maxsplit=1)
            #p.append(y[0])
            palabras.append(y[0])
    return palabras

# Funcion para obetener el valor del espaciado entre palabras
def getValorEspacio(texto):
    list_espaciado =[]
    
    x = texto.split(sep = 'CONTENT="')
    for i in range(1, len(x)):
        #espaciado = []
        if x[i].find('SP WIDTH="') != -1:
            p = x[i].split(sep = 'SP WIDTH="', maxsplit=1)
            l = p[1].split(sep = '"', maxsplit=1)
            #espaciado.append(l[0])
            if l[0] == "0":
                l[0] = 1
            espaciado = abs(int(l[0]))
        else:
            espaciado = 100
            #espaciado.append('enter')
        
        list_espaciado.append(espaciado)
    return list_espaciado

# Funcion para comprobar valores marcados
def getValores(ListadoM, listaP, listaE):
    uno = 1
    dos = 2
    Marcas = {}
    for listaM in ListadoM:
        for x in listaM:
            for i in range(len(listaP)):
                if x == listaP[i]:
                    valor = listaE[i]-1
                    #valorI = listaE[i] - uno
                    #valorS = listaE[i] + uno
                    if valor < 99 and listaE[i+uno] != 100:
                        if valor <= listaE[i+uno]:
                            print(i)
                            print("no es marca")
                        elif valor <= listaE[i+dos] and listaE[i+dos] != 100:
                            print(i)
                            print("no es marca")
                        elif valor >= listaE[i+dos] and listaE[i+dos] != 100 and valor >= listaE[i+uno]:
                            print(i)
                            print("marca")
                            Marcas[i] = listaP[i]
                        elif valor <= listaE[i+dos] and listaE[i+dos] != 100 and valor <= listaE[i+uno]:
                            print(i)
                            print("no es marca")
                        else:
                            if valor <= listaE[i-uno] and listaE[i-uno] != 100:
                                print(i)
                                print("no es marca")
                            else:
                                print(i)
                                print("marca")
                                Marcas[i] = listaP[i]
                    elif valor == 99:
                        print(i)
                        print("es Final de linea")
                    else:
                        if valor <= listaE[i+dos] and listaE[i+dos] != 100:
                            print(i)
                            print("no es marca")
                        else:
                            print(i)
                            print("marca")
                            Marcas[i] = listaP[i]

    return Marcas
""" print(Marcas)
    print(len(Marcas))
    if len(listaP) <= 300:
        if len(Marcas) >= 9:
            print("Estefany es la zarapastrosa")
        else:
            print("Desconocido")
    elif len(listaP) >= 300:
        if len(Marcas) >= 15:
            print("Estefany es la zarapastrosa")
        else:
            print("Desconocido")
"""
 
def verificar_Marca():
    pass


listadoT = [['prueba', 'fecha', 'sarapastrosa'],['Quijote', 'cumbre', 'primera'] ,['graciosos,', 'reseña', 'argumento,'] , [], ['armas', 'buscar', 'deshaciendo'], ['andanzas', 'caminos', 'blancos'], [], ['respectivamente.', 'caballerescas.', 'segunda'], ['persona,', 'percibe', 'quiero'], ['quienes', 'algunos', 'romances'], ['Charcas,', 'estructurada', 'organizada'], ['1560.', 'Francisco', '860.000'], ['Audiencia', 'Charcas', 'incorporada'], ['XVIII,', 'similar.', 'masas'], ['Fueron', 'expulsados,', 'tanto'], ['virreinales', 'lograron', 'principales'], ['constituyente', 'proyecto', 'presidente'], ['siguiendo', 'hispana,', 'todos'], ['descontento,', 'Pedro', 'depuesto'], ['Posteriormente', 'aunque', 'fuera'], [], ['escasamente', 'poblado', '990.000'], ['profundas', 'desde', 'enriquecida'], ['inexistencia', 'pronunciamiento', 'forma'], ['mayor', 'mantener', 'guerra'], ['populares,', 'objetivos', 'pueblo'], ['atenuar', 'progresivamente', 'reservando'], ['partidos', 'partidos,', 'leves'], ['fines', 'fueron', 'nacionalistas'], [], ['Obrero', 'gracias', 'clase'], ['quien', 'asimismo', 'diversos'], [], [], ['elecciones', 'izquierda', 'austeridad'], ['elecciones', 'Zamora', 'presidente'], ['impuso', 'salud,', 'vicepresidente'], ['presidencia', 'Posteriormente', 'Gisbert'], ['Corte', 'Suprema', 'Justicia'], [], ['votos', 'Morales', 'Ostenta'], [], ['fundaron', 'Bolivia', 'enfermedades'], ['Imperio', 'dominio', 'capturar'], [], ['embargo,', 'cuando', 'dominio'], [], ['historia', 'Bolivia', 'resumida,'], [], [], [], ['civilizado', 'durante', 'Tiahuanaco'], [], ['Bolivia', 'imparable.', 'españoles'], ['regiones', 'independizaron', 'España.'], ['enfrentaba', 'muchas', 'minas']]

print(len(listadoT))

def lectura_img():
    l = getImagenTexto("prueba1.jpeg")
    f = getParrafos(l)
    p = getPalabras(f)
    e = getValorEspacio(l)
    getValores(listadoT, p, e)
    pass

l = getImagenTexto("/app/static/uploads/imgs/prueba1.jpeg")

f = getParrafos(l)
p = getPalabras(f)
#print(p)
e = getValorEspacio(l)

getValores(listadoT, p, e)
#print(p)
#print(len(e))
## Buscador de Palabras solo para pruebas
""" hola = True
while(hola != "end"):
    indice = 0
    hola = input('ingrese Valor a buscar: ')
    for x in p:
        if x == hola:
            print("############")
            print(x)
            
            print(e[indice-2])
            print(e[indice-1])
            print("&&&&&&&&")
            print(e[indice])
            print("&&&&&&&&")
            print(e[indice+1])
            print(e[indice+2])
            print(e[indice+3])
            print(indice)
            indice += 1
            print("*********")
        else:
            indice += 1 """
        
#print(p[304])
#print(e)
            
# Funcion para crear un diccionario con la palabra y valor de espacios
""" valores = {palabra:int(espacio) for (palabra,espacio) in zip(p,e)}
#print (valores)
t = [abs(int(i)) for i in e]
#print(t)
conteo = Counter(t)
resultado = {}
for i in conteo:
    valor = conteo[i]
    if valor != 1:
        resultado[i] = abs(valor) """
# Funcion para ordenar orden por cantidad de espacios
#valores2 = dict(valores)
""" s = dict(sorted(resultado.items(), key=lambda x: x[1], reverse=True))
#print(valores.items())
valores2 = dict(valores)
for valor, esp in valores2.items():
    if esp <= 5 :
        del valores[valor]
#print(valores) """

#print(s)

#print(p)
#print(len(e))

""" #print(listado)
print(espaciado)
print(len(espaciado))
print(len(listado))
cont = 0
#for i in range(len(espaciado)):
for i in espaciado:
    if i == "enter":
        cont += 1
print( cont)
#print(x[5]) """








