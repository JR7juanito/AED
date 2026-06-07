# 7 Ordenación

El problema de ordenar un conjunto de datos (por ejemplo, en orden ascendente) tiene gran importancia tanto teórica como práctica. En esta sección veremos principalmente algoritmos que ordenan mediante comparaciones entre llaves, para los cuales se puede demostrar una cota inferior que coincide con la cota superior provista por varios algoritmos. También veremos un algoritmo de otro tipo, que al no hacer comparaciones, no está sujeto a esa cota inferior.
## Cota inferior

Supongamos que deseamos ordenar tres datos $A$, $B$ y $C$. La siguiente figura muestra un árbol de decisión posible para resolver este problema. Los nodos internos del árbol representan comparaciones y los nodos externos representan salidas emitidas por el programa.

![arbol-decision-ordenacion](recursos/arbol-decision-ordenacion.gif)

Como se vio en el capítulo de búsqueda, todo árbol de decisión con $H$ hojas tiene al menos altura $\log_2{H}$, y la altura del árbol de decisión es igual al número de comparaciones que se efectúan en el peor caso.

En un árbol de decisión para ordenar $n$ datos se tiene que $H=n!$, y por lo tanto se tiene que todo algoritmo que ordene $n$ datos mediante comparaciones entre llaves debe hacer al menos $\log_2{n!}$ comparaciones en el peor caso.

Usando la aproximación de Stirling, se puede demostrar que $\log_2{n!} = n \log_2{n} + \Theta(n)$, por lo cual la cota inferior es de $\Theta(n\log{n})$.

Si suponemos que todas las posibles permutaciones resultantes son equiprobables, es posible demostrar también que el número promedio de comparaciones que cualquier algoritmo debe hacer es también de $\Theta(n\log{n})$.
## Quicksort

Este método fue inventado por C.A.R. Hoare a comienzos de los '60s, y sigue siendo el método más eficiente para uso general.

Quicksort es un ejemplo clásico de la aplicación del principio de *dividir para reinar*. Su estructura es la siguiente:

* Primero se elige un elemento al azar, que se denomina el pivote.

* El arreglo a ordenar se reordena dejando a la izquierda a los elementos menores que el pivote, el pivote al medio, y a la derecha los elementos mayores que el pivote:

![particion](recursos/particion.gif)

* Luego cada sub-arreglo se ordena recursivamente.

La recursividad termina, en principio, cuando se llega a sub-arreglos de tamaño cero o uno, los cuales trivialmente ya están ordenados. En la práctica veremos que es preferible detener la recursividad antes de eso, para no desperdiciar tiempo ordenando recursivamente arreglos pequeños, los cuales pueden ordenarse más eficientemente usando Ordenación por Inserción, por ejemplo.

```python
def quicksort(a):
    qsort(a,0,len(a)-1)

def qsort(a,i,j): # ordena a[i],...,a[j]
    if i<j: # quedan 2 o más elementos por ordenar
        k=particion(a,i,j)
        qsort(a,i,k-1)
        qsort(a,k+1,j)

def particion(a,i,j): # particiona a[i],...,a[j], retorna posición del pivote
    k=np.random.randint(i,j) # genera un número al azar k en rango i..j
    (a[i],a[k])=(a[k],a[i]) # mueve a[k] al extremo izquierdo
    # a[i] es el pivote
    s=i # invariante: a[i+1..s]<=a[i], a[s+1..t]>a[i]
    for t in range(s,j):
        if a[t+1]<=a[i]:
            (a[s+1],a[t+1])=(a[t+1],a[s+1])
            s=s+1
    # mover pivote al centro
    (a[i],a[s])=(a[s],a[i])
    return s
```


```python
def chequea_orden(a):
    print("Ordenado" if np.all(a[:-1]<=a[1:]) else "Desordenado")
```


```python
import numpy as np
a = np.random.random(12)
print(a)
chequea_orden(a)
quicksort(a)
print(a)
chequea_orden(a)
```


