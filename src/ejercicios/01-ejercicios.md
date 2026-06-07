### Ejercicio 1.1

La función ``maximo`` hace $n-1$ comparaciones de elementos para encontrar el máximo de un conjunto de tamaño $n$.


```python
# Encuentra el máximo de una lista a
def maximo(a):
    m=a[0]
    # Al comenzar cada iteración, se cumple que m==max(a[0],...,a[k-1])
    for k in range(1,len(a)):
        if a[k]>m:
            m=a[k]
    return m

print(maximo([25, 42, 93, 17, 54, 28]))
```


```
93

```

Supongamos que se desea escribir una función ``minmax`` que al ser llamada con una lista de números, retorne un par ordenado (tupla) ``(min,max)``, con el mínimo y el máximo elemento del conjunto, respectivamente. Escriba a continuación esa función haciendo dos pasadas sobre los datos: una para encontrar el mínimo y otra para encontrar el máximo, y pruébela sobre una lista de ejemplo.

```python
def minmax(a):
    # escribir la función aquí

    return(minimo,maximo)

# Probarla acá
```

La función anterior debería hacer $2n-2$ comparaciones de elementos ($2n-3$ si se evita comparar el elemento seleccionado en la primera pasada). ¿Será posible encontrar el mínimo y el máximo haciendo muchas menos comparaciones?

¡La respuesta es que sí! Veámoslo con un ejemplo. Para simplificar, supongamos que la lista es de largo par:

$$
[45,21,34,67,55,89,44,12]
$$

Luego comparemos cada elemento que está en una posición par con su vecino de la derecha, e intercambiémoslos de modo que el par quede en orden ascendente (recuerde que las posiciones comienzan desde cero):

$$
[21,45,34,67,55,89,12,44]
$$

Luego hagamos una pasada solo sobre las posiciones pares para encontrar el mínimo ($12$), y otra pasada solo entre las posiciones impares para encontrar el máximo ($89$). ¡Listo!

Programe este nuevo algoritmo, pruébelo y diga cuántas comparaciones hace en total:

---

```python
def minmax(a):
    # escribir la función aquí

    return(minimo,maximo)

# Probarla acá
```

### Ejercicio 1.2

Existe un algoritmo alternativo a Hoare, que resulta en una codificación más sencilla. Este algoritmo, debido a **Lomuto**, se basa en el siguiente invariante:

