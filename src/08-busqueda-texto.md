# 8 Búsqueda en Texto

La búsqueda de patrones en un texto es un problema muy importante en la práctica. Sus aplicaciones en computación son variadas, como por ejemplo la búsqueda de una palabra en un archivo de texto o problemas relacionados con biología computacional, en donde se requiere buscar patrones dentro de una secuencia de ADN, la cual puede ser modelada como una secuencia de caracteres (el problema es más complejo que lo descrito, puesto que se requiere buscar patrones en donde ocurren alteraciones con cierta probabilidad, esto es, la búsqueda no es exacta).

En este capítulo se considerará el problema de buscar la ocurrencia de un patrón dentro de un texto. Se utilizarán las siguientes convenciones:

* $n$ denotará el largo del texto en donde se buscará el patrón, es decir, el texto es $a_0 a_1 \ldots a_{n-1}$
* $m$ denotará el largo del patrón a buscar, es decir el patrón es $b_0 b_1 \ldots b_{m-1}$

Por ejemplo:

* Texto = "analisis de algoritmos"
* Patrón = "algo"
## Algoritmo de fuerza bruta

Se alinea la primera posición del patrón con la primera posición del texto, y se comparan los caracteres uno a uno hasta que se acabe el patrón, en cuyo caso se encontró una ocurrencia del patrón en el texto, o hasta que se encuentre una discrepancia.

![bruta1](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/bruta1.png?raw=1)

Si se detiene la búsqueda por una discrepancia, se desliza el patrón en una posición hacia la derecha y se intenta calzar el patrón nuevamente.

![bruta2](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/bruta2.png?raw=1)

El proceso se repite, siempre avanzando en una posición

![bruta3](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/bruta3.png?raw=1)

hasta que finalmente se encuentre

![bruta4](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/bruta4.png?raw=1)

o se agote el texto sin encontra el patrón.

En el peor caso este algoritmo realiza $\Theta(mn)$ comparaciones de caracteres.

Si suponemos que todos los caracteres aparecen en forma equiprobable e independiente, en el caso esperado el método de fuerza bruta funciona mucho mejor. Si el alfabeto es de tamaño $c$, entonces en cada comparación la probabilidad de que dos caracteres sean iguales es $\frac{1}{c}$ y de que sean distintos es $1-\frac{1}{c}$. A partir de cada posición, el número esperado de comparaciones que se efectúa hasta encontrar un descalce es

$$
\frac{1}{1-\frac{1}{c}}=\frac{c}{c-1}= 1+\frac{1}{c-1}
$$

Por lo tanto, en cada posición en que el patrón no está, el número esperado de comparaciones es una constante poco mayor que $1$, por lo tanto el costo total de la búsqueda es $\Theta(n)$.
## Algoritmo Knuth-Morris-Pratt (KMP)

Suponga que se está comparando el patrón y el texto en una posición dada, cuando se encuentra una discrepancia.

![kmp1](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/kmp1.png?raw=1)

Sea $x$ la parte del patrón que calza con el texto, e $y$ la correspondiente parte del texto, y suponga que el largo de $x$ es $j$. El algoritmo de fuerza bruta mueve el patrón una posición hacia la derecha, sin embargo, esto puede o no puede ser lo correcto en el sentido que los primeros $j-1$ caracteres de $x$ pueden o no pueden calzar los últimos $j-1$ caracteres de $y$.

La observación clave que realiza el algoritmo Knuth-Morris-Pratt (en adelante KMP) es que $x$ es igual a $y$, por lo que la pregunta planteada en el párrafo anterior puede ser respondida mirando solamente el patrón de búsqueda, lo cual permite precalcular la respuesta y almacenarla en una tabla.

Por lo tanto, si deslizar el patrón en una posición no funciona, se puede intentar deslizarlo en $2, 3, \ldots,$ hasta $j$ posiciones.

Se define la *función de fracaso* (*failure function*) del patrón como:

$$
f(j)=\max\{i | 0 \le i<j \wedge b_0\ldots b_{i-1} = b_{j-i}\ldots b_{j-1} \}
$$

![kmp2](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/kmp2.png?raw=1)

Intuitivamente, $f(j)$ es el largo del mayor prefijo de $x$ que además es sufijo del mismo $x$.
Por ejemplo, si el patrón es ``"aabaaa"``, entonces la función de fracaso es

$j$    | 1 | 2 | 3 | 4 | 5 | 6
------ | - | - | - | - | - | -
$f(j)$ | 0 | 1 | 0 | 1 | 2 | 2


Si se detecta una discrepancia entre el patrón y el texto cuando se trata de calzar $b_j$, se desliza el patrón de manera que $b_{f(j)-1}$ se encuentre donde $b_{j-1}$ se encontraba, y se intenta calzar nuevamente.

![kmp3](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/kmp3.png?raw=1)

En el siguiente ejemplo mostramos la ejecución de una búsqueda:

![kmp4](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/kmp4.png?raw=1)