```
[0.21939313 0.41324672 0.99870279 0.15140399 0.33302848 0.92304672
 0.11206401 0.63418302 0.64504804 0.50401626 0.2064129  0.81939607]
Desordenado
[0.11206401 0.15140399 0.2064129  0.21939313 0.33302848 0.41324672
 0.50401626 0.63418302 0.64504804 0.81939607 0.92304672 0.99870279]
Ordenado

```

### Costo promedio de Quicksort

Si suponemos, como una primera aproximación, que el pivote siempre resulta ser la mediana del conjunto, entonces el costo de ordenar está dado (aproximadamente) por la ecuación de recurrencia

$$
T(n)=n+2T\left( \frac{n}{2} \right)
$$

Esto tiene solución $T(n) = n \log_2{n}$ y es, en realidad, el *mejor* caso de Quicksort.

Para analizar el tiempo promedio que demora la ordenación mediante Quicksort, observemos que el funcionamiento de Quicksort puede graficarse mediante un *árbol de partición*:

![arbol-particion](recursos/arbol-particion.gif)

Por la forma en que se construye, es fácil ver que el árbol de partición es un *árbol de búsqueda binaria*, y como el pivote es escogido al azar, entonces la raíz de cada subárbol puede ser cualquiera de los elementos del conjunto en forma equiprobable. En consecuencia, los árboles de partición y los árboles de búsqueda binaria tienen exactamente la misma distribución.

En el proceso de partición, cada elemento de los subárboles ha sido comparado contra la raíz (el pivote). Al terminar el proceso, cada elemento ha sido comparado contra todos sus ancestros. Si sumamos todas estas comparaciones, el resultado total es igual al *largo de caminos internos*.

Usando todas estas correspondencias, tenemos que, usando los resultados ya conocidos para árboles, el número promedio de comparaciones que realiza Quicksort es de:

$$
T(n)=1.38 n\log_2{n}+\Theta(n)
$$

Por lo tanto, Quicksort, en el caso esperado, corre en un tiempo proporcional a la cota inferior.
### Peor caso de Quicksort

El peor caso de Quicksort se produce cuando el pivote resulta ser siempre el mínimo o el máximo del conjunto. En este caso la ecuación de recurrencia es

$$
T(n) = n - 1 + T(n-1)
$$
            
lo que tiene solución $T(n) = \Theta(n^2)$. Desde el punto de vista del árbol de partición, esto corresponde a un árbol en "zig-zag".

Si bien este peor caso es extremadamente improbable si el pivote se escoge al azar, algunas implementaciones de Quicksort toman como pivote al primer elemento del arreglo (suponiendo que, al venir el arreglo al azar, entonces el primer elemento es tan aleatorio como cualquier otro). El problema es que si el conjunto viene en realidad ordenado, entonces caemos justo en el peor caso cuadrático.

Lo anterior refuerza la importancia de que el pivote se escoja al azar. Esto no aumenta significativamente el costo total, porque el número total de elecciones de pivote es $\Theta(n)$.
### Mejoras a Quicksort

Quicksort puede ser optimizado de varias maneras, pero hay que ser muy cuidadoso con estas mejoras, porque es fácil que terminen empeorando el desempeño del algoritmo.

En primer lugar, es desaconsejable hacer cosas que aumenten la cantidad de trabajo que se hace dentro del "loop" de partición, porque este es el lugar en donde se concentra el costo $\Theta(n \log{n})$.

Algunas de las mejoras que han dado buen resultado son las siguientes:
#### Quicksort con "mediana de 3"

En esta variante, el pivote no se escoge como un elemento tomado al azar, sino que primero se extrae una muestra de 3 elementos, y entre ellos se escoge a la mediana de esa muestra como pivote.

Si la muestra se escoge tomando al primer elemento del arreglo, al del medio y al último, entonces lo que era el peor caso (arreglo ordenado) se transforma de inmediato en mejor caso.

