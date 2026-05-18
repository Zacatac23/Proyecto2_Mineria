# Revisión del Proyecto 02 - Minería de Datos

## 1. Estado general del repositorio

El repositorio contenía un avance principal en Python/Jupyter:
`Proyecto2_Defunciones_Guatemala.ipynb`, más el script auxiliar
`fix_notebook.py`. No existían README, requirements, reporte final, antecedentes
ni script reproducible independiente. El PDF de instrucciones se encontró fuera
de la raíz del repositorio, en la carpeta padre:
`../Proyecto 02 - DM.pdf`.

El notebook ya define una variable respuesta, entrena tres algoritmos y conserva
salidas de una ejecución previa. Sin embargo, el dataset usado
`datos_limpios_proyecto1.csv` está en `.gitignore` y no está disponible en esta
copia local, por lo que no fue posible regenerar métricas nuevas durante esta
revisión.

## 2. Archivos encontrados

| Archivo | Función | Estado |
| --- | --- | --- |
| `.gitignore` | Ignora `datos_limpios_proyecto1.csv` y artefactos locales de Python/Jupyter. | Existente; actualizado |
| `Proyecto2_Defunciones_Guatemala.ipynb` | Notebook principal con carga, limpieza, variable respuesta, modelos y métricas guardadas de una ejecución previa. | Existente; avance parcial fuerte |
| `fix_notebook.py` | Script auxiliar histórico para corregir celdas del notebook. | Existente; no es el flujo final |
| `run_project.py` | Script reproducible agregado para ejecutar limpieza, modelado, métricas y figuras. | Creado |
| `requirements.txt` | Dependencias de Python. | Creado |
| `README.md` | Instrucciones de instalación, dataset, ejecución y salidas. | Creado |
| `antecedentes_borrador.md` | Borrador de antecedentes con fuentes verificables y referencias APA 7. | Creado |
| `reporte_proyecto_02.md` | Borrador estructurado del informe final. | Creado |
| `REVISION_PROYECTO_02.md` | Revisión técnica contra el PDF del proyecto. | Creado |
| `outputs/figures/.gitkeep` | Carpeta preparada para figuras generadas. | Creado |
| `outputs/results/.gitkeep` | Carpeta preparada para tablas y métricas generadas. | Creado |
| `../Proyecto 02 - DM.pdf` | Instrucciones y rúbrica del Proyecto 02. | Encontrado fuera del repo |

## 3. Checklist contra el PDF del proyecto

| Requisito | Estado | Evidencia en repo | Acción realizada |
| --- | --- | --- | --- |
| Selección de variable respuesta | Completo | Notebook define `asis_med`; script usa `asis_med_bin`. | Se documentó en README y reporte. |
| Explicar si la variable es cuantitativa o cualitativa | Completo | Notebook indica clasificación binaria. | Se amplió en `reporte_proyecto_02.md`. |
| Justificación de la elección | Completo | Notebook incluye justificación breve. | Se reforzó en README, reporte y antecedentes. |
| Investigación de antecedentes con fuentes confiables | Parcial | No existía antes. | Se creó `antecedentes_borrador.md` con fuentes verificables. |
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
| Métricas de evaluación | Completo en código; pendiente de regenerar | Notebook tiene métricas previas. | Script guarda métricas en `outputs/results/model_results.csv`. |
| Matriz de confusión para clasificación | Completo en código; pendiente de regenerar | Notebook muestra matrices. | Script guarda `confusion_matrix_best.csv` y figura. |
| Gráficas/tablas explicadas | Parcial | Notebook tiene gráficas, pero no exportadas. | Script exporta figuras; reporte explica dónde incluirlas. |
| Script final reproducible | Completo con dependencia de datos | No existía script final. | Se creó `run_project.py`. |
| Documento o reporte final | Parcial | No existía. | Se creó `reporte_proyecto_02.md`; falta convertirlo a Word/PDF final. |
| README con instrucciones | Completo | No existía. | Se creó `README.md`. |
| Evidencia de contribuciones/código | Parcial | Git tiene dos commits previos; no hay control de cambios de documento. | Se documentó pendiente para el equipo. |
| Material Word/PDF final | Faltante | No hay `.docx` ni `.pdf` final del informe. | Se dejó borrador Markdown convertible. |
| Vínculo de repositorio GitHub | Parcial | Repo tiene remoto `origin`. | No se hizo commit ni push por instrucción del usuario. |

## 4. Problemas encontrados

- El dataset `datos_limpios_proyecto1.csv` no está en el repositorio ni en
  carpetas cercanas revisadas; además está ignorado por `.gitignore`.
- El PDF de requisitos no está dentro de la raíz del repo, sino en la carpeta
  padre.
- No existían README, requirements, reporte, antecedentes ni salidas exportadas.
- Las métricas del notebook están guardadas como salidas internas, pero no como
  CSV/Markdown reutilizable.
- El notebook depende de una ruta relativa al CSV limpio; si el archivo no está
  presente, no se puede ejecutar de inicio a fin.
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
- Se creó `README.md` con instrucciones de instalación y ejecución.
- Se creó `requirements.txt`.
- Se creó `antecedentes_borrador.md` con fuentes verificables.
- Se creó `reporte_proyecto_02.md` con la estructura solicitada.
- Se prepararon carpetas `outputs/results/` y `outputs/figures/`.

## 6. Modelos y evaluación

El notebook existente conserva una ejecución previa con estos resultados
principales:

| Modelo | Accuracy test | ROC-AUC | Comentario |
| --- | --- | --- | --- |
| Árbol de Decisión `max_depth=5` | 0.8637 | 0.9056 | Buen desempeño e interpretable. |
| Random Forest `n_estimators=100`, `max_depth=10` | 0.8685 | 0.9256 | Mejor modelo guardado en el notebook. |
| Regresión Logística `C=0.01` | 0.6324 | 0.6869 | Desempeño menor; posible relación no lineal. |

El script nuevo no hardcodea esos resultados: los recalcula al ejecutarse con el
dataset. El ranking final se guarda en `outputs/results/model_results.csv` y el
mejor modelo se selecciona automáticamente.

## 7. Archivos modificados o creados

- `README.md`
- `REVISION_PROYECTO_02.md`
- `.gitignore`
- `antecedentes_borrador.md`
- `reporte_proyecto_02.md`
- `requirements.txt`
- `run_project.py`
- `outputs/figures/.gitkeep`
- `outputs/results/.gitkeep`

No se hizo commit automático.

## 8. Cómo ejecutar el proyecto

Instalar dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Ejecutar con el CSV limpio en la raíz:

```powershell
python run_project.py --data datos_limpios_proyecto1.csv
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

- Recuperar o colocar `datos_limpios_proyecto1.csv` para regenerar resultados
  actuales.
- Ejecutar `python run_project.py --data datos_limpios_proyecto1.csv`.
- Revisar las tablas y figuras generadas en `outputs/`.
- Integrar `antecedentes_borrador.md` y `reporte_proyecto_02.md` en el documento
  final Word/PDF solicitado por el curso.
- Asegurar que el documento Word o Google Docs muestre contribuciones de todos
  los integrantes.
- Agregar al informe final las tablas y gráficas generadas por el script, con
  explicación textual de cada una.
