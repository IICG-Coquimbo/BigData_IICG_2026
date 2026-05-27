## Pregunta 1: ¿El problema es el algoritmo o los datos?

El problema de los resultados no está en los modelos en sí, ya que cada uno cumplió con su propósito (tanto los árboles de decisión, Random Forest y SVM en clasificación, como la regresión en la predicción).

Los problemas vienen de cómo se usaron los datos:

En la clasificación: Los datos ya se habían agrupado antes a través de K-Means, lo que determinó de antemano las etiquetas. Por lo tanto, la clasificación "ya estaba hecha" y los modelos supervisados solo la repitieron.

En la regresión: El bajo resultado se debe a que las variables predictoras no son representativas para este caso. No hay una relación real entre el precio de un producto y las variables de opiniones o rating. Las opiniones que tenga un producto o su cantidad de estrellas en internet no determinan ni se relacionan con el precio que la empresa decide ponerle.

## Pregunta 2: ¿Cómo lo solucionarían en el mundo real? ¿Qué datos faltan?

Para solucionar el problema de los datos, hay que encontrar variables que realmente influyan o tengan relación con el precio de venta en el mercado. Por ejemplo:

Impuestos a la importación de las distintas bolsas de comida.

Precios de los ingredientes utilizados por las distintas marcas.

Tasas y costos de transporte.

Precios de la competencia.

Estas variables de costos y mercado sí pueden explicar los precios que se ven en las distintas categorías o clusters de productos.