# Revisión del Proyecto 02 - Minería de Datos

## 1. Estado general del repositorio

El repositorio contenía un avance principal en Python/Jupyter:
`Proyecto2_Defunciones_Guatemala.ipynb`, más el script auxiliar
`fix_notebook.py`. No existían README, requirements, reporte final, antecedentes
ni script reproducible independiente. El PDF de instrucciones se encontró fuera
de la raíz del repositorio, en la carpeta padre:
`../Proyecto 02 - DM.pdf`.

El notebook ya define una variable respuesta, entrena tres algoritmos y conserva
salidas de una ejecución previa. En esta segunda revisión se encontró el CSV real
en `data/processed/datos_limpios_proyecto1.csv` y se ejecutó el flujo reproducible
`run_project.py` con métricas y figuras nuevas. El CSV pesa aproximadamente
289 MB y se mantiene ignorado por Git.

Veredicto sobre lenguaje: el PDF permite entregar script de R (`.r` o `.rmd`) o
script de Python. El uso de Python/Jupyter en este repositorio cumple el
requisito; no es necesario migrar el proyecto a R.

## 2. Archivos encontrados

| Archivo | Función | Estado |
| --- | --- | --- |
| `.gitignore` | Ignora `datos_limpios_proyecto1.csv` y artefactos locales de Python/Jupyter. | Existente; actualizado |
| `Proyecto2_Defunciones_Guatemala.ipynb` | Notebook principal con carga, limpieza, variable respuesta, modelos y métricas guardadas de una ejecución previa. | Existente; avance parcial fuerte |
| `fix_notebook.py` | Script auxiliar histórico para corregir celdas del notebook. | Existente; no es el flujo final |
| `run_project.py` | Script reproducible agregado para ejecutar limpieza, modelado, métricas y figuras. | Creado |
| `requirements.txt` | Dependencias de Python. | Creado |
| `README.md` | Instrucciones de instalación, dataset, ejecución y salidas. | Creado |
| `docs/antecedentes_borrador.md` | Borrador de antecedentes con fuentes verificables y referencias APA 7. | Creado |
| `docs/reporte_proyecto_02.md` | Borrador estructurado del informe final. | Creado |
| `docs/REVISION_PROYECTO_02.md` | Revisión técnica contra el PDF del proyecto. | Creado |
| `outputs/figures/.gitkeep` | Carpeta preparada para figuras generadas. | Creado |
| `outputs/results/.gitkeep` | Carpeta preparada para tablas y métricas generadas. | Creado |
| `data/processed/datos_limpios_proyecto1.csv` | Dataset limpio real usado para la ejecución reproducible. | Disponible localmente; ignorado por Git |
| `outputs/results/model_results.csv` | Ranking de modelos generado desde código. | Generado |
| `outputs/results/class_balance.csv` | Balance de clases generado desde código. | Generado |
| `outputs/results/confusion_matrix_best.csv` | Matriz de confusión del mejor modelo por ROC-AUC. | Generado |
| `outputs/figures/*.png` | Figuras de distribución, comparación, matriz e importancia. | Generado |
| `../Proyecto 02 - DM.pdf` | Instrucciones y rúbrica del Proyecto 02. | Encontrado fuera del repo |

## 3. Checklist contra el PDF del proyecto

