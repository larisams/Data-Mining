## Extracción de asociaciones entre polimorfismos y fenotipos empleando técnicas de minería de datos 

Con los grandes avances en tecnologías de secuanciación masiva, la cantidad de información genómica disponible ha incrementado de manera exponencial, y con ellos ha surgido la necesidad de analizarlos para poder extraer la información que embeben. A pesar de los intentos que se han hecho, no existe un consenso para representar esta información. Para objeto de nuestro estudio, las variantes genéticas o polimorfismos asociados a enfermedades son de vital importancia cuando se trata de encontrar poosibles tratamientos a estas, sin embargo, cada autor los describe con un nombre diferente,dificultando su caracterización de manera contundente, por lo tanto, resulta indispensable contar con una base de datos que unifique los términos y establezca, con base en la información disponible en otras bases de datos, relaciones entre polimorfismos y fenotipos de manera estandarizada para facilitar su acceso y aplicación al desarrollo de tratamientos de enfermedades genéticas.

## Estrategia de solución 

Proponemos aplicar las técnicas de minería de datos así como expresiones regulares para:
1) Clasificar oraciones dentro de textos de literatura científica que contenga asociaciones entre polimorfismos y enfermedades 
2) Extraer estas asociaciones unificando terminologías y estandarizando procesos 

## Archivos 

* Los datasets procesados bajo una estrategia de expresiones regulares sin el uso de técnicas de minería de datos contienen la etiqueta 'RE' en el nombre, así como los scripts utilizados para procesar dichos archivos. 

* Tanto datasets como scripts contienen una etiqueta que representa en que parte del proceso fueron utilizados :
   - PRE : Fase de preprocesamiento de archivos
   - TRA : Fase de entrenamiento de los clasificadores 
   - EVAL: Fase final de evaluación     
   - TES : Fase de evaluación del clasificador     
   - CLA : Fase de clasificación de abstracts 
   - FIN : Archivos resultantes del análisis
