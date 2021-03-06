import numpy as np
from numpy.polynomial import Polynomial
import numpy.linalg as alg
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D

##Méthode de détermination des valeurs propres par l'algorithme de Leverrier :

#On fait tout d'abord une fonction permettant de calculer la suite des valeurs Mk que l'on range dans une liste
def M(A):
    n = len(A)
    I = np.eye(n)
    L = [A]
    for i in range(1,n):
        D = L[-1]
        M = np.dot(A,(D-(np.trace(D)/i)*I))
        L.append(M)
    return L

#Ensuite, on calcul le polynome caractéristique avec la méthode annoncée
def Leverrier(A):
    n = len(A)
    L = M(A) #dans cette liste, Mk est à la kieme position
    P = []
    for k in range(n):
        P.append(-np.trace(L[n-k-1])/(n-k))
    P.append(1)
    return Polynomial(P)

#On va donc calculer les racines de ce polynome qui sont les valeurs propres de A
def valeurs_propres(A):
    p = Leverrier(A)
    return p.roots()


## Diagonalisation de la matrice M

def D(M):
    n = len(M)
    D = np.zeros((n,n))
    vp = valeurs_propres( M )
    for i in range(n):
        D[i,i] = vp[i]
    return D
    
def Q(M):
    n = len(l)
    vp = valeurs_propres( M )
    X0 = np.zeros((1,n))
    Q = np.zeros((n,0))
    for i in range(n):
        S = M-vp[i]*np.eye(n)
        X = np.linalg.solve(S,X0)
        Q = np.concatenate(Q,X,axis=1)
    return Q

def diagonalisation(M):
    Q=Q(M)
    return alg.inv(Q),D(M),Q
    
    
## Je fais une fonction qui va renvoyer la matrice colonne des fonctions de H et L

#La fonction qui suit se place comme un moyen d'application de l'algorithme construit jusqu'ici, celle-ci est faite dans le but de s'executer en un temps minimum
#On a tout d'abord besoin des valeurs
G = 6.67408*(10**-11)
Ms = 1.989*(10**30)
m = [3.285*(10**23), 4.867*(10**24), 5.972*(10**24), 6.39*(10**23), 1.898*(10**27), 5.863*(10**26), 8.681*(10**25), 1.024*(10**26)]
a = [57909227000, 108208475000, 149598262000, 227943824000, 778340821000, 1426666422000, 2870658186000, 4498396441000]
n = [ np.sqrt(G*Ms/(a[i]**3)) for i in range(8) ]

def Fourier(n,i,j):
    alp = a[i]/a[j]
    def signal(t):
        return alp*np.cos(n*t)/(a[j]*((1+(alp**2)-2*alp*np.cos(t))**(3/2)))
    return integr.quad(signal,-np.pi,np.pi)[0]/np.pi

#Calcul du tableau de coefficients N(p,v)
def N():
    n = len(m)
    N=np.zeros((n,n))
    for i in range(n):
        for j in range(i,n):
            Nij = Fourier(1,i,j)/8
            N[i,j],N[j,i] = Nij, Nij
    return N

N = N()

#Calcul du tableau de coefficients P(p,v)
def P():
    n = len(m)
    P=np.zeros((n,n))
    for i in range(n):
        for j in range(i,n):
            Pij = Fourier(2,i,j)/8
            P[i,j],P[j,i] = Pij, Pij
    return P
    
P = P()

#Calcul des coefficient (p,v)
def coef_p(p,v):
    return (2*f*m[v]*N[p,v]/(n[p]*(a[p]**2)))
    
#Calcul des coefficient [p,v]
def coef_c(p,v):
    return (2*f*m[v]*P[p,v]/(n[p]*(a[p]**2)))

#Calcul de A
def A(l):
    n = len(l)
    A = np.zeros((n,n))
    for i in l:
        for j in l:
            if i==j:
                s_i = 0
                for k in l:
                    if k != i:
                        s_i += coef_p(i,k)
                A[i,i] = s_i
            else:
                A[i,j] = -coef_c(i,j)
    return A

#On résoud le système. Cette fonction prend en entrée les listes des conditions initiales et renvoie 2 tableaux de fonctions
def resol_totale(l,CI1,CI2):
    n=len(l)
    A=A(l)
    B=np.dot(A,A)
    iP,D,P = diagonalisation(B)
    #Fait la résolution pour la matrice D du système et renvoie un tableau contenant les constantes à l'aide de R1 et R2, qui sont les matrices colonnes contenant les conditions initiales
    def resol_red(R1,R2):
        K = np.zeros((n,3))
        for i in range(n):
            wi = np.sqrt(D[i,i])
            K[i,2] = wi                         #pulsation
            for j in range(n):
                K[i,0] += P[i,j]*R1[l[j]]       #Ai
                Cj = 0
                for k in range(n):
                    Cj += A[j,k]*R2[l[k]]
                K[i,1] += P[i,j]*Cj
                K[i,1] = K[i,1]/wi              #Bi
        return K
    K=resol_red(CI1,CI2)
    J=resol_red(CI2,CI1)
    def dered(C):          #Va renvoyer un tableau de fonctions et "déréduire" la solution
        def add_func(f,g):
            return lambda x: f(x) + g(x)
        H=[lambda x:0 for i in range(n)]
        for i in range(n):
            for j in range(n):
                H[i] = add_func (H[i],(lambda x: iP[i,j]*(C[j,0]*np.cos(C[j,2]*x)+C[j,1]*np.sin(C[j,2]*x))))
        return H
    return dered(K), dered(J)

'''
H,L=resol_totale(l,H0,L0)
P,Q=resol_totale(l,P0,Q0)
'''