De todas formas, es aconsejable que la muestra se escoja al azar, y en ese caso el análisis muestra que el costo esperado para ordenar n elementos es

$$
\frac{12}{7} n \ln{n}  \approx  1.19 n \log_2{n}
$$

Esta reducción en el costo se debe a que el pivote es ahora una mejor aproximación a la mediana. De hecho, si en lugar de escoger una muestra de tamaño 3, lo hiciéramos con tamaños como 7, 9, etc., se lograría una reducción aún mayor, acercándonos cada vez más al óptimo, pero con rendimientos rápidamente decrecientes.
---
#### Uso de Ordenación por Inserción para ordenar sub-arreglos pequeños

Tal como se dijo antes, no es eficiente ordenar recursivamente sub-arreglos demasiado pequeños.

En lugar de esto, se puede establecer un tamaño mínimo $M$, de modo que los sub-arreglos de tamaño menor que esto se ordenan por inserción en lugar de por Quicksort.

Claramente debe haber un valor óptimo para $M$, porque si creciera indefinidamente se llegaría a un algoritmo cuadrático. Esto se puede analizar, y el óptimo es cercano a 10.

Como método de implementación, al detectarse un sub-arreglo de tamaño menor que $M$, se lo puede dejar simplemente sin ordenar, retornando de inmediato de la recursividad. Al final del proceso, se tiene un arreglo cuyos pivotes están en orden creciente, y encierran entre ellos a bloques de elementos desordenados, pero que ya están en el grupo correcto. Para completar la ordenación, entonces, basta con hacer una sola gran pasada de Ordenación por Inserción, la cual ahora no tiene costo $\Theta(n^2)$, sino $\Theta(nM)$, porque ningún elemento está a distancia mayor que $M$ de su ubicación definitiva.
#### Ordenar recursivamente sólo el sub-arreglo más pequeño

Un problema potencial con Quicksort es la profundidad que puede llegar a tener la recursividad. En el peor caso, ésta puede llegar a ser $\Theta(n)$.

Para evitar esto, se puede usar recursividad solo para la "mitad" más pequeña, y ordenar la otra "mitad" de manera iterativa. Con este enfoque, cada llamada recursiva se aplica a un sub-arreglo cuyo tamaño es a lo más la mitad del tamaño del arreglo a ordenar, de modo que si llamamos $S(n)$ a la profundidad de recursión, tenemos que

$$
S(n) \le 1 + S\left(\frac{n}{2}\right)
$$

lo cual tiene solución $\log_2{n}$, de modo que la profundidad de la recursión nunca es más que logarítmica.

```python
def qsort(a,i,j): # ordena a[i],...,a[j]
    while i<j: # quedan 2 o más elementos por ordenar
        k=particion(a,i,j)
        if k-i<=j-k: #mitad izquierda es más pequeña
            qsort(a,i,k-1)
            i=k+1
        else:
            qsort(a,k+1,j)
            j=k-1
```


```python
import numpy as np
a = np.random.random(6)
print(a)
quicksort(a)
print(a)
```


```
[0.66656624 0.76798384 0.87811887 0.74763235 0.30180187 0.82056957]
[0.30180187 0.66656624 0.74763235 0.76798384 0.82056957 0.87811887]

```

### Un algoritmo de selección basado en Quicksort

Es posible modificar el algoritmo de Quicksort para seleccionar el $k$-ésimo elemento de un arreglo $a[0],\ldots,a[n-1]$, esto es, el elemento que quedaría en la posición $a[k]$ si el arreglo se ordenara. Una solución trivial sería, precisamente, ordenar el arreglo y retornar ese elemento, pero la pregunta es si eso se puede hacer de manera más eficiente.

Una idea para resolver este problema idea es ejecutar Quicksort, pero en lugar de ordenar las dos mitades, hacerlo solo con aquella mitad en donde se encontraría el elemento buscado, o incluso no hacer nada si tenemos suerte y el pivote quedó justo en la posición $a[k]$.

