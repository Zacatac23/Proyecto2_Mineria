# Proyecto 02 - Minería de Datos

## 1. Introducción

Este proyecto utiliza registros de defunciones de Guatemala para construir
modelos predictivos que clasifiquen si una defunción tuvo asistencia antes del
fallecimiento. El dataset trabajado en el notebook corresponde a
`datos_limpios_proyecto1.csv`, un archivo limpio generado en el Proyecto 01 a
partir de datos de defunciones del INE Guatemala.

El objetivo predictivo es apoyar el análisis de patrones asociados al acceso o
contacto con asistencia, usando variables disponibles en los registros:
características demográficas, territoriales, temporales y de causa de defunción.

## 2. Variable respuesta

La variable respuesta es `asis_med_bin`, creada a partir de `asist`.

- Tipo de variable: cualitativa binaria.
- Clase `1`: registros con `MEDICA`, `PARAMEDICA`, `EMPIRICA` o `COMADRONA`.
- Clase `0`: registros sin asistencia o con otra categoría registrada, por
  ejemplo `NINGUNA` o `IGNORADO`.
- Tipo de problema: clasificación binaria.

La elección se justifica porque permite estudiar diferencias en asistencia antes
de la defunción. Esta variable es relevante para una discusión de brechas de
acceso, contacto con servicios de salud y desigualdades territoriales.

## 3. Antecedentes

Los antecedentes completos se dejaron en `antecedentes_borrador.md`. En resumen,
las fuentes revisadas cubren tres líneas:

- La fuente oficial del dataset: estadísticas vitales de defunciones del INE.
- El contexto de acceso y desigualdad en salud en Guatemala, documentado por
  OPS/PAHO, Banco Mundial y el estudio de Owen, Obregón y Jacobsen sobre acceso
  geográfico a servicios de salud en Alta Verapaz.
- El uso de aprendizaje automático en problemas clínicos de clasificación,
  especialmente predicción de mortalidad, donde se comparan regresión logística,
  árboles, Random Forest, SVM, KNN y modelos de boosting.

Estos antecedentes respaldan la selección de variables territoriales y
demográficas, así como la comparación entre un modelo lineal interpretable, un
árbol y un ensamble de árboles.

## 4. Selección de algoritmos

Se consideraron más de tres algoritmos posibles: Regresión Logística, Árbol de
Decisión, Random Forest, KNN, SVM y Gradient Boosting/XGBoost. Para la
implementación reproducible se seleccionaron tres:

- Regresión Logística: modelo base interpretable para clasificación binaria.
- Árbol de Decisión: modelo explicable mediante reglas y control de profundidad.
- Random Forest: ensamble no lineal que reduce varianza y suele funcionar bien
  con variables mixtas.

La selección equilibra interpretabilidad, desempeño y facilidad de reproducción
con scikit-learn.

## 5. Preparación de los datos

El script `run_project.py` implementa:

- Normalización de nombres de columnas.
- Estandarización de texto: mayúsculas, espacios y eliminación de tildes.
- Conversión de columnas numéricas como `anoreg`, `mesreg`, `diaocu`, `edadif`
  y `edad_anios`.
- Cálculo de `edad_anios` si no existe y están disponibles `edadif` y `perdif`.
- Creación de `causa_capitulo` desde `caudef` si no existe.
- Filtro de edades válidas entre 0 y 115 años.
- Creación de `asis_med_bin` desde `asist`.
- Selección de variables con máximo 30% de nulos.
- Imputación de nulos en pipelines.
- Codificación One-Hot para variables categóricas.
- Escalamiento de variables numéricas.

Las variables candidatas para el modelado son:

- Numéricas: `edad_anios`, `anoreg`.
- Categóricas: `sexo`, `areag`, `depocu`, `depreg`, `ocur`,
  `causa_capitulo`, `perdif`, `mesreg`.

## 6. Conjuntos de entrenamiento y prueba

Se utiliza una división 70% entrenamiento y 30% prueba con semilla fija
`random_state=42`. Como la variable respuesta es categórica, la división se hace
con estratificación para preservar la proporción de clases.

El notebook existente reporta una ejecución previa con 802,793 registros de
modelado y clases casi balanceadas: 49.7% con asistencia y 50.3% sin asistencia.
El script nuevo guarda la tabla actualizada en:

- `outputs/results/class_balance.csv`
- `outputs/results/class_balance.md`

## 7. Modelos generados

El script genera al menos tres variaciones por algoritmo:

- Árbol de Decisión: `max_depth` 3, 5 y 10.
- Random Forest: combinaciones de `n_estimators` y `max_depth`.
- Regresión Logística: valores de `C` 0.01, 1 y 10.

Cada modelo se entrena en el conjunto de entrenamiento y se evalúa en el conjunto
de prueba. El ranking completo se guarda en:

- `outputs/results/model_results.csv`
- `outputs/results/model_results.md`

## 8. Evaluación de resultados

Para clasificación se calculan:

- Accuracy.
- Balanced accuracy.
- Precision.
- Recall.
- F1-score.
- ROC-AUC.
- Matriz de confusión del mejor modelo.

Las salidas se generan automáticamente en:

- `outputs/results/confusion_matrix_best.csv`
- `outputs/results/classification_report_best.csv`
- `outputs/figures/confusion_matrix_best.png`
- `outputs/figures/model_comparison.png`
- `outputs/figures/target_distribution.png`
- `outputs/figures/feature_importance_best.png`

La ejecución guardada dentro del notebook reporta como mejor modelo previo:
Random Forest con `n_estimators=100` y `max_depth=10`, accuracy de prueba 0.8685
y ROC-AUC 0.9256. Esos valores deben regenerarse con `run_project.py` antes de
cerrar la entrega final, porque el CSV no está presente en esta copia local.

## 9. Selección del modelo final

El script selecciona automáticamente el mejor modelo ordenando por ROC-AUC,
F1-score y accuracy de prueba. También calcula la diferencia entre accuracy de
entrenamiento y prueba para revisar señales de sobreajuste.

En la ejecución previa guardada en el notebook, Random Forest fue el mejor modelo
y el árbol sin límite de profundidad mostró sobreajuste, ya que la diferencia
entre entrenamiento y prueba fue mucho mayor que en los modelos con profundidad
controlada.

## 10. Conclusiones

El repositorio ya contenía un avance sustancial de modelado en notebook. La
revisión agregó un flujo reproducible que guarda resultados y figuras desde el
código, además de documentación para ejecutar y completar la entrega. La variable
respuesta está bien alineada con un problema de clasificación binaria y el
balance de clases observado en el notebook no requiere técnicas adicionales como
SMOTE.

El principal pendiente técnico es recuperar o colocar el archivo
`datos_limpios_proyecto1.csv` para regenerar los resultados finales. También
queda pendiente convertir este borrador a Word/PDF y asegurar que el documento
final muestre contribuciones individuales del equipo.

## 11. Referencias

Instituto Nacional de Estadística. (2024). *Estadísticas vitales - defunciones*
[Conjunto de datos]. Gobierno de Guatemala. Recuperado el 18 de mayo de 2026,
de https://datos.ine.gob.gt/es/dataset/estadisticas-vitales-defunciones

Naemi, A., Schmidt, T., Mansourvar, M., Naghavi-Behzad, M., Ebrahimi, A., &
Wiil, U. K. (2021). Machine learning techniques for mortality prediction in
emergency departments: A systematic review. *BMJ Open, 11*(11), e052663.
https://doi.org/10.1136/bmjopen-2021-052663

Owen, K. K., Obregón, E. J., & Jacobsen, K. H. (2010). A geographic analysis of
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
