# Antecedentes - Proyecto 02

## Tema del proyecto

El proyecto trabaja con registros de defunciones de Guatemala y plantea un
problema de clasificacion binaria: predecir si la persona fallecida tuvo algun
tipo de asistencia antes de la defuncion. La variable respuesta se construye a
partir de `asist`, separando los casos con asistencia registrada (`MEDICA`,
`PARAMEDICA`, `EMPIRICA`, `COMADRONA`) de los casos sin asistencia o con
asistencia no especificada. Este planteamiento conecta el analisis predictivo
con una pregunta de salud publica: que caracteristicas demograficas,
geograficas, temporales o clinicas se asocian con la presencia o ausencia de
asistencia.

Los datos de defunciones del Instituto Nacional de Estadistica de Guatemala
forman parte de las estadisticas vitales. El portal del INE describe estas
estadisticas como registros administrativos de nacimientos, defunciones,
matrimonios y divorcios, utiles para observar cambios en mortalidad, fecundidad
y nupcialidad y para calcular indicadores demograficos importantes para el
sector salud. Por esa razon, el uso de estos registros como base para modelos
predictivos es consistente con el objetivo de extraer patrones utiles para la
toma de decisiones en salud.

## Contexto de salud y acceso en Guatemala

La Organizacion Panamericana de la Salud, en el perfil de Guatemala de Health in
the Americas, reporta que la esperanza de vida al nacer fue de 72.7 anios en
2024, menor que el promedio regional, y que el gasto de bolsillo represento una
porcion alta del gasto total en salud. El mismo perfil describe estrategias del
MSPAS orientadas a redes integradas de servicios de salud, acceso universal y
reduccion de desigualdades. Estos elementos son relevantes para este proyecto
porque la variable `asis_med_bin` no mide directamente cobertura sanitaria, pero
si representa una senial administrativa de contacto con asistencia al momento o
antes de la defuncion.

Un antecedente mas cercano al pais es el estudio de Owen, Obregon y Jacobsen
(2010), que analiza el acceso geografico a servicios de salud en Alta Verapaz
mediante analisis de redes viales. El articulo muestra que el acceso no depende
solo de distancia lineal, sino de caminos, tiempos de viaje, pobreza y
distribucion territorial de servicios. Aunque ese trabajo no es un modelo de
clasificacion sobre defunciones, aporta una justificacion importante para
incluir variables como departamento, area geografica y lugar de ocurrencia, pues
el acceso a servicios en Guatemala tiene un componente territorial fuerte.

El Banco Mundial tambien identifica a Guatemala como un pais con desafios
estructurales de acceso a servicios, desigualdad territorial, pobreza rural y
brechas para poblaciones indigenas. Estos antecedentes ayudan a contextualizar
por que variables de residencia, ocurrencia y caracteristicas demograficas
pueden aportar informacion predictiva. En el informe final conviene conectar
estas fuentes con graficas propias del dataset, por ejemplo distribucion de la
asistencia por departamento, area geografica, sexo y edad.

## Antecedentes de aprendizaje automatico en problemas similares

En problemas de salud, la prediccion con aprendizaje automatico suele comparar
modelos interpretables con modelos de mayor capacidad no lineal. Naemi et al.
(2021) revisaron modelos de aprendizaje automatico para predecir mortalidad en
departamentos de emergencia. El estudio encontro el uso de regresion logistica,
arboles de decision, KNN, SVM, gradient boosting, random forest y redes
neuronales, y tambien senalo que muchos estudios fallan al reportar
preprocesamiento, manejo de valores faltantes y validacion. Para este proyecto,
esa conclusion respalda la necesidad de dejar un script reproducible, separar
entrenamiento y prueba, documentar transformaciones y guardar metricas.

Zhang et al. (2023) realizaron una revision sistematica y metaanalisis sobre
prediccion de muerte relacionada con sepsis. Aunque el desenlace es distinto,
el trabajo es util porque resume familias de modelos frecuentes en clasificacion
clinica: regresion logistica, arboles, random forest, SVM, KNN, XGBoost y redes
neuronales. Sus resultados resaltan el valor de modelos de ensamble como Random
Forest y XGBoost en datos clinicos con relaciones no lineales. Esto se relaciona
con el presente proyecto porque variables como causa, lugar de ocurrencia, edad
y territorio probablemente no se combinan de forma estrictamente lineal.

La regresion logistica sigue siendo un punto de comparacion importante porque
permite interpretar direccion e intensidad de asociaciones bajo una estructura
lineal. Los arboles de decision aportan interpretabilidad visual y reglas
simples que pueden explicarse en un informe academico. Random Forest reduce la
varianza de arboles individuales y suele mejorar desempenio al combinar muchos
arboles entrenados con subconjuntos de datos y variables. Por esa combinacion de
interpretabilidad, comparabilidad y capacidad predictiva, estos tres algoritmos
son adecuados para una primera entrega reproducible.

## Relacion con los algoritmos seleccionados

Los antecedentes sugieren evaluar mas de tres algoritmos posibles:

- Regresion Logistica: base interpretable para clasificacion binaria.
- Arbol de Decision: reglas explicables y facil comparacion de profundidad.
- Random Forest: ensamble robusto para relaciones no lineales y variables mixtas.
- KNN: alternativa basada en proximidad, sensible al escalamiento.
- SVM: alternativa potente para fronteras no lineales, aunque costosa en datasets
  grandes.
- Gradient Boosting o XGBoost: ensambles competitivos, recomendables para una
  extension si se dispone de tiempo y dependencias.

Para el flujo implementado se seleccionan Regresion Logistica, Arbol de Decision
y Random Forest. La seleccion cubre un modelo lineal interpretable, un modelo de
reglas y un ensamble no lineal. Ademas, los tres estan disponibles en
scikit-learn, no requieren dependencias externas pesadas y permiten variar
hiperparametros de forma clara: `C` en regresion logistica, `max_depth` en
arboles y `n_estimators`/`max_depth` en Random Forest.

## Referencias en formato APA 7

Instituto Nacional de Estadistica. (2024). *Estadisticas vitales - defunciones*
[Conjunto de datos]. Gobierno de Guatemala. Recuperado el 18 de mayo de 2026,
de https://datos.ine.gob.gt/es/dataset/estadisticas-vitales-defunciones

Naemi, A., Schmidt, T., Mansourvar, M., Naghavi-Behzad, M., Ebrahimi, A., &
Wiil, U. K. (2021). Machine learning techniques for mortality prediction in
emergency departments: A systematic review. *BMJ Open, 11*(11), e052663.
https://doi.org/10.1136/bmjopen-2021-052663

Owen, K. K., Obregon, E. J., & Jacobsen, K. H. (2010). A geographic analysis of
access to health services in rural Guatemala. *International Health, 2*(2),
143-149. https://doi.org/10.1016/j.inhe.2010.03.002

Pan American Health Organization. (2024). *Guatemala - Country profile*. Health
in the Americas. Recuperado el 18 de mayo de 2026, de
https://hia.paho.org/en/country-profiles/guatemala

World Bank. (2025). *Guatemala overview*. Recuperado el 18 de mayo de 2026, de
https://www.worldbank.org/en/country/guatemala/overview

Zhang, Y., Xu, W., Yang, P., & Zhang, A. (2023). Machine learning for the
prediction of sepsis-related death: A systematic review and meta-analysis.
*BMC Medical Informatics and Decision Making, 23*, 283.
https://doi.org/10.1186/s12911-023-02383-1
