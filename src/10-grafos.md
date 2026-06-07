# 10 Grafos

Un *grafo* es una estructura matemática que se utiliza para representar relaciones como las que hay entre las ciudades conectadas por caminos, los cursos con sus requisitos, las componentes conectadas en un circuito eléctrico, las páginas web vinculadas por enlaces, etc.
## Definiciones básicas

Un grafo consiste de un conjunto $V$ de *vértices* (también llamados *nodos*) y un conjunto $E$ de *arcos*. El número de vértices se suele denotar $n$ y el número de arcos como $m$ (o a veces $e$).

Se dice que un grafo es *no dirigido* si sus arcos no tiene una dirección asociada. Por ejemplo,

![grafo-no-dirigido](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/grafo-no-dirigido.png?raw=1)

$$
\begin{align}
V &=\{v_1,v_2,v_3,v_4,v_5\}\\
E &=\{ \{v_1,v_2\},\{v_1,v_3\},\{v_1,v_5\},\{v_2,v_3\},\{v_3,v_4\},\{v_4,v_5\} \}
\end{align}
$$

Un grafo es *dirigido* si sus arcos tienen una orientación. Por ejemplo:

![grafo-dirigido](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/grafo-dirigido.png?raw=1)

$$
\begin{align}
V &=\{v_1,v_2,v_3,v_4\}\\
E &=\{ (v_1,v_2), (v_2,v_2), (v_2,v_3), (v_3,v_1), (v_3,v_4), (v_4,v_3) \}
\end{align}
$$

Adicionalmente, los grafos pueden tener rótulos asociados a sus vértices o arcos. Estos rótulos pueden representar costos, longitudes, pesos, etc.
## Representaciones de grafos en memoria

Un grafo se puede almacenar en memoria de distintas maneras, las cuales tienen distintos requerimientos de espacio, y ponen también distintas restricciones al tiempo de proceso.

### Matriz de adyacencia

Un grafo se puede representar a través de una matriz $A$ donde $A[i,j]=1$ si hay un arco que conecta $v_i$ con $v_j$, y $0$ si no.
La matriz de adyacencia de un grafo no dirigido es simétrica.

Una matriz de adyacencia permite determinar si dos vértices están conectados o no en tiempo constante, pero requieren $\Theta(n^2)$ bits de memoria. Esto puede ser demasiado para muchos grafos que aparecen en aplicaciones reales, en donde $m<<n^2$. Otro problema es que se requiere tiempo $\Theta(n)$ para encontrar la lista de vecinos de un vértice dado.

### Listas de adyacencia

Esta representación consiste en almacenar, para cada nodo, la lista de los nodos adyacentes a él (sus "vecinos"). Para el segundo ejemplo anterior, tenemos:

$$
\begin{align}
\text{vecinos}[v_1] &= [v_2]\\
\text{vecinos}[v_2] &= [v_2, v_3]\\
\text{vecinos}[v_3] &= [v_1, v_4]\\
\text{vecinos}[v_4] &= [v_3]
\end{align}
$$

Esto utiliza espacio $\Theta(m)$ y permite acceso eficiente a los vecinos, pero no permite acceso directo a los arcos.

## Caminos, ciclos y árboles

Consideremos un grafo no dirigido.

Un *camino* es una secuencia de arcos en que el extremo final de cada arco coincide con el extremo inicial del siguiente en la secuencia. Por ejemplo, los arcos gruesos forman un camino desde $v_2$ a $v_5$ (o viceversa):

![camino](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/camino.png?raw=1)

Un camino es *simple* si no se repiten vértices, excepto posiblemente el primero y el último.

Un *ciclo* es un camino simple y cerrado (esto es, en que el vértice inicial y final son el mismo). En el siguiente ejemplo los arcos gruesos forman un ciclo:

![ciclo](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/ciclo.png?raw=1)

Un grafo que no tiene ciclos se dice que es *acíclico*.

Se dice que un grafo es *conexo* si para todo par de vértices del grafo existe un camino que los une. Si un grafo no es conexo, entonces estará compuesto por varias "islas", cada una de las cuales se llama una *componente conexa*. Más precisamentem una componente conexa es un subgrafo conexo *maximal* (esto es, que no está estrictamente contenido dentro de un subgrafo conexo mayor).