| Requisito | Estado | Evidencia en repo | Acción realizada |
| --- | --- | --- | --- |
| Selección de variable respuesta | Completo | Notebook define `asis_med`; script usa `asis_med_bin`. | Se documentó en README y reporte. |
| Explicar si la variable es cuantitativa o cualitativa | Completo | Notebook indica clasificación binaria. | Se amplió en `docs/reporte_proyecto_02.md`. |
| Justificación de la elección | Completo | Notebook incluye justificación breve. | Se reforzó en README, reporte y antecedentes. |
| Investigación de antecedentes con fuentes confiables | Parcial | No existía antes. | Se creó `docs/antecedentes_borrador.md` con fuentes verificables. |
| Antecedentes de al menos 2 páginas | Parcial | No existía documento final. | Se dejó borrador largo; debe integrarse al Word/PDF final. |
| Selección y justificación de al menos 3 algoritmos | Completo | Notebook usa Árbol, Random Forest y Regresión Logística. | Se documentó y automatizó en `run_project.py`. |
| Considerar más de 3 algoritmos posibles | Completo | No estaba explícito. | Se agregaron KNN, SVM y Gradient Boosting/XGBoost como algoritmos valorados en antecedentes/reporte. |
| Método para obtener train/test | Completo | Notebook usa `train_test_split`. | Script usa 70/30 estratificado con semilla fija. |
| Porcentaje train/test | Completo | Notebook indica 70/30. | Se documentó en README y reporte. |
| Balanceo si es clasificación | Completo | Notebook reporta clases 49.7% y 50.3%. | Script genera `class_balance.csv` y `class_balance.md`. |
| Análisis de atípicos si es regresión | No aplica | El problema es clasificación. | No aplica. |
| Preprocesamiento y transformaciones | Completo | Notebook normaliza texto, codifica y escala. | Script agrega pipelines con imputación, One-Hot y escalamiento. |
| Al menos 3 variaciones por algoritmo | Completo | Notebook prueba varias profundidades, bosques y valores de C. | Script genera 3 variaciones por cada algoritmo. |
| Modelo final con mejores parámetros | Completo | Notebook selecciona Random Forest previo. | Script selecciona automáticamente por ROC-AUC, F1 y accuracy. |
| Métricas de evaluación | Completo | Notebook tiene métricas previas y script generó métricas nuevas con CSV real. | Se guardó `outputs/results/model_results.csv`. |
| Matriz de confusión para clasificación | Completo | Notebook muestra matrices y script generó matriz nueva. | Se guardó `confusion_matrix_best.csv` y figura. |
| Gráficas/tablas explicadas | Parcial | Script exporta figuras; reporte explica dónde incluirlas. | Falta insertar y comentar cada figura en el Word/PDF final. |
| Script final reproducible | Completo con dependencia de datos | No existía script final. | Se creó `run_project.py`. |
| Documento o reporte final | Parcial | No existía. | Se creó `docs/reporte_proyecto_02.md`; falta convertirlo a Word/PDF final. |
| README con instrucciones | Completo | No existía. | Se creó `README.md`. |
| Evidencia de contribuciones/código | Parcial | Git tiene dos commits previos; no hay control de cambios de documento. | Se documentó pendiente para el equipo. |
| Material Word/PDF final | Faltante | No hay `.docx` ni `.pdf` final del informe. | Se dejó borrador Markdown convertible. |
| Vínculo de repositorio GitHub | Completo | Repo tiene remoto `origin`: `https://github.com/Zacatac23/Proyecto2_Mineria.git`. | Falta confirmar que todos los resultados finales estén agregados y subidos. |

## 4. Problemas encontrados

- El dataset `datos_limpios_proyecto1.csv` está disponible localmente en
  `data/processed/`, pero no debe versionarse porque pesa aproximadamente 289 MB.
- El PDF de requisitos no está dentro de la raíz del repo, sino en la carpeta
  padre y también fue proporcionado en `Downloads`.
- El notebook conserva una lógica previa que trataba `IGNORADO` como clase 0; el
  script final lo trata como valor desconocido y lo excluye de `y`.
- No existían README, requirements, reporte, antecedentes ni salidas exportadas
  antes de la revisión.
- El notebook depende de una ruta relativa distinta; el script final usa por
  defecto `data/processed/datos_limpios_proyecto1.csv`.
- `fix_notebook.py` parece ser un script auxiliar de corrección previa y no debe
  considerarse el script final de entrega.
- No existe documento Word/PDF final con contribuciones visibles del equipo.

## 5. Implementaciones realizadas

- Se creó `run_project.py` como flujo reproducible de principio a fin.
- Se agregaron pipelines de scikit-learn con imputación, One-Hot Encoding y
  escalamiento.