![particion-Lomuto](https://github.com/ivansipiran/AED-Apuntes/blob/main/recursos/particion-Lomuto.png?raw=1)

En este algoritmo, en cada iteración, si $a[j]<p$, se intercambian $a[i]$ con $a[j]$ y se incrementa $i$, porque ahora hay un elemento más en el grupo de los menores que $p$. Después de esto, se incrementa $j$, *incondicionalmente* (¿por qué es correcto hacer eso?).

Programe la partición de Lomuto en el recuadro siguiente y pruébela.

```python
def particionLomuto(a,p):
    # retorna el punto de corte, el número de elementos <p y la lista particionada

    # escribir acá el algoritmo de partición de Lomuto

    return (p,i,a)
```


```python
def verifica_particion(t): # imprime y chequea partición
    (p,m,a)=t
    # p=punto de corte, m=número de elementos <p, a=lista completa particionada
    print(a[0:m],p,a[m:])
    print("Partición OK" if (m==0 or max(a[0:m])<p) and (m==len(a) or min(a[m:])>p)
          else "Error")
```


```python
verifica_particion(particionLomuto([73,21,34,98,56,37,77,65,82,15,36],50))
```


```python
verifica_particion(particionLomuto([73,21,34,98,56,37,77,65,82,15,36],0))
```


```python
verifica_particion(particionLomuto([73,21,34,98,56,37,77,65,82,15,36],100))
```

### Ejercicio 1.3

Un polinomio se puede evaluar en tiempo lineal sin necesidad de una variable auxiliar si observamos que $P(x)$ se puede factorizar como:

$$
P(x) = a_0 +x(a_1+x(\cdots+x(a_{n-1}+x(a_n))\cdots))
$$

Por ejemplo,

$$
\begin{align}
P(x) &= 5+2x-3x^2+4x^3\\
 &=5+x(2+x(-3+x(4)))
\end{align}
$$

Programe un algoritmo iterativo que evalúe el polinomio utilizando esta idea. Comience desde el paréntesis más interno y vaya avanzando hacia la izquierda. Indique cuál es el invariante que utiliza. El algoritmo resultante se llama la **Regla de Horner**.

```python
def evalp(a,x):
    """Evalúa en el punto x el polinomio cuyos coeficientes son a[0], a[1],...
    utilizando la Regla de Horner
    Retorna el valor calculado
    """
    # Escriba aquí su algoritmo

    return P
```


```python
print(evalp([5,2,-3,4],2))
```

### Ejercicio 1.4

Suponga que se tiene una matriz $A$ tal que los elementos de cada fila están ordenados ascendentemente, y de la misma manera, los elementos de cada columna también están en orden ascendente. Por ejemplo:

```python
import numpy as np

A = np.array([[10,17,25,36,50,82],
           [15,19,28,45,63,87],
           [21,30,42,56,77,91],
           [27,35,74,84,90,95],
           [40,62,81,86,93,98]])
print(A)
```


```
[[10 17 25 36 50 82]
 [15 19 28 45 63 87]
 [21 30 42 56 77 91]
 [27 35 74 84 90 95]
 [40 62 81 86 93 98]]

```

Para simplificar, vamos a suponer que no hay elementos repetidos en la matriz.

Se desea escribir una función que, dado un número $x$, lo busque dentro de la matriz $A$. Si lo encuentra, debe retornar una tupla $(i,j)$ tal que $A[i,j]=x$. Si no lo encuentra debe retornar `None`.

Si la matriz es de $m\times n$, se podría hacer una búsqueda secuencial, la cual en el peor caso demoraría un tiempo proporcional a $m n$. El objetivo de este ejercicio es desarrollar un algoritmo más eficiente, que haga la búsqueda en un tiempo proporcional a $m+n$.

La idea es comenzar comparando $x$ contra el elemento de la esquina inferior izquierda de la matriz, es decir, $A[m-1,0]$. Si $x$ es igual a ese elemento, el algoritmo termina exitosamente. Si no, vemos si $x$ es mayor o menor que él, y dependiendo de eso, podemos ya sea descartar esa fila o esa columna. El proceso se repite con la parte restante de la matriz.

De esta manera, al comenzar una nueva iteración, el invariante sería que la parte de la matriz en donde todavía podría encontrarse $x$ son las filas de la $0$ hasta la $i$ y las columnas desde la $j$ hasta la $n-1$, como ilustra la siguiente figura:

![invariante-matriz](https://github.com/ivansipiran/AED-Apuntes/blob/main/recursos/invariante-matriz.png?raw=1)

La parte de color gris son las filas y columnas que ya han sido descartadas.

Escriba aquí su función y ejecute las pruebas que se indican a continuación:

```python
# Busca x en la matriz A
def busca(x,A):
  (m,n)=np.shape(A)
  # Escriba aquí su algoritmo de búsqueda
```


```python
print(busca(28,A)) # Debe imprimir (1,2)
```


```python
print(busca(82,A)) # Debe imprimir (0,5)
```


```python
print(busca(33,A)) # Debe imprimir None
```

### Ejercicio 1.5

Se le llama "Camel Case" a la convención de escribir una frase sin espacios, pero marcando el inicio de cada palabra poniendo su primera letra en mayúscula. Por ejemplo, la frase
```
"  Algoritmos y    estructuras de   datos   "
```
transformada a Camel Case queda así:
```
"AlgoritmosYEstructurasDeDatos"
```

Escriba una función que transforme a Camel Case y pruébela:

```python
def CamelCase(s):
    """Retorna un string conteniendo la versión Camel Case del string s"""
    # escriba aquí su algoritmo
```


```python
print(CamelCase("    Algoritmos y    estructuras de   datos   "))
```

### Ejercicio 1.6 - Permutaciones

Una función recursiva que genera e imprime todas las permutaciones de un arreglo se puede plantear
de la siguiente manera:

~~~python
def permutaciones(x,ini,fin):
~~~
   genera las permutaciones del arreglo x desde el elemento
   con índice ini hasta el elemento con índice fin  
   
- Si $ini$ es igual a $fin$ implica que se pide la permutación de un solo elemento, y en ese momento se imprime
  todo el contenido del arreglo
- De lo contrario, para todos los elementos $x[i]$ con $i$ desde $ini$ hasta $fin$ ($fin$ incluido) se hace lo siguiente:
                 . se intercambia el valor del i-ésimo elemento con el inicial
                 . se llama recursivamente a la función permutaciones con el
                    índice del primer elemento incrementado: permutaciones(x, ini+1, fin)
                 . Se vuelven a restaurar los valores del elemento inicial con el i-ésimo

Implemente la función "permutaciones" que imprima todas las permutaciones de un arreglo de entrada. Probar su función con arreglos de tamaño 1, 3 y 5.
### Ejercicio 1.7 - Generando números binarios
Una función recursiva que genera e imprime todos los números binarios de ``n`` dígitos se puede plantear con un encabezado de la siguiente manera:

```python
def genera_binarios(a,k,n):
    #Aquí debes definir tu código

```

Donde ``a`` es un arreglo que contiene los unos y ceros de los números que se van generando, el cual se va rellenando con valores de izquierda a derecha, ``k`` es el grado de avance en el proceso de generación (más precisamente cuantos dígitos se han generado hasta esta llamada) y ``n`` es la cantidad total de dígitos que deben generarse (``n = len(a)``). Por lo tanto ``n-k`` es la cantidad de dígitos que faltan por generar. Esta función se llama la primera vez de la siguiente manera:

```python
import numpy as np
n = 4
a = np.empty(n,dtype=int) # arreglo de largo n sin inicializar
genera_binarios(a,0,len(a))
```

Este código debe generar la salida:

[0 0 0 0]

[0 0 0 1]

[0 0 1 0]

[0 0 1 1]

[0 1 0 0]

[0 1 0 1]

[0 1 1 0]

[0 1 1 1]

[1 0 0 0]

[1 0 0 1]

[1 0 1 0]

[1 0 1 1]

[1 1 0 0]

[1 1 0 1]

[1 1 1 0]

[1 1 1 1]
Se le pide que escriba las instrucciones de la función ``genera_binarios`` de acuerdo al siguiente algoritmo:

---



* si el valor de ``k`` es igual a ``n``, ya se han generado todos los dígitos por
    lo cual se imprime el arreglo en pantalla ``(print(a))``
* si no, se hacen dos cosas:  
    - se pone un 0 en la ``k``-ésima posicion y se llama recursivamente
      a la función para que genere los dígitos restantes
    - luego se pone un 1 en la misma ``k``-ésima posición (reemplazando el 0) y se
      llama recursivamente a la función para que genere los dígitos restantes

Pruebe su función con para el caso ``n=4``. Asegúrese de que genere el mismo resultado que el que aparece en el enunciado.
