import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
from scipy.io import wavfile

def agrupa(P): #agrupa dois simbolos, ou seja, cada simbolo é na realidade uma sequencia de dois simbolos contiguos
    P=P.flatten()
    tamanho=len(P)
    if (tamanho % 2 ==1): #se for de tamanho impar, ignoramos o ultimo simbolo
        tamanho = len(P)-1
    nova=np.zeros((int(tamanho/2),2))
    i=0
    a=0
    if isinstance(P[0],str): #se for um texto
        while(a<int(tamanho/2)):
            nova[a][0]=ord(P[i])
            nova[a][1]=ord(P[i+1])
            i+=2
            a+=1
    else:
        while(a<int(tamanho/2)):
            nova[a][0]=P[i]
            nova[a][1]=P[i+1]
            i+=2
            a+=1
    nova=nova.tolist()
    return nova

def descobrirAlfabeto(P):
    tipo=str(P.dtype)
    n=int(tipo[-1:])
    alfabeto=range(0,2**n)

    return alfabeto

def entropia(numOco): #calcula a entropia
    np.asarray(numOco)
    entropia=0
    p = numOco / np.sum(numOco)
    p=p[p>0]
    entropia = -np.sum(p*np.log2(p))

    return entropia

def histograma(numOco,A): #apresenta o histograma
    plt.figure()
    plt.bar(A,numOco)

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
    histograma(counts,values)
    return P,A,entropia(counts)
    
def lerAudio(ficheiro): #lê um audio e retorna os dados,alfabeto e entropia
    [fs,P]=wavfile.read(ficheiro)
    P=P.flatten()
    A=descobrirAlfabeto(P)
    values , counts = np.unique(P,return_counts=True)
    histograma(counts,values)
    return P,A,entropia(counts)

def ex5(P):
    agrupado= agrupa(P)
    alfabetoagru=[]
    for a in agrupado:
        if a not in alfabetoagru:
            alfabetoagru.append(a)
    contagem=[]
    for i in alfabetoagru:
        contagem.append(agrupado.count(i))
    print(entropia(contagem)/2)

def main():
    #P,entropia=lerTexto("english.txt")
    P,alfabeto,entropia=lerImagem("homerBin.bmp")
    #P,alfabeto,entropia=lerAudio("guitarsolo.wav")
    ex5(P)
    
    #guitarsolo 5.75
    #english 3.63
    #kid 4.91
    #homer 2.41
    #homerbin 0.398
    
    
if __name__ == "__main__":
    main()