```python
def quickselect(a,k):
    assert k>=0 and k<len(a)
    qselect(a,k,0,len(a)-1)
    return a[k]

def qselect(a,k,i,j): # selecciona el elemento que quedaría en a[k]
                      # si se ordenara a[i],...,a[j] (i<=k<=j)
    if i<j:
        p=particion(a,i,j)
        if p!=k:
            if k<p:
                qselect(a,k,i,p-1)
            else:
                qselect(a,k,p+1,j)
```


```python
import numpy as np
a = np.random.random(6)
print(a)
k=int(input("k="))
print(quickselect(a,k))
```


```
[0.19052461 0.578469   0.14702632 0.62380414 0.21373454 0.59978106]
k=4
0.5997810643996624

```

En realidad la recursividad de ``qselect`` es fácil de transformar en iteración, y una vez hecho eso ya no hay razón para que sea una función aparte:

```python
def quickselect(a,k):
    assert k>=0 and k<len(a)
    i=0
    j=len(a)-1
    while i<j:
        p=particion(a,i,j)
        if p==k:
            break
        if k<p:
            j=p-1
        else:
            i=p+1
    return a[k]
```


```python
import numpy as np
a = np.random.random(6)
print(a)
k=int(input("k="))
print(quickselect(a,k))
```


```
[0.28147833 0.06014974 0.56597127 0.42582274 0.66869136 0.11621771]
k=3
0.4258227414342961

```

El análisis del costo esperado de Quickselect es complicado, pero se puede demostrar que es $\Theta(n)$. Por otra parte, el peor caso se da cuando el pivote cae siempre en un extremo, y en ese caso el costo es $\Theta(n^2)$.
### Un algoritmo de selección de tiempo lineal en el peor caso

La razón por la cual el algoritmo ``Quickselect`` puede demorar tiempo cuadrático en el peor caso es que el pivote puede resultar ser siempre el mínimo o el máximo, o un elemento muy cercano a los extremos.

Esta debilidad se subsanaría si pudiéramos garantizar que los elementos que quedan a cada lado del pivote son siempre al menos una cierta fracción fija del total, digamos $\alpha n$, para algún $\alpha \in (0,\frac12)$.

Una forma de lograrlo es la siguiente. Dividamos el conjunto completo de $n$ elementos en grupos de tamaño $5$, y encontremos la mediana de cada uno de estos pequeños conjuntos. Cada uno de ellos se puede visualizar como un orden parcial de la forma

![spider](recursos/spider.png)

donde los dos elementos de arriba son mayores que la mediana, y ésta es mayor que los dos de abajo.

A continuación, aplicamos este mismo algoritmo, recursivamente, para encontrar la **mediana de las medianas**. Este elemento, que se muestra encerrado en un círculo en el diagrama siguiente, será nuestro pivote:

![median-of-medians](recursos/median-of-medians.png)

Como se ve, todos los elementos encerrados en las líneas punteadas están garantizados de estar por sobre o por debajo del pivote, respectivamente.
Por lo tanto, en el peor caso, podemos garantizar que al menos $\frac{3}{10}n$ elementos son menores que el pivote, otros $\frac{3}{10}n$ son mayores que él.

Por lo tanto, en el peor caso, la llamada recursiva que se hace para continuar el proceso se aplica a un conjunto de a lo más $\frac{7}{10}n$ elementos.

Si llamamos $T(n)$ al tiempo que demora este algoritmo en el peor caso, y si $cn$ es el tiempo que demora encontrar las medianas de los $n/5$ subconjuntos, para alguna constante $c$, entonces tenemos que, en el peor caso,

$$
T(n)=cn+T\left(\frac{n}{5}\right)+T\left(\frac{7n}{10}\right)
$$

Esta ecuación tiene solución lineal. En efecto, supongamos que existe una constante $d$ tal que $T(n)=dn$. Reemplazando en la ecuación, tenemos

$$
dn=cn+\frac{dn}{5}+\frac{7dn}{10}
$$

