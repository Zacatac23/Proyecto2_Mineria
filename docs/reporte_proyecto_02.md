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
El código de entrega se presenta en Python, formato permitido por el PDF del
proyecto junto con R o RMarkdown.

## 2. Variable respuesta

La variable respuesta es `asis_med_bin`, creada a partir de `asist`.

- Tipo de variable: cualitativa binaria.
- Clase `1`: registros con `MEDICA`, `PARAMEDICA`, `EMPIRICA` o `COMADRONA`.
- Clase `0`: registros con `NINGUNA`.
- Registros excluidos de la variable respuesta: `IGNORADO`, porque esa categoría
  no significa ausencia de asistencia sino dato desconocido.
- Tipo de problema: clasificación binaria.

La elección se justifica porque permite estudiar diferencias en asistencia antes
de la defunción. Esta variable es relevante para una discusión de brechas de
acceso, contacto con servicios de salud y desigualdades territoriales.

## 3. Antecedentes

Los antecedentes completos se dejaron en `docs/antecedentes_borrador.md`. En resumen,
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
- Selección de variables con suficiente información para modelado.
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

La ejecución reproducida con `data/processed/datos_limpios_proyecto1.csv` usó 799,810
registros para modelado después de excluir `IGNORADO` en `asist`. Las clases
quedaron balanceadas:

- Sin asistencia: 397,807 registros, 49.7%.
- Con asistencia: 402,003 registros, 50.3%.

El script guarda la tabla actualizada en:

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

Interpretación de las figuras generadas:

- `target_distribution.png`: confirma que la variable respuesta está casi
  balanceada, por lo que no fue necesario aplicar SMOTE u otra técnica de
  rebalanceo.
- `model_comparison.png`: compara los modelos por la métrica principal usada
  para ordenar el ranking. Permite observar que las tres variantes de Regresión
  Logística tienen el mejor ROC-AUC, mientras que el Árbol de Decisión con
  profundidad 10 compite mejor en accuracy y F1.
- `confusion_matrix_best.png`: muestra los aciertos y errores del modelo final.
  El modelo clasifica correctamente 111,019 casos sin asistencia y 97,795 casos
  con asistencia; los errores principales son 22,806 casos con asistencia
  predichos como sin asistencia.
- `feature_importance_best.png`: resume las variables codificadas que más pesan
  en el modelo final. Debe usarse como apoyo descriptivo, no como causalidad.

La ejecución reproducida con el CSV real generó este ranking principal:

| Modelo | Accuracy prueba | F1 prueba | ROC-AUC prueba |
| --- | --- | --- | --- |
| Regresión Logística `C=10` | 0.8703 | 0.8627 | 0.9280 |
| Regresión Logística `C=1` | 0.8702 | 0.8626 | 0.9280 |
| Regresión Logística `C=0.01` | 0.8699 | 0.8622 | 0.9275 |
| Random Forest `n_estimators=100`, `max_depth=10` | 0.8727 | 0.8614 | 0.9267 |
| Árbol de Decisión `max_depth=10` | 0.8758 | 0.8651 | 0.9251 |

La matriz de confusión del mejor modelo por ROC-AUC, Regresión Logística `C=10`,
fue:

|  | Pred. sin asistencia | Pred. con asistencia |
| --- | ---: | ---: |
| Real sin asistencia | 111,019 | 8,323 |
| Real con asistencia | 22,806 | 97,795 |

## 9. Selección del modelo final

El script selecciona automáticamente el mejor modelo ordenando por ROC-AUC,
F1-score y accuracy de prueba. Con ese criterio, el modelo final es Regresión
Logística con `C=10`, porque obtuvo el mayor ROC-AUC reproducido (0.9280) y una
brecha train/test baja de 0.0005, sin señales fuertes de sobreajuste.

Si el equipo decide priorizar accuracy o F1 sobre ROC-AUC, el Árbol de Decisión
con `max_depth=10` es una alternativa defendible, porque alcanzó mayor accuracy
de prueba (0.8758) y F1 (0.8651). Esta diferencia debe explicarse en el informe:
ROC-AUC evalúa la capacidad de ordenar probabilidades en todos los umbrales,
mientras accuracy y F1 evalúan el desempeño con el umbral de clasificación usado
para la matriz de confusión.

## 10. Conclusiones

El repositorio ya contenía un avance sustancial de modelado en notebook. La
revisión agregó un flujo reproducible que guarda resultados y figuras desde el
código, además de documentación para ejecutar y completar la entrega. La variable
respuesta está bien alineada con un problema de clasificación binaria y el
balance de clases no requiere técnicas adicionales como SMOTE.

El pendiente principal ya no es técnico de modelado, sino de entrega: convertir
este borrador a Word/PDF, insertar las figuras generadas y asegurar que el
documento final muestre contribuciones individuales del equipo.

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
