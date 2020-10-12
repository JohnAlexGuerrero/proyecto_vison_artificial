import cv2
import os, shutil, re

def readPositiveAndChangeName():
    numForLoop = 1
    lst = os.listdir("pos")

    #print(lst)
    orderlst = sorted(lst, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in orderlst:
        os.rename("pos/"+str(filename),"pos/pos_"+str(numForLoop)+".png")
        numForLoop += 1
    print("Positivos, nombres cambiados")

def readPositiveAndChangeSize():
    wi = 50
    he = 50
    lst_pos = os.listdir('pos/')

    for filename in lst_pos:
        img = cv2.imread("pos/"+str(filename),cv2.IMREAD_GRAYSCALE)
        resized = cv2.resize(img, (wi, he))
        cv2.imwrite("pos/"+str(filename), resized)
    print("Positivos, tamaño modificado")

def writeInfoFile():
    lst = os.listdir("pos")
    orderlst = sorted(lst, key=lambda x:(int(re.sub('\D','',x)),x))
    for filename in orderlst:
        path = "pos/"+filename
        file = cv2.imread(path)
        height, width, channels = file.shape
        line = path + " 1 0 0 "+str(height)+" "+str(width)+"\n"
        with open("wheel.info","a") as info:
            info.write(line)
    print("Positivos, Archivo INFO creado")

def readNegativesAndChangeName():
    numForLoop = 1
    lst = os.listdir("neg")
    orderlst = sorted(lst, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in orderlst:
        os.rename("neg/"+str(filename), "neg/neg_"+str(numForLoop)+".png")
        numForLoop += 1

    print("Negativos, nombres cambiados")

def readNegativesAndChangeSize():
    wi = 100
    he = 100
    lst = os.listdir("neg")
    orderlst = sorted(lst, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in orderlst:
        img = cv2.imread("neg/"+str(filename),cv2.IMREAD_GRAYSCALE)
        resized = cv2.resize(img, (wi, he))
        cv2.imwrite("neg/"+str(filename),resized)
    print("Negativos, tamaño modificado")

def writeBgFile():
    lst = os.listdir("neg")
    orderlst = sorted(lst, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in orderlst:
        path = "neg/"+filename+"\n"
        with open("bg.txt","a") as bg:
            bg.write(path)
    print("Negativos, archivo TXT Creado")

def consoleCreatePositiveVec():
    num = len(os.listdir("pos"))
    firstItem = "pos/"+os.listdir("pos")[0]
    file = cv2.imread(firstItem)
    height, width, channels = file.shape
    os.popen("opencv_createsamples -info wheel.info -num "+str(num)+" -w "+str(width)+" -h "+str(height)+" -vec wheel.vec")
    print("Positivos, Archivo VEC creado")

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
    print("\n Ejecutar a continuacion")
    print("opencv_traincascade -data data -vec wheel.vec -bg bg.txt -numPos "+str(numPos)+" -numNeg "+str(numNeg)+" -numStages "+str(stages)+" -w "+str(width)+" -h "+str(height)+" -featureType LBP")

#readPositiveAndChangeName()

#readPositiveAndChangeSize()

#writeInfoFile()

#readNegativesAndChangeName()

#readNegativesAndChangeSize()

#writeBgFile()

consoleCreatePositiveVec()

consoleCreateCascade()