de donde podemos despejar $d$ y obtener $d=10c$. Por lo tanto, $T(n)=10cn$, y el algoritmo demora tiempo $\Theta(n)$ en el peor caso.

La razón por la cual la ecuación admite solución lineal es porque los coeficientes de $n$ en las llamadas recursivas suman $\frac{1}{5}+\frac{7}{10}<1$. Eso explica por qué no habría funcionado haber dividido el conjunto en grupos de tamaño 3. En ese caso, los coeficientes habrían sido $\frac{1}{3}$ y $\frac{2}{3}$ respectivamente, y su suma no sería menor que $1$.
## Heapsort

A partir de cualquier implementación de una cola de prioridad es posible obtener un algoritmo de ordenación. El esquema del algoritmo es:

* Comenzar con una cola de prioridad vacía.
* *Fase de construcción de la cola de prioridad*:
Traspasar todos los elementos del conjunto que se va a ordenar a la cola de prioridad, mediante $n$ inserciones.
* *Fase de ordenación*:
Sucesivamente extraer el máximo $n$ veces. Los elementos van apareciendo en orden decreciente y se van almacenando en el conjunto de salida.

Si aplicamos esta idea a las dos implementaciones simples de colas de prioridad, utilizando lista enlazada ordenada y lista enlazada desordenada, se obtienen los algoritmos de ordenación por Inserción y por Selección, respectivamente. Ambos son algoritmos cuadráticos, pero es posible que una mejor implementación lleve a un algoritmo más rápido. En el capítulo de *Pilas y Colas* vimos que una forma de obtener una implementación eficiente de colas de prioridad es utilizando una estructura de datos llamada *heap*.
### Implementación de Heapsort

Al utilizar un heap como implementación de una cola de prioridad para construir un algoritmo de ordenación, se obtiene un algoritmo llamado *Heapsort*, para el cual resulta que tanto la fase de construcción de la cola de prioridad, como la fase de ordenación, tienen ambas costo $\Theta(n \log{n})$, de modo que el algoritmo completo tiene ese mismo costo.

Por lo tanto, Heapsort tiene un orden de magnitud que coincide con la cota inferior, esto es, es óptimo incluso en el peor caso. Nótese que esto no era así para Quicksort, el cual era óptimo en promedio, pero no en el peor caso.

De acuerdo a la descripción de esta familia de algoritmos, daría la impresión de que en la fase de construcción del heap se requeriría un arreglo aparte para el heap, distinto del arreglo de entrada. De la misma manera, se requeriría un arreglo de salida aparte, distinto del heap, para recibir los elementos a medida que van siendo extraídos en la fase de ordenación.

En la práctica, esto no es necesario y basta con un sólo arreglo: todas las operaciones pueden efectuarse directamente sobre el arreglo de entrada.

En primer lugar, en cualquier momento de la ejecución del algoritmo, los elementos se encuentran particionados entre aquellos que están ya o aún formando parte del heap, y aquellos que se encuentran aún en el conjunto de entrada, o ya se encuentran en el conjunto de salida, según sea la fase. Como ningún elemento puede estar en más de un conjunto a la vez, es claro que, en todo momento, en total nunca se necesita más de $n$ casilleros de memoria, si la implementación se realiza bien.

En el caso de Heapsort, durante la fase de construcción del heap, podemos utilizar las celdas de la izquierda del arreglo para ir "armando" el heap. Las celdas necesarias para ello se las vamos "quitando" al conjunto de entrada, el cual va perdiendo elementos a medida que van "trepando" en el heap. Al concluir esta fase, todos los elementos han sido insertados, y el arreglo completo es un solo gran heap.

![heap-cons](recursos/heap-cons.gif)

En la fase de ordenación, se van extrayendo elementos del heap, con lo cual éste se contrae de tamaño y deja espacio libre al final, el cual puede ser justamente ocupado para ir almacenando los elementos a medida que van saliendo del heap (recordemos que van apareciendo en orden decreciente).

