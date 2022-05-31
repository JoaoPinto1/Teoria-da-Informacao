import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
from scipy.io import wavfile

def descobrirAlfabeto(P):
    tipo=str(P.dtype)
    n=int(tipo[-1:])
    alfabeto=range(0,2**n)

    return alfabeto

#conta o nº de ocorrências dos elementos de A em P

def conta_ocorrencias(P,A):
    #array com o nº de ocorrencias
    no=np.zeros((len(A),len(A)))
    for i in range(len(P)):
        no[A[P[i]]]+=1

    return no


def histograma(numOco,A): #apresenta o histograma
    plt.figure()
    plt.bar(A,numOco)

#Ex2
def entropia(numOco): #calcula a entropia
    np.asarray(numOco)
    entropia=0
    p = numOco / np.sum(numOco)
    p=p[p>0]
    entropia = -np.sum(p*np.log2(p))

    return entropia

#Ex3
def lerTexto(ficheiro): #lê um ficheiro de texto e retorna todos os carateres alfabéticos e a entropia do conjunto
    f = open(ficheiro,"r")
    texto = f.read()
    lista=[]
    for char in texto:
        char = char.lower()
        if char.isalpha():
            lista.append(char)
    P = np.asarray(lista)
    no = np.zeros(26)
    #contar ocorrencias das letras
    for i in range(len(P)):
        no[ord(P[i])-97]+=1
    A = range(97,123)
    lista=[]
    for a in A:
        a=chr(a)
        lista.append(a)
    histograma(no,lista)
    return P,entropia(no)

def lerImagem(imagem): #lê uma imagem e returna os dados, alfabeto, e entropia
    P= mpimg.imread(imagem)
    P=P.flatten()
    A=descobrirAlfabeto(P)
    values , counts = np.unique(P,return_counts=True)
    histograma(counts,A)
    return P,A,entropia(counts)
    
def lerAudio(ficheiro): #lê um audio e retorna os dados,alfabeto e entropia
    [fs,P]=wavfile.read(ficheiro)
    P=P.flatten()
    A=descobrirAlfabeto(P)
    values , counts = np.unique(P,return_counts=True)
    histograma(counts,values)
    return P,A,entropia(counts)

def main():
    #P,entropia=lerTexto("english.txt")
    #P,alfabeto,entropia=lerImagem("kid.bmp")
    P,alfabeto,entropia=lerAudio("guitarsolo.wav")
    print(entropia)
    
    #kid 6.95
    #homer 3.46
    #homerbin 0.64
    #guitarsolo 7.32
    #english 4.22

if __name__ =="__main__":
    main()
    