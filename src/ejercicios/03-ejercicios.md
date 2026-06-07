### Ejercicio 3.1

Si tenemos dos números complejos

$$
\begin{align}
u&=a+bi\\
v&=c+di
\end{align}
$$

podemos calcular su producto $z=x+yi$ calculando

$$
\begin{align}
x&=ac-bd\\
y&=ad+bc
\end{align}
$$

lo cual requiere hacer 4 multiplicación de números reales.

El siguiente código implementa este cálculo:


```python
def mult4(u,v):
  # Recibe dos números complejos como pares ordenados
  # y retorna su producto utilizando 4 multiplicaciones
  (a,b)=u
  (c,d)=v
  x=a*c-b*d
  y=a*d+b*c
  return (x,y)

print(mult4((0,1),(0,1)))
print(mult4((2,-4),(1,3)))
print(mult4((-1,2),(3,4)))
```

Encuentre una forma de realizar este cálculo **haciendo solo 3 multiplicaciones de números reales**.
Escriba las fórmulas respectivas y luego escriba el código para la siguiente función:

```python
def mult3(u,v):
  # Recibe dos números complejos como pares ordenados
  # y retorna su producto utilizando solo 3 multiplicaciones
  (a,b)=u
  (c,d)=v

  # Escriba aquí las instrucciones para calcular x, y

  return (x,y)

print(mult3((0,1),(0,1)))
print(mult3((2,-4),(1,3)))
print(mult3((-1,2),(3,4)))
```

### Ejercicio 3.2

Si $f_n$ son los números de Fibonacci, demuestre que, para todo $n\ge 1$,

$$
\begin{pmatrix}
1 & 1\\
1 & 0
\end{pmatrix}^n
=
\begin{pmatrix}
f_{n+1} & f_n \\
f_n & f_{n-1}
\end{pmatrix}
$$
### Ejercicio 3.3

Se tiene una lista $A$ que consta de un conjunto de números ceros seguidos por un conjunto de números unos. Un ejemplo de lista $A$ es el siguiente:

$$
[0,0,0,0,0,0,0,0,0,1,1,1]
$$

Implemente la función "contar_ceros" que use la estrategia "dividir  para reinar" y que devuelve la cantidad de ceros de la lista de entrada en tiempo $O(\log{n})$

```python
def contar_ceros(A, i, j):
  #La función recibe la lista A y los índices i, j que indican dónde empieza
  #y dónde termina la lista que actualmente se está analizando.
  #La primera vez la función se llamará como contar_ceros(A, 0, len(A)-1)

  pass

```

Usa estos tests para comprobar que tu función está correcta

```python
print("OK" if contar_ceros([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1], 0, 16)==13 else "Error")
print("OK" if contar_ceros([0,1,1,1,1,1,1,1,1],0,8)==1 else "Error")
print("OK" if contar_ceros([1,1,1,1,1],0,4)==0 else "Error")
print("OK" if contar_ceros([0,0,0,0,0,0,0],0,6)==7 else "Error")
```

### Ejercicio 3.4

Modifique la función ``LCS`` para que retorne una subsecuencia común más larga, en lugar de retornar su longitud.

Recordemos que el algoritmo del apunte va llenando una martiz $L$, donde $L[i,j]$ contiene el largo de la subsecuencia común mas larga entre $a[0:i]$ y $b[0:j]$. Su algoritmo modificado debe ir llenando en paralelo una matriz $S$, tal que $S[i,j]$ contenga un string que es la subsecuencia común más larga entre $a[0:i]$ y $b[0:j]$.

Para ayudarlo, el siguiente código ya tiene la definición de la matriz y la inicialización respectiva. Usted tiene que encargarse de modificar todo lo demás que sea necesario para cumplir con lo pedido.

```python
import numpy as np
def LCS(a,b):
    """
    Encuentra el largo de la subsecuencia común más larga entre a y b
    """
    m=len(a)
    n=len(b)
    L=np.zeros((m+1,n+1),dtype=int)
    S=np.empty((m+1,n+1),dtype=object)
    for i in range(0,m+1):
      S[i,0]=""
    for j in range(0,n+1):
      S[0,j]=""
    for i in range(1,m+1):
        for j in range(1,n+1):
            if a[i-1]==b[j-1]:
                L[i,j]=1+L[i-1,j-1]

            else: # lo siguiente es equivalente a L[i,j]=max(L[i-1,j],L[i,j-1])
                if L[i-1,j]>L[i,j-1]:
                    L[i,j]=L[i-1,j]

                else:
                    L[i,j]=L[i,j-1]


    return S[m,n]
```


```python
assert LCS("abracadabra","pasapalabra")=="aaaabra"
```


```python
assert LCS("matemáticas","computación") in ["mta", "mti", "mai"]
```

### Ejercicio 3.5

Modifique la función para que marque con `"."` los casilleros por donde hubo intentos no exitosos de salir, y con `"x"` los casilleros que finalmente condujeron a la salida.

```python
def salida(i,j):
    if L[i][j]=="=": # encontramos la salida
        return True
    if L[i][j]!=" ": # espacio ocupado
        return False
    L[i]=L[i][:j]+"x"+L[i][j+1:]
    if salida(i,j-1) \
    or salida(i,j+1) \
    or salida(i-1,j) \
    or salida(i+1,j):
        return True
    return False

L = [
"+--+-----+--+",
"|  |     |  |",
"|  +--+     =",
"|     |  |  |",
"+--+  |  |  |",
"|  |        |",
"|  |     |  |",
"+--+-----+--+"
]
print(salida(4,10))
for linea in L:
    print(linea)
```

Además, pruebe el caso salida(1,1) y muestre el resultado.

```python
L = [
"+--+-----+--+",
"|  |     |  |",
"|  +--+     =",
"|     |  |  |",
"+--+  |  |  |",
"|  |        |",
"|  |     |  |",
"+--+-----+--+"
]
print(salida(1,1))

for linea in L:
    print(linea)
```
