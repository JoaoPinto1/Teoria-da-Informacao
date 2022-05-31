import numpy as np
from scipy.io import wavfile

def descobrirAlfabeto(P):
    tipo=str(P.dtype)
    n=int(tipo[-1:])
    alfabeto=range(0,2**n)

    return alfabeto

def auxInfMut(q): #funcao auxiliar para calcular a entropia de um conjunto para a informacao mutua
    dic={}
    q=q.flatten()
    q=q.tolist()
    for i in q:
        dic[i]=q.count(i)
    lista=list(dic.values())
    dic=np.array(lista)
    return entropia(dic)
    
def informacaoMutua(query,target,alfabeto,passo):#calcula a informacao mutua de varias amostras e coloca tudo numa lista
    tamanho = len(query)
    nJanelas=int((len(target)-tamanho)/passo+1)
    infMutua = np.zeros(nJanelas)
    hQ=auxInfMut(query)
    for i in range(nJanelas):
        aux=target[i:tamanho+i]
        hT=auxInfMut(aux)
        cQT=np.zeros((len(alfabeto),len(alfabeto)))
        for a in range(tamanho):
            cQT[query[a]][aux[a]]+=1
        hQT=entropia(cQT) #calcula a entropia conjunta
        infJanela=hQ+hT-hQT
        infMutua[i]=infJanela
    print(infMutua)
    return infMutua
   
def entropia(numOco): #calcula a entropia
    np.asarray(numOco)
    entropia=0
    p = numOco / np.sum(numOco)
    p=p[p>0]
    entropia = -np.sum(p*np.log2(p))
    return entropia

def lerAudio(ficheiro): #lê um audio e retorna os dados,alfabeto e entropia
    [fs,P]=wavfile.read(ficheiro)
    P=P.flatten()
    A=descobrirAlfabeto(P)
    values , counts = np.unique(P,return_counts=True)
    return P,A,entropia(counts)

def ex6c():
    query,alfabeto,entropia=lerAudio("guitarsolo.wav")
    maximos=[]
    for i in range(1,8):
        target,alf,entropia2=lerAudio("Song0"+str(i)+".wav")
        passo=int(len(query)/4)
        infMutua=informacaoMutua(query,target,alfabeto,passo)
        maximo=max(infMutua)
        maximos.append(maximo)
        print(maximo)
    maximos.sort()
    print(maximos)

def main():
    ex6c()
    
if __name__ =="__main__":
    main()