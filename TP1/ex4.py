import matplotlib.pyplot as plt
from huffmancodec import * 
import numpy as np
import matplotlib.image as mpimg
from scipy.io import wavfile

def descobrirAlfabeto(P):
    tipo=str(P.dtype)
    n=int(tipo[-1:])
    alfabeto=range(0,2**n)

    return alfabeto

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
def huffman(P):
    codec = HuffmanCodec.from_data(P)
    s, l = codec.get_code_len()
    values , counts = np.unique(P,return_counts=True)
    print("Media Ponderada:")
    media=np.average(l,weights=counts)
    print(media)
    print("Variancia:")
    variancia= np.average((l-media)**2,weights=counts)
    print(variancia)

def main():
    #P,entropia=lerTexto("english.txt")
    #P,alfabeto,entropia=lerImagem("kid.bmp")
    P,alfabeto,entropia=lerAudio("guitarsolo.wav")
    huffman(P)
    
if __name__ =="__main__":
    main()