- Se automatizó la creación de `asis_med_bin` desde `asist`.
- Se implementó split 70/30 estratificado con semilla fija.
- Se implementaron tres variaciones por algoritmo para Árbol de Decisión,
  Random Forest y Regresión Logística.
- Se automatizaron métricas: accuracy, balanced accuracy, precision, recall,
  F1-score, ROC-AUC y brecha train/test.
- Se programó la exportación de tablas en CSV y Markdown.
- Se programó la exportación de gráficas útiles en `outputs/figures/`.
- Se ejecutó el flujo con `data/processed/datos_limpios_proyecto1.csv`.
- Se ajustó la variable respuesta para excluir `IGNORADO` como dato desconocido.
- Se conservó `areag` como predictor, imputando faltantes categóricos como
  `DESCONOCIDO`.
- Se creó `README.md` con instrucciones de instalación y ejecución.
- Se creó `requirements.txt`.
- Se creó `docs/antecedentes_borrador.md` con fuentes verificables.
- Se creó `docs/reporte_proyecto_02.md` con la estructura solicitada.
- Se prepararon carpetas `outputs/results/` y `outputs/figures/`.

## 6. Modelos y evaluación

El flujo reproducible con el CSV real usó 799,810 registros de modelado. Se
excluyeron 9,482 registros con `asist = IGNORADO` porque no permiten confirmar
si hubo o no asistencia. Las clases quedaron balanceadas: 397,807 sin asistencia
(49.7%) y 402,003 con asistencia (50.3%).

Resultados principales de la nueva ejecución:

| Modelo | Accuracy test | ROC-AUC | Comentario |
| --- | --- | --- | --- |
| Regresión Logística `C=10` | 0.8703 | 0.9280 | Mejor modelo por ROC-AUC. |
| Random Forest `n_estimators=100`, `max_depth=10` | 0.8727 | 0.9267 | Buen equilibrio, alta precisión. |
| Árbol de Decisión `max_depth=10` | 0.8758 | 0.9251 | Mejor accuracy y F1, alternativa defendible si se prioriza clasificación directa. |

El mejor modelo automático se selecciona por ROC-AUC, luego F1 y luego accuracy.
Con ese criterio el modelo final es Regresión Logística `C=10`. Si el equipo
prefiere priorizar accuracy/F1 para la matriz de confusión, debe justificar la
selección del Árbol de Decisión `max_depth=10`.

## 7. Archivos modificados o creados

- `README.md`
- `docs/REVISION_PROYECTO_02.md`
- `.gitignore`
- `docs/antecedentes_borrador.md`
- `docs/reporte_proyecto_02.md`
- `requirements.txt`
- `run_project.py`
- `outputs/figures/.gitkeep`
- `outputs/results/.gitkeep`
- `data/.gitkeep`
- `data/processed/.gitkeep`
- Salidas generadas en `outputs/results/` y `outputs/figures/` quedan ignoradas por Git.

No se ejecutó commit manual durante esta revisión. Antes de entregar, revisar
`git status` y decidir si se versionan las salidas generadas.

## 8. Cómo ejecutar el proyecto

Instalar dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Ejecutar con el CSV real disponible actualmente:

```powershell
python run_project.py
```

Ejecutar con ruta explícita:

```powershell
python run_project.py --data data\processed\datos_limpios_proyecto1.csv
```

Ejecutar con el CSV en otra ubicación:

```powershell
python run_project.py --data ruta\al\datos_limpios_proyecto1.csv
```

Ejecutar con varios archivos originales en una carpeta:

```powershell
python run_project.py --data-dir data\raw
```

## 9. Pendientes

- Revisar las tablas y figuras generadas en `outputs/` e insertarlas en el
  documento final.
- Integrar `docs/antecedentes_borrador.md` y `docs/reporte_proyecto_02.md` en el documento
  final Word/PDF solicitado por el curso.
- Asegurar que el documento Word o Google Docs muestre contribuciones de todos
  los integrantes.
- Agregar al informe final las tablas y gráficas generadas por el script, con
  explicación textual de cada una.
