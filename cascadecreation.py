# -*- coding: utf-8 -*-
"""
    Javier J. Medinilla A.
    https://github.com/JMedinilla/
"""

# cv2       ->  Tratamiento de imágenes
# os        ->  Manejar ficheros
# shutil    ->  Eliminar carpetas
# re        ->  Expresiones regulares
import cv2, os, shutil, re

"""
    Esta función elimina los ficheros y carpetas que existieran previamente,
    debido a que van a volver a ser creados durante la ejecución de este
    programa
"""
def clearDir():
    try:
        os.remove("wheel.info")
        print("Archivo INFO anterior eliminado")
    except:
        print("No hay INFO que borrar")
    try:
        os.remove("wheel.vec")
        print("Archivo VEC anterior eliminado")
    except:
        print("No hay VEC que borrar")
    try:
        os.remove("bg.txt")
        print("Archivo TXT anterior eliminado")
    except:
        print("No hay TXT que borrar")
    try:
        shutil.rmtree('data')
        print("Carpeta DATA anterior eliminada")
    except:
        print("No hay DATA que borrar")


"""
    Cambia el nombre a todos los ficheros de la carpeta de positivos, por unos
    más adecuados, por simple motivo de orden
"""
def readPositivesAndChangeName():
    numForLoop = 1
    lst = os.listdir("pos")
    orderlst = sorted(lst, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in orderlst:
        os.rename("pos/"+str(filename), "pos/pos_"+str(numForLoop)+".png")
        numForLoop += 1

    print("Positivos, nombres cambiados")

"""
    Lee todas las imágenes de la carpeta de positivos y modifica, con el
    objetivo de reescribirlas en una escala de grises y a un tamaño uniforme
    Si el objeto a detectar cumple otras dimensiones, cambiar tamaño en
    consecuencia para mantener la proporción del objeto
"""
def readPositivesAndChangeSize():
	wi = 50
	he = 50
    lst_pos = os.listdir("pos")

    for filename in lst_pos:
        img = cv2.imread("pos/"+str(filename),cv2.IMREAD_GRAYSCALE)
        resized = cv2.resize(img, (wi, he))
        cv2.imwrite("pos/"+str(filename), resized)
        
    print("Positivos, tamaño modificado")

"""
    Lee todos los ficheros de la carpeta de imágenes positivas y escribe sus
    rutas en un fichero con la extensión .info, necesario posteriormente para
    crear el vector de imágenes
"""
def writeInfoFile():
    lst = os.listdir("pos")
    orderlst = sorted(lst, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in orderlst:
        path = "pos/"+filename
        file = cv2.imread(path)
        height, width, channels = file.shape
        line = path + " 1 0 0 "+str(height)+" "+str(width)+"\n"
        with open("wheel.info", "a") as info:
            info.write(line)

    print("Positivos, Archivo INFO creado")

"""
    Cambia el nombre a todos los ficheros de la carpeta de negativos, por unos
    más adecuados, por simple motivo de orden
"""
def readNegativesAndChangeName():
    numForLoop = 1
    lst = os.listdir("neg")
    orderlst = sorted(lst, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in orderlst:
        os.rename("neg/"+str(filename), "neg/neg_"+str(numForLoop)+".png")
        numForLoop += 1

    print("Negativos, nombres cambiados")

"""
    Lee todas las imágenes de la carpeta de negativos y las modifica, con el
    objetivo de reescribirlas en una escala de grises y a un tamaño uniforme
    Hay que asegurarse de que todas las imágenes negativas van a tener un tamaño
    mayor que el objeto a detectar presente en las imágenes positivas
"""
def readNegativesAndChangeSize():
	wi = 100
	he = 100

    lst = os.listdir("neg")
    orderlst = sorted(lst, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in orderlst:
        img = cv2.imread("neg/"+str(filename),cv2.IMREAD_GRAYSCALE)
        resized = cv2.resize(img, (wi, he))
        cv2.imwrite("neg/"+str(filename), resized)

    print("Negativos, tamaño modificado")

"""
    Lee todos los ficheros de la carpeta de imágenes negativas y escribe sus
    rutas en un fichero con la extensión .txt, necesario posteriormente para
    crear el entrenamiento del haar cascade
"""
def writeBgFile():
    lst = os.listdir("neg")
    orderlst = sorted(lst, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in orderlst:
        path = "neg/"+filename+"\n"
        with open("bg.txt", "a") as bg:
            bg.write(path)

    print("Negativos, Archivo TXT creado")

"""
    Este método obtiene, en primer lugar, la cantidad de imágenes positivas que
    hay en el directorio, y procede a leer la primera de todas para leer sus
    dimensiones
    Estas 3 cosas son necesarias para el comando que se va a ejecutar de opencv
    en consola, el cual, con la lista de imágenes positivas, su alto y su ancho,
    creará un fichero con la extensión .vec, que contiene todas las instancias
    del objeto a detectar proporcionadas por el usuario para el posterior
    entrenamiento del haar cascade
"""
def consoleCreatePositiveVec():
    num = len(os.listdir("pos"))
    firstItem = "pos/"+os.listdir("pos")[0]
    file = cv2.imread(firstItem)
    height, width, channels = file.shape
    os.popen("opencv_createsamples -info wheel.info -num "+str(num)+" -w "+str(width)+" -h "+str(height)+" -vec wheel.vec")

    print("Positivos, Archivo VEC creado")

"""
    Igual que el método anterior, este obtiene la cantidad de positivos, aunque
    también de negativos, y reduce la cifra obtenida a un 90 de su valor, ya que
    no todas las imágenes deberían ser usadas en el entrenamiento
    También se establece un número de fases para el entrenamiento, el cual
    influirá en gran medida en el tiempo que durará el mismo, aunque también la
    eficacia de la detección
    Cuando todos los valores han sido obtenidos, se construye el comando que el
    usuario tendrá que ejecutar a continuación, copiándolo y pegándolo para
    ejecutarlo a mano, como un comando separado, ya que este podría durar de 20
    minutos a incluso más de 1 semana de ejecución ininterrumpida
"""
def consoleCreateCascade():
	percent = 90
    stages = 20

    firstItem = "pos/"+os.listdir("pos")[0]
    file = cv2.imread(firstItem)
    height, width, channels = file.shape

    numPos = round((len(os.listdir("pos"))*percent)/100)
    numNeg = round((len(os.listdir("neg"))*percent)/100)

    os.popen("mkdir data")
    print("Carpeta DATA creada")
    print("\nEjecutar a continuación,")
    print("opencv_traincascade -data data -vec wheel.vec -bg bg.txt -numPos "+str(numPos)+" -numNeg "+str(numNeg)+" -numStages "+str(stages)+" -w "+str(width)+" -h "+str(height)+" -featureType LBP")
    os.popen(("opencv_traincascade -data data -vec wheel.vec -bg bg.txt -numPos "+str(numPos)+" -numNeg "+str(numNeg)+" -numStages "+str(stages)+" -w "+str(width)+" -h "+str(height)+" -featureType LBP"))

clearDir()
readPositivesAndChangeName()
readPositivesAndChangeSize()
writeInfoFile()
readNegativesAndChangeName()
readNegativesAndChangeSize()
writeBgFile()
consoleCreatePositiveVec()
consoleCreateCascade()