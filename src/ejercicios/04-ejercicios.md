### Ejercicio 4.1

Demostrar que $T(n) = \lceil \log_2{(n+1)} \rceil$, en el caso de la búsqueda binaria.
### Ejercicio 4.2

Cuando los datos que se encuentran en un arreglo son de tipo real (float) se puede implementar una búsqueda basada en interpolación que, en promedio, tiene mejor comportamiento que la búsqueda binaria. La idea es que en un arreglo de números reales ordenados se revise cuál es el valor del menor y del mayor y suponiendo que los datos están uniformemente distribuidos en el arreglo, se calcula por interpolación el lugar más probable donde se pueda encontrar el elemento buscado. Para simplificar, vamos a suponer que todos los elementos del arreglo son distintos.

Para un segmento de un arreglo desde $a[i]$ hasta $a[j]$, queremos escribir la fórmula en términos de $a[i]$, $a[j]$, $i$, $j$ y $x$ (número buscado) que nos da $k$, que es el lugar donde queremos examinar a continuación, usando la proporción

$$
\frac{x-a[i]}{a[j]-a[i]}=\frac{k-i}{j-i}
$$ 

de donde podemos despejar

$$
k = i+\frac{x-a[i]}{a[j]-a[i]}(j-i)
$$

Como $k$ debe ser entero, la fórmula de la derecha debería redondearse, por ejemplo al entero inmediatamente inferior, para lo cual se puede usar la función `int` de python.

_Nota_: A diferencia de la búsqueda binaria, en que está garantizado que $k$ está entre $i$ y $j$, esta fórmula podría dar valores fuera de ese rango. Esa sería una condición adicional que habría que chequear, y si se da ese caso, la búsqueda sería infructuosa.

Con estas consideraciones, modifique la versión que viene a continuación para implementar la búsqueda por interpolación, y luego ejecute los casos de prueba. Observe que para evitar una división por cero en el caso $i=j$, es preferible que el ciclo `while` itere solo mientras $i<j$, y a la salida revisar si se detuvo porque $i$ era igual a $j$.

```python
# Búsqueda por interpolación
# busca x en el arreglo a, retorna subíndice o -1 si no está
def binterp(x,a):
  # El código que viene a continuación es el de la búsqueda binaria.
  # Usted debe modificarlo para que implemente la búsqueda por interpolación
    n=len(a)
    i=0
    j=n-1
    while i<=j:
        k=(i+j)//2
        if x==a[k]:
            return k
        if x<a[k]:
            j=k-1
        else:
            i=k+1
    return -1
```


```python
# Casos de prueba
a = [2.3, 5.4, 7.1, 15.3, 27.4, 28.3, 30.0, 37.8, 45.6]
assert binterp(28.3,a)== 5
print("OK")
assert binterp(2.3,a) == 0
print("OK")
assert binterp(16,a) == -1
print("OK")
```

### Ejercicio 4.3
Escriba una función que pueda ser invocada como ``L.reversar()``, que al ejecutarse re-enlace los nodos de la lista de modo que queden en el orden opuesto al original, en tiempo lineal en el largo de la lista. Esto debe hacerse solo modificando punteros, sin crear nuevos nodos. Escriba a continuación la definición de la clase ``Lista`` incluyendo la función ``reversar``.

```python
!pip install aed_utilities

import aed_utilities as aed

class Nodo:
    def __init__(self, info, sgte=None):
        self.info=info
        self.sgte=sgte
        
class Lista:
    def __init__(self):
        self.primero=None
        
    def insertar_al_inicio(self,info):
        self.primero=Nodo(info,self.primero)
    
    def insertar_despues_de(self,p,info): # inserta después de nodo p
        p.sgte=Nodo(info,p.sgte)
    
    def eliminar_al_inicio(self):
        assert self.primero is not None
        self.primero=self.primero.sgte
    
    def eliminar_sgte_de(self,p): # elimina el nodo siguiente de p
        assert p.sgte is not None
        p.sgte=p.sgte.sgte
    
    def k_esimo(self,k): # retorna k-esimo nodo, o None si fuera de rango
        p=self.primero
        j=1
        while p is not None:
            if j==k:
                return p
            p=p.sgte
            j+=1
        return None
    
    def imprimir(self):
        p=self.primero
        while p is not None:
            print(p.info, end=" ")
            p=p.sgte
        print()
    
    def reversar(self):
        #Escribir código aquí

    def dibujar(self):
      lld = aed.LinkedListDrawer(fieldHeader="primero", fieldData="info", fieldLink="sgte", strHeader="primero")
      lld.draw_linked_list(self)
```

Probar su función con los siguientes casos:

```python
# Lista de varios elementos
L=Lista()
L.insertar_al_inicio(44)
L.insertar_al_inicio(13)
L.insertar_al_inicio(65)
L.insertar_al_inicio(42)
L.dibujar()
L.reversar()
L.dibujar()
```


```python
# Lista vacía
L1 = Lista()
L1.dibujar()
L1.reversar()
L1.dibujar()
```


```python
# Lista con un único elemento
L2 = Lista()
L2.insertar_al_inicio(12)
L2.dibujar()
L2.reversar()
L2.dibujar()
```

### Ejercicio 4.4

Suponga que por un accidente, o quizás por vandalismo, todos los punteros ``prev`` de una lista de doble enlace han sido destruidos. Afortunadamente, los punteros ``sgte`` están intactos. Usted debe escribir primero una función que pueda invocarse como ``L.destruye_prev()`` que remueva todos los punteros ``prev`` de los nodos. Para lograr esto hay que hacer que todos los punteros ``prev`` apunten a la cabecera. A continuación, debe escribir una función que pueda invocarse como ``L.repara_prev`` que reconstruya los punteros faltantes. A continuación se encuentra la definición de la clase ``Lista_doble_enlace`` incluyendo las cabeceras de las funciones ``destruye_prev`` y ``repara_prev`` que usted debe completar. También se entrega un caso de prueba para probar que sus funciones son correctas.

```python
!pip install aed_utilities

import aed_utilities as aed

class Nodo:
    def __init__(self, prev, info, sgte):
        self.prev=prev
        self.info=info
        self.sgte=sgte

class Lista_doble_enlace:
    def __init__(self):
        self.cabecera=Nodo(None,0,None)
        self.cabecera.prev=self.cabecera
        self.cabecera.sgte=self.cabecera
    
    def insertar_despues_de(self,p,info): # inserta después de nodo p
        r=p.sgte
        p.sgte=r.prev=Nodo(p,info,r)
 
    def eliminar(self,p): # elimina el nodo p
        assert p is not self.cabecera
        (p.prev.sgte,p.sgte.prev)=(p.sgte,p.prev)
    
    def k_esimo(self,k): # retorna k-esimo nodo, o None si fuera de rango
        p=self.cabecera
        j=0
        while True:
            if j==k:
                return p
            p=p.sgte
            if p is self.cabecera:
                return None
            j+=1
    
    def ascendente(self):
        p=self.cabecera.sgte
        while p is not self.cabecera:
            yield p.info
            p=p.sgte

    def descendente(self):
        p=self.cabecera.prev
        while p is not self.cabecera:
            yield p.info
            p=p.prev
    
    def destruye_prev(self):
        #Define aqui la función para destruir todos los enlaces "prev"
            
    def repara_prev(self):
        #Define aquí la función para reparar los enlaces "prev"

    def dibujar(self):
      lld=aed.LinkedListDrawer(fieldHeader="cabecera", fieldData="info", fieldLink="sgte", fieldReverseLink="prev")
      lld.draw_double_linked_list(self)
```

Pruébela a continuación:

```python
L=Lista_doble_enlace()
L.insertar_despues_de(L.k_esimo(0),42)
L.insertar_despues_de(L.k_esimo(1),65)
L.insertar_despues_de(L.k_esimo(2),13)
L.insertar_despues_de(L.k_esimo(3),44)
L.dibujar() #Muestra la lista doblemente enlazada original

L.destruye_prev()
L.dibujar() #Muestra la lista como si fuera una lista enlazada simple (sin enlaces "prev")

L.repara_prev()
L.dibujar() #Muestra la lista con los enlaces "prev" reparados
```

### Ejercicio 4.5

Suponga que los campos ``info`` de los nodos externos de un árbol contienen solo números y escriba una función que pueda invocarse como ``formula.evaluar()``, que al ser ejecutada entregue el valor numérico  de la fórmula representada por el árbol. Modifique a continuación la definición de las clases ``Arbol``, ``Nodoi`` y ``Nodoe`` para que incluyan la nueva función ``evaluar()``. Note que tiene que implementar la función ``evaluar()`` en las tres clases.

```python
class Nodoi:
    def __init__(self, izq, info, der):
        self.izq=izq
        self.info=info
        self.der=der
   
class Nodoe:
    def __init__(self, info=""):
        self.info=info
    
class Arbol:
    def __init__(self,raiz=Nodoe()):
        self.raiz=raiz
```

Pruébela a continuación:

```python
formula= Arbol(
            Nodoi(
                Nodoi(Nodoe(5),"+",Nodoe(2)),
                "*",
                Nodoi(
                    Nodoe(8),
                    "-",
                    Nodoi(Nodoe(9),"/",Nodoe(3))
                )
            )
        )
print(formula.evaluar())
```
