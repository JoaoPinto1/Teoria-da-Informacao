import numpy as np

def entropia(numOco): #calcula a entropia
    np.asarray(numOco)
    entropia=0
    p = numOco / np.sum(numOco)
    p=p[p>0]
    entropia = -np.sum(p*np.log2(p))

    return entropia

def auxInfMut(q): #funcao auxiliar para calcular a entropia de um conjunto para a informacao mutua
    dic={}
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

def main():
    query=[2,6,4,10,5,9,5,8,0,8]
    target = [6,8,9,7,2,4,9,9,4,9,1,4,8,0,1,2,2,6,3,2,0,7,4,9,5,4,8,5,2,7,8,0,7,4,8,5,7,4,3,2,2,7,3,5,2,7,4,9,9,6]
    A=[0,1,2,3,4,5,6,7,8,9,10]
    informacaoMutua(query, target, A, 1)
    
if __name__ =="__main__":
    main()