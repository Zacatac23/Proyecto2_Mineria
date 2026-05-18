# Proyecto 02 - Mineria de Datos

Modelos predictivos sobre registros de defunciones en Guatemala. El objetivo del
proyecto es predecir si una defuncion tuvo asistencia antes del fallecimiento,
usando variables demograficas, territoriales y de contexto disponibles en los
registros.

## Dataset

El proyecto usa el archivo `datos_limpios_proyecto1.csv`, generado en el
Proyecto 01 a partir de datos de defunciones del INE Guatemala. En esta copia
local el CSV real esta en `data/processed/datos_limpios_proyecto1.csv`. El
archivo se mantiene ignorado por Git porque pesa aproximadamente 289 MB.

Fuente oficial de referencia:
<https://datos.ine.gob.gt/es/dataset/estadisticas-vitales-defunciones>

Para ejecutar el proyecto, coloque `datos_limpios_proyecto1.csv` en
`data/processed/` o pase una ruta con `--data`.

## Variable respuesta

- Variable: `asis_med_bin`
- Origen: columna `asist`
- Tipo: cualitativa binaria
- Clase `1`: `MEDICA`, `PARAMEDICA`, `EMPIRICA`, `COMADRONA`
- Clase `0`: `NINGUNA`
- Valores excluidos del modelado: `IGNORADO`, porque no confirma ausencia de
  asistencia sino desconocimiento del dato.
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

## Lenguaje de entrega

El PDF solicita un script de R (`.r` o `.rmd`) o de Python. Por lo tanto, este
repo puede entregarse en Python con `run_project.py` y el notebook
`Proyecto2_Defunciones_Guatemala.ipynb`; no es obligatorio migrarlo a R.

## Estructura del repositorio

- `run_project.py`: script principal reproducible.
- `Proyecto2_Defunciones_Guatemala.ipynb`: notebook original del avance.
- `docs/`: revisión, reporte y antecedentes.
- `data/processed/`: ubicación local del CSV limpio real. No se versionan datos
  pesados.
- `outputs/results/`: tablas generadas al correr el script. Ignorado por Git.
- `outputs/figures/`: figuras generadas al correr el script. Ignorado por Git.
- `fix_notebook.py`: auxiliar histórico para corregir el notebook; no es el
  script final de entrega.

## Instalacion

Desde PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecucion

Con el CSV real que esta actualmente en `data/processed/`:

```powershell
python run_project.py
```

Equivalente con ruta explicita:

```powershell
python run_project.py --data data\processed\datos_limpios_proyecto1.csv
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

El script crea estas carpetas automaticamente. Su contenido se ignora en Git
para evitar versionar resultados y PNG generados en cada corrida:

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
- `docs/reporte_proyecto_02.md`: borrador estructurado del informe final.
- `docs/antecedentes_borrador.md`: antecedentes con fuentes verificables en formato
  APA 7.
- `docs/REVISION_PROYECTO_02.md`: revision tecnica contra el PDF del proyecto.
- `requirements.txt`: dependencias de Python.

## Resultados reproducidos con el CSV real

La ejecucion con `data/processed/datos_limpios_proyecto1.csv` genero 799,810 registros
para modelado despues de excluir `IGNORADO` en la variable respuesta. Las clases
quedaron balanceadas: 49.7% sin asistencia y 50.3% con asistencia.

Con ROC-AUC como criterio principal, el mejor modelo reproducido fue
Regresion Logistica `C=10` con accuracy de prueba 0.8703, F1 0.8627 y ROC-AUC
0.9280. Si se prioriza accuracy o F1 en la clase positiva, el Arbol de Decision
`max_depth=10` queda muy competitivo y debe discutirse en el informe.
