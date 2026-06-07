### Ejercicio 2.1

Resuelva la ecuación

$$
a_n=b_n a_{n-1}+c_n
$$

donde $b_n$ y $c_n$ son funciones conocidas y $b_n\neq 0$ for all $n\ge 0$.
### Ejercicio 2.2

Resuelva la ecuación homogénea de las Torres de Hanoi:

$$
\begin{align}
a_n-3a_{n-1}+2a_{n-2}&=0 \text{ para } n\ge 2\\
a_0=0\\
a_1=1
\end{align}
$$
### Ejercicio 2.3

El método del ordenación **Stooge Sort** es un método recursivo que puede describirse de la siguiente manera:

* Si el primer elemento es mayor que el último, los intercambiamos
* Si hay 3 o más elementos en la lista, entonces:
    * Ordenar los primeros 2/3 de la lista recursivamente
    * Ordenar los últimos 2/3 de la lista, recursivamente, y
    * Ordenar (¡de nuevo!) los primeros 2/3 de la lista.

Escriba una ecuación que modele el tiempo de ejecución de Stooge Sort y resuélvala usando el Teorema Maestro.