Un *árbol* es un grafo que es *conexo* y *acíclico*. En el siguiente ejemplo, los arcos gruesos forman un árbol:

![arbol](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/arbol.png?raw=1)

Si un árbol incluye todos los nodos de un grafo, se dice que es un *árbol cobertor* (*spanning tree*).

### Propiedades de los árboles

Es fácil demostrar las siguientes propiedades:

* Todo árbol con $n$ nodos tiene $n-1$ arcos.
* Si se agrega un arco a un árbol, se crea un único ciclo.
## Recorridos de grafos

En muchas aplicaciones es necesario visitar todos los vértices del grafo a partir de un nodo dado. Algunas aplicaciones son:

* Encontrar ciclos
* Encontrar componentes conexas
* Encontrar árboles cobertores

Hay dos enfoque básicos:

*Recorrido (o búsqueda) en profundidad (depth-first search)*:

La idea es alejarse lo más posible del nodo inicial (sin repetir nodos), luego devolverse un paso e intentar lo mismo por otro camino.

*Recorrido (o búsqueda) en amplitud (breadth-first search)*:

Se visita a todos los vecinos directos del nodo inicial, luego a los vecinos de los vecinos, etc.
### Recorrido en profundidad (DFS)

A medida que recorremos el grafo, iremos numerando correlativamente los nodos encontrados $1,2,\ldots$. Suponemos que todos estos números son cero inicialmente, y para ir asignando esta numeración utilizamos un contador global $n$, también inicializado en cero. A esta numeración asignada la llamamos el Depth-First-Number (DFN).

El siguiente algoritmo en seudo-código muestra cómo se puede hacer este tipo de recorrido recursivamente:

```python
# seudo-código
def DFS(v): # Recorre en profundidad a partir del vértice v    
    global n
    global DFN
    assert DFN[v]==0 # Supone que es primera vez que se visita el vértice v
    n=n+1
    DFN[v]=n # Numeramos el vértice v
    for w in vecinos[v]:
        if DFN[w]==0:
            DFS(w)  # Visitamos w si no había sido visitado aún
```

Para dar el "puntapié inicial" al proceso, hay que hacer que todos los DFN estén en cero, inicializar en cero la variable global $n$ e indicar el nodo de partida $x$:

```python
# seudo-código
def startDFS(x):
    global n
    global DFN
    n=0
    for v in V:
        DFN[v]=0
    DFS(x)
```

En el siguiente ejemplo mostraremos un posible resultado de aplicar este recorrido a un grafo dado. A la derecha se muestra el mismo grafo, con sus vértices numerados con DFN y marcando más grueso al arco que permitió llegar a por primera vez a cada vértice. A estos arcos los llamamos *arcos de árbol*. A los arcos que permiten llegar a un vértice que ya había sido visitado los llamamos *arcos de retorno* y los mostramos con línea segmentada.

![DFS](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/DFS.png?raw=1)

Si hubiera más de una componente conexa, este recorrido no llegaría a todos los nodos. Para recorrer el grafo por completo, podemos ejecutar un DFS sobre cada componente conexa.

```python
# seudo-código
def startDFS(): # recorre el grafo, retorna número de componentes conexas
    global n
    global ncc
    global DFN
    n=0
    for v in V:
        DFN[v]=0
    ncc=0 # cuenta el número de componentes conexas
    for x in V:
        if DFN[x]==0:
            ncc=ncc+1
            DFS(x)
    return ncc
```

Existe una gran similitud entre el DFS y el recorrido en preorden que vimos para árboles binarios. Tal como ocurrió en esa oportunidad, también es posible programar el recorrido de manera no recursiva utilzando una pila:

```python
# seudo-código
def DFSnorecursivo(x): # Recorre en profundidad a partir del vértice x  
    n=0
    for v in V:
        DFN[v]=0
    s=Pila()
    s.push(x) # el vértice inicial del recorrido
    while not s.is_empty():
        v=s.pop()
        if DFN[v]==0: # primera vez que se visita este nodo
            n=n+1
            DFN[v]=n      
            for w in vecinos[v]:
                s.push(w)
```

