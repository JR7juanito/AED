### Ejercicio 7.1 (Quicksort con mediana de 3)

Modifique el algoritmo Quicksort para que en la fase de partición utilice como pivote a la mediana de 3 elementos elegidos al azar.

Para esto, se recomienda modificar el algoritmo de partición de modo que seleccione 3 elementos al azar en el rango $i..j$ y los ordene, dejando en $a[i]$ el mínimo de los 3, en $a[i+1]$ la mediana de los 3 y en $a[j]$ el máximo de los 3. Luego, se aplica el algoritmo de partición ya conocido al segmento $a[i+2],\ldots,a[j-1]$, con $a[i+1]$ como pivote. Al terminar, el pivote se mueve al centro y se retorna su posición.

Otro cambio que se debe hacer es tratar los casos de arreglos de tamaño $0$, $1$ y $2$ como casos de borde, y aplicar ``qsort`` recursivo solo a arreglos de tamaño mayor o igual a 3.

En el siguiente recuadro escriba su algoritmo modificado y luego ejecute las instrucciones de prueba del recuadro siguiente.

```python
def quicksort3(a):
  qsort(a,0,len(a)-1)

#Esta es la versión del apunte que deberá modificar
def qsort(a,i,j): # ordena a[i],...,a[j]
  if (j-i)<3:
    #Añadir casos de borde
  else:
    k=particionMedianaDe3(a,i,j)
    qsort(a,i,k-1)
    qsort(a,k+1,j)

#Implementar esta función de acuerdo al enunciado
def particionMedianaDe3(a,i,j): # particiona a[i],...,a[j], retorna posición del pivote
  pass
```


```python
import numpy as np
a = np.random.random(12)
print(a)
chequea_orden(a)
quicksort3(a)
print(a)
chequea_orden(a)
```

---
### Ejercicio 7.2 (Radix Sort)

Ordene el conjunto

```
    73895
    93754 
    82149
    99046
    14853
    94171
    54963
    70471
    80564
    66496
```

usando Radix Sort. Muestre el estado del conjunto después cada pasada (una pasada consiste en la separación en grupos de acuerdo a los dígitos presentes en la columna que se está procesando, seguida de la concatenación de los grupos resultantes). Recuerde que las columnas se procesan de derecha a izquierda y que a igualdad de valores, se debe preservar el orden original.

Para entregar su solución y verificar que esté correcta, sustituya los ceros por la información correcta en el siguiente código. Para ayudarle a empezar, se entrega el resultado después de la primera pasada.

```python
import numpy as np

# Verifica que la lista 'a' esté ordenada después de haber efectuado 'k' pasadas
# Se muestran solo los k dígitos de más a la derecha de cada número
def verifica_orden(k,a):
  b=[x%(10**k) for x in a]
  print(b)
  print("Ordenado" if np.all([b[i]<=b[i+1] for i in range(0,len(b) - 1)]) else "Desordenado")
```


```python
verifica_orden(1,[94171,70471,14853,54963,93754,80564,73895,99046,66496,82149])
```


```
[1, 1, 3, 3, 4, 4, 5, 6, 6, 9]
Ordenado

```


```python
verifica_orden(2,[0,0,0,0,0,0,0,0,0,0])
```


```
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Ordenado

```


```python
verifica_orden(3,[0,0,0,0,0,0,0,0,0,0])
```


```
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Ordenado

```


```python
verifica_orden(4,[0,0,0,0,0,0,0,0,0,0])
```


```
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Ordenado

```


```python
verifica_orden(5,[0,0,0,0,0,0,0,0,0,0])
```


```
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Ordenado

```

---
### Ejercicio 7.3 (Merge de listas con repeticiones)

Suponga que se desea mezclar dos listas ordenadas de manera ascendente en las cuales puede haber elementos repetidos. Estas listas se representan en forma compacta como una secuencia de tuplas en que para cada elemento se indica su *multiplicidad*, es decir, el número de veces que se repite. Por ejemplo, la lista
```
[(12,2),(34,1),(56,3),(74,1),(81,1)]
```
es la representación compacta de la lista
```
[12,12,34,56,56,56,74,81]
```
Se pide escribir un método ``merge(a,b)`` que reciba como argumento dos listas compactas ``a`` y ``b`` y retorne el resultado de mezclarlas. El resultado debe estar también en formato compacto.

Para esto, usted debe modificar el método ``merge``del apunte, el que aparece a continuación:


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

y luego debe probarlo ejecutando el código siguiente:

```python
a=[(12,2),(34,1),(56,3),(74,1),(81,1)]
b=[(10,3),(12,5),(65,1),(74,1),(90,3)]
c=[x for x in merge(a,b)]
print(c)
```
