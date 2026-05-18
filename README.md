# Proyecto 02 - Mineria de Datos

Modelos predictivos sobre registros de defunciones en Guatemala. El objetivo del
proyecto es predecir si una defuncion tuvo asistencia antes del fallecimiento,
usando variables demograficas, territoriales y de contexto disponibles en los
registros.

## Dataset

El notebook existente usa el archivo `datos_limpios_proyecto1.csv`, generado en
el Proyecto 01 a partir de datos de defunciones del INE Guatemala. Ese CSV esta
ignorado por Git en `.gitignore` y no se encontro en esta copia local del repo.

Fuente oficial de referencia:
<https://datos.ine.gob.gt/es/dataset/estadisticas-vitales-defunciones>

Para ejecutar el proyecto, coloque `datos_limpios_proyecto1.csv` en la raiz del
repositorio o pase una ruta con `--data`.

## Variable respuesta

- Variable: `asis_med_bin`
- Origen: columna `asist`
- Tipo: cualitativa binaria
- Clase `1`: `MEDICA`, `PARAMEDICA`, `EMPIRICA`, `COMADRONA`
- Clase `0`: otras categorias registradas, como `NINGUNA` o `IGNORADO`
- Problema: clasificacion binaria

La seleccion se justifica porque permite estudiar brechas de acceso o contacto
con asistencia antes del fallecimiento.

## Algoritmos implementados

El script `run_project.py` entrena al menos tres variaciones de cada algoritmo:

- Arbol de Decision
- Random Forest
- Regresion Logistica

Las metricas calculadas son accuracy, balanced accuracy, precision, recall,
F1-score y ROC-AUC. Tambien se guarda la matriz de confusion del mejor modelo.

## Instalacion

Desde PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecucion

Con el CSV limpio en la raiz:

```powershell
python run_project.py --data datos_limpios_proyecto1.csv
```

Con el CSV en otra ruta:

```powershell
python run_project.py --data ruta\al\datos_limpios_proyecto1.csv
```

Con varios archivos originales en una carpeta:

```powershell
python run_project.py --data-dir data\raw
```

## Salidas generadas

El script crea estas carpetas automaticamente:

- `outputs/results/`
- `outputs/figures/`

Archivos principales esperados:

- `outputs/results/model_results.csv`
- `outputs/results/model_results.md`
- `outputs/results/class_balance.csv`
- `outputs/results/confusion_matrix_best.csv`
- `outputs/results/classification_report_best.csv`
- `outputs/results/feature_importance_best.csv`
- `outputs/results/summary.md`
- `outputs/figures/target_distribution.png`
- `outputs/figures/model_comparison.png`
- `outputs/figures/confusion_matrix_best.png`
- `outputs/figures/feature_importance_best.png`

## Archivos importantes

- `Proyecto2_Defunciones_Guatemala.ipynb`: notebook con el avance original de
  modelado y resultados guardados de una ejecucion previa.
- `run_project.py`: script reproducible de inicio a fin.
- `reporte_proyecto_02.md`: borrador estructurado del informe final.
- `antecedentes_borrador.md`: antecedentes con fuentes verificables en formato
  APA 7.
- `REVISION_PROYECTO_02.md`: revision tecnica contra el PDF del proyecto.
- `requirements.txt`: dependencias de Python.

## Nota sobre resultados

En esta revision no se regeneraron metricas nuevas porque el dataset
`datos_limpios_proyecto1.csv` no esta disponible localmente. El notebook conserva
salidas de una ejecucion previa, pero para la entrega final se recomienda
regenerar todo con `run_project.py` y adjuntar las tablas/figuras producidas.