### Recorrido en amplitud

Este recorrido es análogo al recorrido por niveles que vimos para árboles binarios. Su programación es similar a ``DFSnorecursivo``, sustituyendo la pila por una cola.
## Árbol Cobertor Mínimo (*Minimum Spanning Tree*)

Para un grafo dado pueden existir muchos árboles cobertores. Si introducimos un concepto de "peso" (o "costo") sobre los arcos, es interesante tratar de encontrar un árbol cobertor que tenga costo mínimo. El costo de un árbol es la suma de los costos de sus arcos.

En esta sección veremos dos algoritmos para encontrar un árbol cobertor mínimo para un grafo no dirigido dado, conexo y con costos asociados a los arcos.
### Algoritmo de Kruskal

Este es un algoritmo del tipo "avaro" ("greedy"). Comienza inicialmente con un grafo que contiene sólo los nodos del grafo original, sin arcos. Luego, en cada iteración, se agrega al grafo el arco más barato que no genere un ciclo. El proceso termina cuando el grafo está completamente conectado.

En general, la estrategia "avara" no garantiza que se encuentre un óptimo global, porque es un método "miope", que sólo optimiza las decisiones de corto plazo. Por otra parte, a menudo este tipo de métodos proveen buenas heurísticas, que se acercan al óptimo global. Pero en este caso, afortunadamente, se puede demostrar que el método "avaro" logra siempre encontrar el óptimo global, por lo cual un árbol cobertor encontrado por esta vía está garantizado que es un árbol cobertor mínimo.

Una forma de ver este algoritmo es diciendo que al principio cada nodo constituye su propia componente conexa, aislado de todos los demás nodos. Durante el proceso de construcción del árbol, se agrega un arco sólo si sus dos extremos se encuentran en componentes conexas distintas, y luego de agregarlo, esas dos componentes conexas se fusionan en una sola.

La siguiente animación muestra el algoritmo de Kruskal en funcionamiento. A cada paso, se intenta agregar un arco. Si se descarta, porque formaría un ciclo, se marca con una "X" y se pasa al siguiente. Si se acepta, porque une dos componentes conexas distintas, se marca como un arco sólido.

![kruskal](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/kruskal.gif?raw=1)

Para la operatoria con componentes conexas supondremos que cada componente conexa se identifica mediante un representante canónico (el "lider" del conjunto), y que se dispone de las siguientes operaciones:

``Union(a,b)``: Se fusionan las componentes canónicas representadas por a y b, respectivamente.

``Find(x)``: Encuentra al representante canónico de la componente conexa a la cual pertenece x.

Con estas operaciones, el algoritmo de Kruskal se puede escribir así (en seudo-código):

```python
# seudo-código
def kruskal(V,E):
    sort(E) # Ordenar los arcos en orden creciente de costo
    C = [[v] for v in V] # C es el conjunto de componentes conexas, inicialmente "singletons"
    T = [] # La lista de los arcos del árbol
    for e in E: # consideramos los arcos en orden creciente
        if len(C)==1: # queda solo 1 componente conexa
            break
        (v,w)=vertices(e)      # los dos extremos del arco e
        if Find(v) != Find(w): # están en componentes conexas distintas
            T.append(e) # Agregar el arco e al árbol
            Union(Find(v),Find(w)) # Fusionamos las dos componentes en una sola
    return T
```

El tiempo que demora este algoritmo está dominado por lo que demora la ordenación del conjunto $E$ de arcos, $\Theta(m \log{m})$, más lo que demora realizar $m$ operaciones ``Find``, más $n$ operaciones ``Union``.

Es posible implementar ``Union-Find`` de modo que las operaciones ``Union`` demoren tiempo constante, y las operaciones ``Find`` un tiempo casi constante. Más precisamente, el costo amortizado de un Find está acotado por $\log^*{n}$, donde $\log^*{n}$ es una función definida como el número de veces que es necesario tomar el logaritmo de un número para que el resultado sea menor que 1.