![heap-ord](recursos/heap-ord.gif)
### Optimización de la fase de construcción del heap

Como se ha señalado anteriormente, tanto la fase de construcción del heap como la de ordenación demoran tiempo $\Theta(n \log{n})$. Esto es el mínimo posible (en orden de magnitud), de modo que no es posible mejorarlo significativamente.

Sin embargo, es posible modificar la implementación de la fase de construcción del heap para que sea mucho más eficiente.

La idea es invertir el orden de las "mitades" del arreglo, haciendo que el "input" esté a la izquierda y el "heap" a la derecha.

En realidad, si el "heap" está a la derecha, entonces no es realmente un heap, porque no es un árbol completo (le falta la parte superior), pero sólo nos interesa que en ese sector del arreglo se cumplan las relaciones de orden entre cada padre y sus hijos. En cada iteración, se toma el último elemento del "input" y se le "hunde" dentro del heap de acuerdo a su nivel de prioridad.

![heap-cons2](recursos/heap-cons2.gif)

Al concluir, se llega igualmente a un heap completo, pero el proceso es significativamente más rápido.

La razón es que, al ser "hundido", un elemento paga un costo proporcional a su distancia al fondo del árbol. Dada las características de un árbol, la gran mayoría de los elementos están al fondo o muy cerca de él, por lo cual pagan un costo muy bajo. En un análisis aproximado, la mitad de los elementos pagan 0 (ya están al fondo), la cuarta parte paga 1, la octava parte paga 2, etc. Sumando todo esto, tenemos que el costo total está acotado por

$$
n \sum_{i\ge 0}{\frac{i}{2^{i+1}}}
$$

lo cual es igual a $n$.

En la práctica, al comenzar a construir el heap "de abajo hacia arriba", no hace falta examinar los elementos que no tienen hijos, porque ellos cumplen automáticamente la relación de orden. Por lo tanto, basta comenzar a examinar los elementos desde el casillero $\lfloor \frac{n}{2} \rfloor-1$ hacia atrás.

```python
def hundir(a,j,n): # El elemento a[j] se hunde hasta su nivel de prioridad
    while 2*j+1<n: # mientras tenga al menos 1 hijo
        k=2*j+1 # el hijo izquierdo
        if k+1<n and a[k+1]>a[k]: # el hijo derecho existe y es mayor
            k+=1
        if a[j]>=a[k]: # tiene mejor prioridad que ambos hijos
            break
        (a[j],a[k])=(a[k],a[j]) # se intercambia con el mayor de los hijos
        j=k # bajamos al lugar del mayor de los hijos

def heapsort(a):
    n=len(a)
    # Fase de construcción del heap
    for i in range(n//2-1,-1,-1):
        hundir(a,i,n)
    # Fase de ordenación
    for i in range(n-1,-1,-1):
        (a[0],a[i])=(a[i],a[0])
        hundir(a,0,i)
```


```python
import numpy as np
a = np.random.random(6)
print(a)
heapsort(a)
print(a)
```


```
[0.58123276 0.57772293 0.22690173 0.49691097 0.78430617 0.16308228]
[0.16308228 0.22690173 0.49691097 0.57772293 0.58123276 0.78430617]

```

## Radix Sort

Los métodos anteriores operan mediante comparaciones de llaves, y están sujetos, por lo tanto, a la cota inferior $\Omega(n \log{n})$. Veremos a continuación el método *Radix Sort* (llamado también *Bucket Sort*), que opera de una manera distinta, y logra ordenar el conjunto en tiempo lineal.

Supongamos que queremos ordenar $n$ números, cada uno de ellos compuesto de $k$ dígitos decimales. El siguiente es un ejemplo con $n=10$, $k=5$.

```
    73895
    93754
    82149
    99046
    04853
    94171
    54963
    70471
    80564
    66496
```

