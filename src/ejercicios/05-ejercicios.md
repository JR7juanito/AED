### Ejercicio 5.1
En este ejercicio se trata chequear si una secuencia de paréntesis está bien escrita. Si hay solo un tipo de paréntesis, por ejemplo ( y ), una secuencia correcta sería (()(())) y una incorrecta seria (()))()( o ()). Ésta sería una tarea fácil de responder, pues bastaría con llevar un contador de paréntesis abiertos, que se incrementa cuando se encuentra un ( y se decrementa cuando se encuentra un ) y se va chequeando que este contador nunca sea negativo y cuando se termine la secuencia el contador quede en 0. 

```python
def chequeo(s): # s es un strings con una secuencia de paréntesis ( )
    i = 0 # contador de paréntesis abiertos
    for c in s: 
        if c == "(":
            i +=1
        else:
            i -=1
        if i < 0: break
    if i == 0: return "CORRECTA"
    else : return "INCORRECTA Contador = "+str(i)
```

Probemos con los ejemplos :

```python
print(chequeo("(()(()))"))
print(chequeo("(())(()"))
print(chequeo("(()))"))
```

El problema se hace bastante más complejo cuando hay más de un tipo de paréntesis, por ejemplo (), [] y {} y ellos tienen que estar balanceados respectivamente, es decir se permite {([]{()})} o [{()[]}] pero no ([{]}) o {[()}]
Esto se puede hacer con la ayuda de un Stack o Pila, inicialmente vacío.
Luego, por cada símbolo que se va chequeando:
   - si es un abre paréntesis entonces se pone en el stack y se continúa con el chequeo del próximo símbolo
   - si es un cierra paréntesis entonces se revisa el elemento del tope del stack
    - si el stack está vacío, entonces la secuencia está mal escrita y ahí termina el proceso. 
    - si el stack no está vacío, se extrae el símbolo del tope y se chequea si es un abre paréntesis que coincide con el tipo de cierra paréntesis que se encontró. Si es así, se continúa con el chequeo del próximo símbolo, si no la fórmula está mal escrita y ahí termina el proceso. 

Al final del proceso se debe chequear si el stack esta vacío, con lo cual se comprueba que la fórmula esta bien escrita. Si no, la fórmula está mal escrita.
Se le pide escribir una funcion chequeo2 que reciba 3 parametros de tipo string: ``s``, ``a`` y ``b``. En ``s`` viene la secuencia de paréntesis a chequear, en ``a`` vienen los abre parentesis permitidos y en ``b`` los cierra paréntesis respectivos de modo que en ``b[i]`` está el paréntesis que cierra a ``a[i]``. 
Por simplicidad use la implementacion de pila que viene a continuacion 

```python
class Pila:
    def __init__(self):
        self.s=[]
    def push(self,x):
        self.s.append(x)
    def pop(self):
        assert len(self.s)>0
        return self.s.pop() # pop de lista, no de Pila
    def is_empty(self):
        return len(self.s)==0
```

Y escriba la funcion a continuación:

```python
def chequeo2(s, a, b):
    #Escriba aquí su función
```

Pruébela con los siguientes casos:

```python
print(chequeo2("(()())","(",")"))
print(chequeo2("{([]{()})}","{[(","}])"))
print(chequeo2("{([]()})}","{[(","}])"))
print(chequeo2("{<{<>}>}", "{<","}>"))
print(chequeo2("{<{<>>}>}", "{<","}>"))
```

### Ejercicio 5.2

Agregar a la clase Heap un método ``modificar(k,x)`` que al ser invocado, cambie la prioridad del elemento del casillero ``k``, dándole como nuevo valor ``x`` y asegurando que el heap siga cumpliendo las restricciones de orden. Esta operación debe funcionar en tiempo $O(\log{n})$ en el peor caso. Escriba a continuación la definición del método ``modificar(k,x)``, y pruébela con las instrucciones que aparecen en el casillero siguiente.

```python
import numpy as np
def trepar(a,j): # El elemento a[j] trepa hasta su nivel de prioridad 
    while j>=1 and a[j]>a[(j-1)//2]:
        (a[j],a[(j-1)//2])=(a[(j-1)//2],a[j]) # intercambiamos con el padre
        j=(j-1)//2 # subimos al lugar del padre
        
def hundir(a,j,n): # El elemento a[j] se hunde hasta su nivel de prioridad
    while 2*j+1<n: # mientras tenga al menos 1 hijo
        k=2*j+1 # el hijo izquierdo
        if k+1<n and a[k+1]>a[k]: # el hijo derecho existe y es mayor
            k+=1
        if a[j]>=a[k]: # tiene mejor prioridad que ambos hijos
            break
        (a[j],a[k])=(a[k],a[j]) # se intercambia con el mayor de los hijos
        j=k # bajamos al lugar del mayor de los hijos
    
class Heap:
    def __init__(self,maxn=100):
        self.a=np.zeros(maxn)
        self.n=0
    def insert(self,x):
        assert self.n<len(self.a)
        self.a[self.n]=x    
        trepar(self.a,self.n)
        self.n+=1       
    def extract_max(self):
        assert self.n>0
        x=self.a[0] # esta variable lleva el máximo, el casillero 0 queda vacante
        self.n-=1   # achicamos el heap
        self.a[0]=self.a[self.n] # movemos el elemento sobrante hacia el casillero vacante
        hundir(self.a,0,self.n)
        return x
    def modificar(self, k, x): #Implementar esta función
        pass
    def imprimir(self):
        print(self.a[0:self.n])
```


```python
a=Heap(20)
a.insert(55)
a.insert(50)
a.insert(70)
a.insert(12)
a.insert(36)
a.insert(10)
a.insert(21)
a.insert(24)
a.insert(20)
a.insert(62)
a.imprimir()
a.modificar(4,65)
a.imprimir()
a.modificar(3,15)
a.imprimir()
```