Por lo tanto, el costo total es $\Theta(m \log{m})$, lo cual es igual a $\Theta(m \log{n})$, porque en todo grafo se tiene que $m=O(n^2)$.
La correctitud del algoritmo de Kruskal viene del siguiente lema:

#### Lema

Sea $V'$ subconjunto propio de $V$, y sea $e=\{v,w\}$ un arco de costo mínimo tal que $v \in V'$ y $w \in V-V'$. Entonces existe un árbol cobertor mínimo que incluye a $e$.

Este lema permite muchas estrategias distintas para escoger los arcos del árbol. Un ejemplo es el siguiente algoritmo.

### Algoritmo de Prim

Comenzamos con el arco más barato, y marcamos sus dos extremos como "alcanzables". Luego, a cada paso, intentamos extender nuestro conjunto de nodos alcanzables agregando siempre el arco más barato que tenga uno de sus extremos dentro del conjunto alcanzable y el otro fuera de él. De esta manera, el conjunto alcanzable se va extendiendo como una "mancha de aceite".

```python
# seudo-código
def prim(V,E):
    e=arco_de_costo_minimo(E)
    (v,w)=vertices(e)
    T=[e]   # árbol
    A=[v,w] # conjunto alcanzable
    while A!=V:
        e=arco_de_costo_minimo_que_conecta(A,V-A)
        (v,w)=vertices(e) # suponemos v en A y w en V-A
        T.append(e)
        A.append(w)
```

La siguiente animación muestra el algoritmo de Prim en funcionamiento. A cada paso, los arcos candidatos a agregarse se muestran con líneas punteadas. El arco que se acepta, por ser el de menor costo que une al conjunto alcanzable con el resto del grafo se marca como un arco sólido.

![prim](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/prim.gif?raw=1)

Para implementar este algoritmo eficientemente, podemos mantener una tabla donde, para cada nodo de $V-A$, almacenamos el costo del arco más barato que lo conecta al conjunto A. Estos costos pueden cambiar en cada iteración, así que hay que recalcularlos para todos los vecinos del nodo que se agrega al conjunto alcanzable.

Si se organiza la tabla como una cola de prioridad, el tiempo total es $\Theta(m \log{n})$. Si se deja la tabla desordenada y se busca linealmente en cada iteración, el costo es $\Theta(n^2)$. Esto último es mejor que lo anterior cuando el grafo es denso.
## Distancias mínimas en un grafo dirigido

Consideremos un grafo *dirigido* $G=(V,E)$, donde para cada arco $e=(u,v)$ se conoce su largo, o distancia, $d(e)=d(u,v)\ge 0$. Podemos extender la función $d$ a todo $V\times V$ si definimos $d(u,v)=\infty$ cuando $(u,v)\notin E$.

Si se define el largo de un camino como la suma de los largos de los arcos que lo componen, es interesante encontrar los caminos más cortos que unen a nodos del grafo.

Este problema se suele estudiar en dos variantes:

* Encontrar todos los caminos más cortos desde un nodo "origen" $s$ hasta todos los demás nodos del grafo.

* Encontrar todos los caminos más cortos entre todos los pares de nodos del grafo. Esto se puede resolver iterando $n$ veces el problema anterior, cambiando cada vez el nodo origen, pero es posible encontrar un algoritmo más simple si se resuelve todo de una vez.
### Algoritmo de Dijkstra para los caminos más cortos desde un nodo origen

La idea del algoritmo es mantener un conjunto $A$ de nodos "alcanzables" desde el nodo origen e ir extendiendo este conjunto en cada iteración.

Los nodos alcanzables son aquellos para los cuales ya se ha encontrado su camino óptimo desde el nodo origen. Para esos nodos su distancia óptima al origen es conocida. Inicialmente $A=\{s\}$.

Para los nodos que todavía no están en $A$ aún no se conoce su camino óptimo desde $s$, pero sí se puede conocer el camino óptimo *que pasa sólo por nodos de* $A$. Esto es, caminos en que todos los nodos intermedios son nodos de $A$. Llamemos a esto su camino óptimo *tentativo*.