Para comenzar, veamos cómo podemos ordenar el conjunto, en una pasada, si la llave de ordenación fuera uno solo de los dígitos, por ejemplo el tercero de izquierda a derecha (lo mostramos separado para destacarlo):

```
    99 0 46
    82 1 49
    94 1 71
    70 4 71
    66 4 96
    80 5 64
    93 7 54
    73 8 95
    04 8 53
    54 9 63
```

La forma de hacerlo es la siguiente. Llamemos $j$ a la posición del dígito mediante el cual se ordena. La ordenación se puede hacer utilizando una cola de entrada, que contiene al conjunto a ordenar, y un arreglo de 10 colas de salida, subindicadas de 0 a 9. Los elementos se van sacando de la cola de entrada y se van encolando en la cola de salida $Q[d_j]$, donde $d_j$ es el $j$-ésimo dígito del elemento que se está transfiriendo.


![bucket-pass](recursos/bucket-pass.gif)

Al terminar este proceso, los elementos están separados por dígito. Para completar la ordenación, basta concatenar las $k$ colas de salida y formar nuevamente una sola cola con todos los elementos.

Este proceso se hace en una pasada sobre los datos, y toma tiempo $\Theta(n)$.

Para ordenar el conjunto por las llaves completas, ejecutamos este proceso dígito por dígito, *de derecha a izquierda*, en cada pasada separando los elementos según el valor del dígito respectivo, luego recolectándolos para formar una sola cola, y realimentando el proceso con esos mismos datos. El conjunto completo queda finalmente ordenado (¡esto *no* es obvio!).

Como hay que realizar $k$ pasadas y cada una de ellas toma tiempo $\Theta(n)$, el tiempo total es $\Theta(kn)$, que es el tamaño total del archivo de entrada (en bytes). Por lo tanto, la ordenación toma tiempo lineal en el tamaño de los datos.

El proceso anterior se puede generalizar para cualquier alfabeto, no sólo dígitos (por ejemplo, ASCII). Esto aumenta el número de colas de salida, pero no cambia sustancialmente el tiempo que demora el programa.
---
### El tiempo es lineal, pero ¿es $\Theta(n)$?

Como $k$ es un parámetro ($k=5$ en nuestro ejemplo), es tentador decir que $\Theta(kn)=\Theta(n)$, pero en realidad no es tan simple.

Si fijamos $k$, entonces el máximo número de elementos distintos que podemos generar es $10^k$. Por lo tanto, $n\le 10^k$, es decir, $k\ge \log_{10}{n}$.

Por lo tanto, $k$ no puede ser constante, sino que tiene que crecer logarítmicamente con $n$, de modo que el algoritmo en realidad demora tiempo $\Omega(n\log{n})$.

### Archivos con records de largo variable

Si las líneas a ordenar no son todas del mismo largo, es posible alargarlas hasta completar el largo máximo, con lo cual el algoritmo anterior es aplicable. Pero si hay algunas pocas líneas desproporcionadamente largas y otras muy cortas, se puede perder mucha eficiencia.

Es posible, aunque no lo vamos a ver aquí, generalizar este algoritmo para ordenar líneas de largo variable sin necesidad de alargarlas. El resultado es que la ordenación se sigue realizando en tiempo proporcional al tamaño del archivo.
## Mergesort

Si tenemos dos arreglos que ya están ordenados, podemos mezclarlos para formar un solo arreglo ordenado en tiempo proporcional a la suma de los tamaños de los dos arreglos.

Esto se hace leyendo el primer elemento de cada arreglo, copiando hacia un arreglod de salida al menor de los dos, y avanzando al siguiente elemento en el arreglo respectivo. Cuando uno de los dos arreglos se termina, todos los elementos restantes del otro se copian hacia la salida. Este proceso se denomina "mezcla", o bien "merge", por su nombre en inglés.

Como cada elemento se copia sólo una vez, y con cada comparación se copia algún elemento, es evidente que el costo de mezclar los dos archivos es lineal.