Suponiendo que se tiene la función $f(j)$ precalculado, la implementación del algoritmo KMP es la siguiente:

```python
def kmp(a,b,f): # busca b dentro de a, retorna None (fracaso) o posición del calce
    n=len(a)
    m=len(b)
    j=0
    k=0
    while k<n and j<m:
        while j>0 and a[k]!=b[j]:
            j=f[j]
        if a[k]==b[j]:
            j=j+1
        k=k+1
    if j==m:
        return k-m # éxito
    else:
        return None # fracaso
```


```python
f=[0,0,1,0,1,2,2]
print(kmp("aaaabaabaaa","aabaaa",f))
print(kmp("aaaabaabaaabb","abbaaa",f))
```


```
5
None

```

El tiempo de ejecución de este algoritmo no es difícil de analizar, pero es necesario ser cuidadoso al hacerlo. Dado que se tienen dos ciclos anidados, se puede acotar el tiempo de ejecución como el número de veces que se ejecuta el ciclo externo (menor o igual a $n$) multiplicado por el número de veces que se ejecuta el ciclo interno (menor o igual a $m$), lo que de una cota superior a $O(mn)$, ¡que es igual a lo que demora el algoritmo de fuerza bruta!.

Sin embargo, el análisis descrito es pesimista. Observemos que el número total de veces que el ciclo interior es ejecutado es menor o igual al número de veces que se puede decrementar $j$, dado que $f(j)<j$. Pero $j$ comienza desde cero y es siempre mayor o igual que cero, por lo que dicho número es menor o igual al número de veces que $j$ es incrementado, el cual es menor que $n$. Por lo tanto, el tiempo total de ejecución es $\Theta(n)$ en el peor caso. Por otra parte, $k$ nunca es decrementado, lo que implica que el algoritmo nunca se devuelve en el texto.
### Cálculo de la función de fracaso

Queda por resolver el problema de definir la función de fracaso, $f(j)$. Esto se puede realizar inductivamente. Para empezar, $f(1)=0$ por definición. Para calcular $f(j+1)$ suponga que ya se tienen almacenados los valores de $f(1), f(2), \ldots, f(j)$. Se desea encontrar un $i$ tal que el $i$-ésimo carácter del patrón sea igual al $j$-ésimo carácter del patrón.

Para esto se debe cumplir que $i=f(j)$. Si $b_i=b_j$, entonces $f(j+1)=i+1$. En caso contrario, se reemplaza $i$ por $f(i)$ y se verifica nuevamente la condición.

![kmp5](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/kmp5.png?raw=1)

El algoritmo resultante es el siguiente (note que es similar al algoritmo KMP):

```python
def fracaso(b): # calcula y retorna función de fracaso para patrón b
    m=len(b)
    f=[0]*(m+1)
    for j in range(1,m):
        i=f[j]
        while i>0 and b[i]!=b[j]:
            i=f[i]
        if b[i]==b[j]:
            f[j+1]=i+1
        else:
            f[j+1]=0
    return f
```


```python
print(fracaso("aabaaa"))
```


```
[0, 0, 1, 0, 1, 2, 2]

```

El tiempo de ejecución para calcular la función de fracaso puede ser acotado por los incrementos y decrementos de la variable $i$, y por lo tanto es $\Theta(m)$.

Por lo tanto, el tiempo total de ejecución del algoritmo en el peor caso, sumando el preprocesamiento del patrón más la búsqueda, es $\Theta(m+n)$.
## Algoritmo de Boyer-Moore

Hasta el momento, los algoritmos de búsqueda en texto siempre comparan el patrón con el texto de izquierda a derecha. La idea del algoritmo de Boyer-Moore es comparar *de derecha a izquierda*: si hay una discrepancia en el último carácter del patrón y el carácter del texto no aparece en todo el patrón, entonces éste se puede deslizar $m$ posiciones sin realizar ninguna comparación extra. En particular, no habría sido necesario comparar los primeros $m-1$ caracteres del texto, lo cual indica que se podría realizar una búsqueda en el texto con menos de $n$ comparaciones; sin embargo, si el carácter discrepante del texto se encuentra dentro del patrón, éste podría desplazarse en un número menor de espacios.

El método descrito es la base del algoritmo Boyer-Moore, del cual se estudiarán dos variantes: Horspool y Sunday.
### Algoritmo Boyer-Moore-Hospool (BMH)

Supongamos que el último caracter del patrón de búsqueda $b$ se encuentra alineado con el caracter $a_k$ del texto.
El algoritmo BMH compara el patrón con el texto **de derecha a izquierda**, y se detiene cuando se encuentra una discrepancia con el texto. Cuando esto sucede, se desliza el patrón de manera que la letra $c=a_k$ del texto que estaba alineada con la letra final del patrón, ahora quede alineada con un caracter anterior de $b$ con el cual coincida, si dicho calce es posible, o si no, con $b_{-1}$, un carácter ficticio a la izquierda de $b_0$ (este es el mejor caso del algoritmo).

Para determinar el desplazamiento del patrón se define la función $g(c)$ como:

* $g(c)=i$ si $i$ es el mayor subíndice en el rango $0\le i \le m-2$ tal que $b_i=c$. Nótese que si hay más de una ocurrencia de $c$, se toma la de más a la derecha.

![bmh1](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/bmh1.png?raw=1)

* $g(c)=-1$ si $c$ no aparece entre los primeros $m-1$ caracteres del patrón.

![bmh2](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/bmh2.png?raw=1)

En ambos casos se busca el caracter $c$ solo dentro de los primeros $m-1$ caracteres del patrón, excluyendo el último, para que el deslizamiento del patrón sea de al menos una posición.

Esta función sólo depende del patrón y se puede precalcular antes de realizar la búsqueda.
#### Ejemplo de Boyer-Moore-Horspool

Supongamos que queremos buscar el patrón ``"datos"`` dentro de ``"estructuras de datos"``. La función $g(c)$ estaría dada por

$c$    | "a" | "d" | "o" | "t"
------ | --- | --- | --- | ---
$g(c)$ |  1  |  0  |  3  |  2

y $g(c)=-1$ para toda otra letra $c$.

El siguiente diagrama muestra el proceso de búsqueda:

![bmh3](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/bmh3.png?raw=1)
Por simplicidad de programación, para implementar el algoritmo usaremos un diccionario de Python para la función $g$. En una implementación eficiente, esta función se impelemntaría como un arreglo subindicado por la representación numérica de cada letra.

```python
def construyeg(b): # construye un diccionario para representar la función g
    d={}
    for i in range(0,len(b)-1): # ignoramos el último caracter
        d[b[i]]=i
    return d
```


```python
def bmh(a,b): # busca b dentro de a, retorna None (fracaso) o posición del calce
    g=construyeg(b) # Uso: g(c)=g.get(c,-1) para rellenar con -1 los valores faltantes
    n=len(a)
    m=len(b)
    k=m-1
    j=m-1
    while k<n:
        if j<0:
            return k-m+1
        if a[k-(m-1-j)]==b[j]:
            j=j-1
        else:
            k=k+(m-1-g.get(a[k],-1))
            j=m-1
    return None
```


```python
print(bmh("estructuras de datos","datos"))
print(bmh("estructuras de datos","struct"))
print(bmh("estructuras de datos","gatos"))
```


```
15
1
None

```

Se puede demostrar que si el alfabeto tiene tamaño $L$ y los caracteres aparecen con probabilidad uniforme y de manera independiente, entonces el tiempo promedio que demora BMH es

$$
\Theta\left( n \left( \frac{1}{m}+\frac{1}{2L} \right) \right)
$$

Para un alfabeto razonablemente grande, esto es aproximadamente $\Theta\left( \frac{n}{m} \right)$.
### Algoritmo Boyer-Moore-Sunday (BMS)

El algoritmo BMH desliza el patrón basado en el símbolo del texto que corresponde a la posición del último carácter del patrón. Este siempre se desliza al menos una posición si se encuentra una discrepancia con el texto.

Es fácil ver que si se utiliza el carácter una posición más adelante en el texto como entrada de la función siguiente el algoritmo también funciona, pero en este caso es necesario considerar el patrón completo al momento de calcular los valores de la función siguiente. Esta variante del algoritmo es conocida como Boyer-Moore-Sunday (BMS).

Caso en que $c=a_{k+1}$ aparece dentro del patrón:

![bms1](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/bms1.png?raw=1)

Caso en que $c=a_{k+1}$ no aparece dentro del patrón:

![bms2](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/bms2.png?raw=1)

#### Ejemplo de Boyer-Moore-Sunday

Supongamos que queremos buscar el patrón ``"datos"`` dentro de ``"estructuras de datos"``. La función $g(c)$ estaría dada por

$c$    | "a" | "d" | "o" | "s" | "t"
------ | --- | --- | --- | --- | ---
$g(c)$ |  1  |  0  |  3  |  4  |  2

y $g(c)=-1$ para toda otra letra $c$.

El siguiente diagrama muestra el proceso de búsqueda:

![bms3](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/bms3.png?raw=1)

```python
def construyeg(b): # construye un diccionario para representar la función g
    d={}
    for i in range(0,len(b)): # utilizamos hasta el último caracter
        d[b[i]]=i
    return d
```


```python
def bms(a,b): # busca b dentro de a, retorna None (fracaso) o posición del calce
    g=construyeg(b) # Uso: g(c)=g.get(c,-1) para rellenar con -1 los valores faltantes
    n=len(a)
    m=len(b)
    k=m-1
    j=m-1
    while k<n:
        if j<0:
            return k-m+1
        if a[k-(m-1-j)]==b[j]:
            j=j-1
        else:
            if k>=n-1:
                break
            k=k+(m-g.get(a[k+1],-1))
            j=m-1
    return None
```


```python
print(bms("estructuras de datos","datos"))
print(bms("estructuras de datos","struct"))
print(bms("estructuras de datos","gatos"))
```


```
15
1
None

```