En cada iteración, el algoritmo encuentra el nodo que no está en $A$ cuyo camino óptimo tentativo tiene largo mínimo. Es fácil demostrar por contradicción que ese camino tiene que ser el camino óptimo para ese nodo. Luego, ese nodo se agrega a $A$ y su camino óptimo tentativo se convierte en su camino óptimo. Luego se actualizan los caminos óptimos tentativos para los demás nodos.

```python
# seudo-código
def Dijkstra(V,E,d,s):
    A=[s]
    for v in V:
        D[v]=d(s,v)
    D[s]=0
    # D[] almacena las distancias óptimas desde s para los nodos en A
    # y las distancias óptimas tentativas para los nodos en V-A
    while A!=V:
        # Encontramos el nodo v de menor distancia óptima tentativa
        v = findmin(D[u] for u in V-A)
        # Agregamos v al conjunto alcanzable
        A.append(v)
        # recalculamos las distancias óptimas tentativas
        # considerando la posibilidad de pasar por el nuevo nodo v
        for w in vecinos[v]: # los nodos w tal que (v,w) in E
            D[w] = min(D[w],D[v]+d(v,w))
    # Al terminar, D[] almacena las distancias óptimas definitivas
    return D
```

Si $D$ se implementa como un arreglo en donde el mínimo se busca secuencialmente, encontrar el mínimo toma tiempo $\Theta(n)$, con un aporte de $\Theta(n^2)$ al tiempo total. Por otra parte, recalcular las distancias óptimas tentativas toma en total tiempo $\Theta(m)$, porque cada arco se usa a lo más una vez. Como $m=O(n^2)$, el tiempo total es $\Theta(n^2)$.

Una forma alternativa de implementar este algoritmo es usando una *cola de prioridad*, por ejemplo un heap, para almacenar los valores de $D$ de los nodos en $V-A$. Así, encontrar y extraer el mínimo toma tiempo $\Theta(\log{n})$, lo cual se ejecuta $n$ veces, y cada recálculo toma también tiempo $\Theta(\log{n})$, porque hay que cambiar la prioridad del respectivo elemento en el heap, y esto se ejecuta $m$ veces. Por lo tanto, en esta implementación el tiempo total es $\Theta(m\log{n})$.
### Algoritmo de Floyd para todas las distancias más cortas

Para aplicar este algoritmo, los nodos se numeran arbitrariamente $1,2,\ldots,n$. El algoritmo va a construir una matriz $D$ tal que, al final, $D[i,j]$ va a ser el largo del camino más corto que va desde el nodo $i$ hasta el nodo $j$.

El invariante del algoritmo es que al comenzar la iteración $k$-ésima, $D[i,j]$ es la distancia mínima entre $i$ y $j$ medida a través de caminos *que pasen sólo por nodos intermedios de numeración* $<k$.

En la iteración $k$-ésima se comparan estas distancias óptimas con las que se obtendrían si se pasara una vez por el nodo $k$. Si de esta manera se obtendría un camino más corto, entonces se prefiere este nuevo camino, de lo contrario nos quedamos con el camino antiguo.

![floyd](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/floyd.gif?raw=1)

Al terminar esta iteración, las distancias calculadas ahora incluyen la posibilidad de pasar por nodos intermedios de numeración $\le k$, con lo cual estamos listos para ir a la iteración siguiente.

Inicialmente, hacemos $D[i,j]=d(i,j)$ para todo $i,j$ (recordemos la convención de que $d(i,j)=\infty$ si $(i,j)\notin E$), excepto que la diagonal es $D[i,i]=0$, porque la distancia óptima de todo nodo a sí mismo es $0$.

```python
# seudo-código
def Floyd(V,E,d):
    for i in range(1,n+1):
        for j in range(1,n+1):
            D[i,j]=d(i,j)
        D[i,i]=0
    
    for k in range(1,n+1):
        for i in range(1,n+1):
            for j in range(1,n+1):
                D[i,j]=min(D[i,j],D[i,k]+D[k,j])
    
    return D
```

El tiempo total que demora este algoritmo claramente es $\Theta(n^3)$.
## Algoritmo de Warshall para cerradura transitiva y reflexiva de un grafo dirigido