Si bien es posible realizar el proceso de mezcla de dos arreglos contiguos *in situ*, el algoritmo es muy complicado y no resulta práctico. Por esta razón, el proceso se implementa generalmente copiando desde dos arreglos de entrada a uno de salida.

```python
def merge(a,b):
    i=0
    j=0
    while i<len(a) or j<len(b):
        if j>=len(b) or (i<len(a) and a[i]<=b[j]):
            yield a[i]
            i=i+1
        else:
            yield b[j]
            j=j+1
```


```python
a = [24,43,55,57,88,91]
b = [10,17,40,61,70,76]
print(a)
print(b)
c=[x for x in merge(a,b)]
print(c)
```


```
[24, 43, 55, 57, 88, 91]
[10, 17, 40, 61, 70, 76]
[10, 17, 24, 40, 43, 55, 57, 61, 70, 76, 88, 91]

```

Usando esta idea en forma reiterada, es posible ordenar un conjunto. Una forma de ver esto es recursivamente, de manera "*top-down*", usando "dividir para reinar".

```python
def mergesort(a):
    n=len(a)
    if n>1:    
        mergesort(a[0:n//2])
        mergesort(a[n//2:n])
        a[0:n]=[x for x in merge(a[0:n//2],a[n//2:n])]
```


```python
import numpy as np
a = np.random.random(6)
print(a)
mergesort(a)
print(a)
```


```
[0.98208828 0.87903465 0.49512148 0.9665445  0.75927717 0.20751891]
[0.20751891 0.49512148 0.75927717 0.87903465 0.9665445  0.98208828]

```

El tiempo total está dado aproximadamente por la ecuación de recurrencia

$$
T(n) = 2 T\left(\frac{n}{2}\right) + n
$$

la cual tiene solución $\Theta(n \log{n})$, de modo que el algoritmo resulta ser óptimo.

Esto mismo se puede implementar en forma no recursiva, "*bottom-up*", agrupando los elementos de a dos y mezclándolos para formar pares ordenados. Luego mezclamos pares para formar cuádruplas ordenadas, y así sucesivamente hasta mezclar las últimas dos mitades y formar el conjunto completo ordenado. Como cada "ronda" tiene costo lineal y se realizan $\log{n}$ rondas, el costo total es $\Theta(n \log{n})$.
### "*Runs*"

En el enfoque "*bottom-up*" no recursivo, en lugar de comenzar mezclando elementos individuales para formar pares, etc., podemos comenzar detectando "*runs*" (corridas), que son secuencias de elementos consecutivos lo más largas posibles que ya vengan ordenados. A partir de ahí, mezclamos "*runs*" consecutivas y lo seguimos haciendo hasta que quede solo una gran "*run*", que es el arreglo completo ordenado.
### Mergesort para ordenamiento externo

La idea de Mergesort es la base de la mayoría de los métodos de ordenamiento externo, esto es, métodos que ordenan conjuntos almacenados en archivos muy grandes, en donde no es posible copiar todo el contenido del archivo a memoria para aplicar alguno de los métodos estudiados anteriormente.

En las implementaciones prácticas de estos métodos, se utiliza el enfoque no recursivo, optimizado usando las siguientes ideas:

* No se comienza con elementos individuales para formar pares ordenados, sino que se generan archivos ordenados lo más grandes posibles. Para esto, el archivo de entrada se va leyendo por trozos a memoria y se ordena mediante Quicksort, por ejemplo.
* En lugar de mezclar sólo dos archivos se hace una mezcla múltiple (con $k$ archivos de entrada. Como en cada iteración hay $k$ candidatos a ser el siguiente elemento en salir, y siempre hay que extrar al mínimo de ellos y sustituirlo en la lista de candidatos por su sucesor, la estructura de datos apropiada para ello es un heap.
En caso que no baste con una pasada de mezcla múltiple para ordenar todo el archivo, el proceso se repite las veces que sea necesario.

Al igual que en los casos anteriores, el costo total es $\Theta(n \log{n})$.