Dado un grafo dirigido $G=(V,E)$, su *cerradura transitiva y reflexiva* es un grafo $G^*=(V,E^*)$, donde hay un arco $(u,v)\in E^*$ ssi existe un camino desde $u$ hasta $v$ en $G$. Si se consideran solo caminos de largo $\ge 1$, el grafo se llama la cerradura transitiva de $G$ y se denota por $G^+$. La diferencia entre $G^+$ y $G^*$ es que para construir $G^+$ se agregan todos los arcos de transitividad, y para $G^*$ se agregan además todos los auto-ciclos.

El siguiente ejemplo muestra un grafo dirigido $G$ y su correspondiente cerradura transitiva y reflexiva $G^*$, mostrando en línea punteada los arcos que se agregan.

![warshall](https://github.com/ivansipiran/CC3001-Apuntes/blob/main/recursos/warshall.png?raw=1)

Supongamos que el grafo $G$ se representa a través de su matriz de adyacencia $A$, con $A[i,j]=1$ si hay un arco entre $v_i$ y $v_j$, y $0$ si no. Queremos calcular la matriz $A^*$ correspondiente al grafo $G^*$. Para el grafo del ejemplo, tendríamos

$$
A=
\begin{bmatrix}
0 & 1 & 0 & 0 \\
0 & 1 & 0 & 1 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0
\end{bmatrix}
~~~~~~
A^*=
\begin{bmatrix}
1 & 1 & 1 & 1 \\
0 & 1 & 1 & 1 \\
0 & 1 & 1 & 1 \\
0 & 1 & 1 & 1
\end{bmatrix}
$$

Podemos resolver este problema haciendo uso del algoritmo de Floyd, de la siguiente manera: formamos una matriz de distancias $D$, con

$$
D[i,j] =
\begin{cases}
+\infty & \text{if }A[i,j]=0 \\
0 & \text{if }A[i,j]=1
\end{cases}
$$

Luego de aplicar el algoritmo de Floyd, tendremos que la distancia entre dos nodos es $0$ ssi existe un camino entre los dos nodos, así que podemos recuperar la matriz $A^*$ haciendo la sustitución inversa.

Yendo más allá, podemos re-examinar el funcionamiento del algoritmo de Floyd sobre esos infinitos y ceros, y ver cuál sería su interpretación si estuvieran operando sobre los ceros y unos originales, respectivamente.

El algoritmo de Floyd hace uso de dos operaciones, $+$, y $\min$. Las dos tablas siguientes muestran el efecto de esas operaciones:

| $+$      | $\infty$ | $0$      |
|----------|----------|----------|
| $\infty$ | $\infty$ | $\infty$ |
| $0$      | $\infty$ | $0$      |

| $\min$   | $\infty$ | $0$      |
|----------|----------|----------|
| $\infty$ | $\infty$ | $0$      |
| $0$      | $0$      | $0$      |

Si reemplazamos $\infty$ por $0$ y $0$ por $1$, respectivamente, vemos que las tablas resultantes corresponden a las operaciones lógicas $\wedge$ y $\vee$:

| $\wedge$ | $0$      | $1$      |
|----------|----------|----------|
| $0$      | $0$      | $0$      |
| $1$      | $0$      | $1$      |

| $\vee$   | $0$      | $1$      |
|----------|----------|----------|
| $0$      | $0$      | $1$      |
| $1$      | $1$      | $1$      |

Si reescribimos el algoritmo de Floyd en términos de ceros y unos, con estas operaciones lógicas, obtenermos el algoritmo de Warshall:

```python
# seudo-código
def Warshall(V,E,d):
    for i in range(1,n+1):
        for j in range(1,n+1):
            A[i,j]=1 if (i,j) in E else 0
        A[i,i]=1
    
    for k in range(1,n+1):
        for i in range(1,n+1):
            for j in range(1,n+1):
                A[i,j]=A[i,j] or (A[i,k] and A[k,j])
    
    return A
```

Tal como en el caso del algoritmo de Floyd, el algoritmo de Warshall obviamente demora tiempo $\Theta(n^3)$.