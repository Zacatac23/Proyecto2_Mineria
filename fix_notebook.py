"""
fix_notebook.py  –  Corrige todos los errores detectados en
Proyecto2_Defunciones_Guatemala.ipynb y guarda el resultado.
"""

import json, copy, re

NB_PATH = "Proyecto2_Defunciones_Guatemala.ipynb"

with open(NB_PATH, encoding="utf-8") as f:
    nb = json.load(f)


def set_source(cell, lines):
    """Reemplaza el source de una celda con una lista de líneas."""
    cell["source"] = lines
    cell["outputs"] = []
    cell["execution_count"] = None


# ── Índice de celdas de código (0-based entre todas las celdas) ─────────────
code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]

# Identificamos celdas por su id para ser precisos
cell_by_id = {c["id"]: c for c in nb["cells"]}

# ═══════════════════════════════════════════════════════════════════════════
# FIX 1 – Celda cf3852a8  (Limpieza y transformación)
#   • "ANO" in p or "ANO" in p  →  "ANO" in p or "AÑO" in p
# ═══════════════════════════════════════════════════════════════════════════
cell = cell_by_id["cf3852a8"]
new_source = [
    "import unicodedata\n",
    "\n",
    "def quitar_tildes(s):\n",
    "    if not isinstance(s, str):\n",
    "        return s\n",
    "    return \"\".join(c for c in unicodedata.normalize(\"NFD\", s)\n",
    "                   if unicodedata.category(c) != \"Mn\")\n",
    "\n",
    "# Estandarizar texto — todo en una lambda, sin .str.upper() sobre NaN\n",
    "for col in datos_raw.select_dtypes(include=\"object\").columns:\n",
    "    datos_raw[col] = datos_raw[col].apply(\n",
    "        lambda x: quitar_tildes(x).upper().strip() if isinstance(x, str) else x\n",
    "    )\n",
    "\n",
    "# Convertir numéricas\n",
    "for col in [\"anoreg\", \"mesreg\", \"diaocu\", \"edadif\"]:\n",
    "    if col in datos_raw.columns:\n",
    "        datos_raw[col] = pd.to_numeric(datos_raw[col], errors=\"coerce\")\n",
    "\n",
    "# Edad en años (solo si no viene ya calculada del CSV limpio)\n",
    "if \"edad_anios\" not in datos_raw.columns:\n",
    "    def edad_en_anios(row):\n",
    "        p = str(row.get(\"perdif\", \"\")).upper()\n",
    "        e = row.get(\"edadif\", float(\"nan\"))\n",
    "        if pd.isna(e):\n",
    "            return float(\"nan\")\n",
    "        if \"ANO\" in p or \"AÑO\" in p:   # FIX: segunda condición era duplicado\n",
    "            return e\n",
    "        if \"MES\" in p:\n",
    "            return e / 12\n",
    "        if \"DIA\" in p:\n",
    "            return e / 365\n",
    "        if \"HORA\" in p:\n",
    "            return e / 8760\n",
    "        return float(\"nan\")\n",
    "    datos_raw[\"edad_anios\"] = datos_raw.apply(edad_en_anios, axis=1)\n",
    "\n",
    "# Capítulo CIE-10 (solo si no viene del CSV limpio)\n",
    "if \"causa_capitulo\" not in datos_raw.columns and \"caudef\" in datos_raw.columns:\n",
    "    datos_raw[\"causa_capitulo\"] = datos_raw[\"caudef\"].str[:1]\n",
    "\n",
    "# Filtrar edades imposibles\n",
    "datos = datos_raw[datos_raw[\"edad_anios\"].isna() | (datos_raw[\"edad_anios\"] <= 115)].copy()\n",
    "print(f\"Registros tras limpieza: {len(datos):,}\")\n",
    "print(f\"Columnas disponibles: {datos.columns.tolist()}\")\n",
]
cell["source"] = new_source
cell["outputs"] = []
cell["execution_count"] = None

# ═══════════════════════════════════════════════════════════════════════════
# FIX 2 – Celda 966e5bdf  (Variable respuesta / binarización)
#   • Tenía SyntaxError por f-string sin cerrar en versión anterior.
#   • La versión actual del notebook ya está corregida en source, pero
#     limpiamos el output de error que quedó registrado.
# ═══════════════════════════════════════════════════════════════════════════
cell = cell_by_id["966e5bdf"]
# El source actual ya es correcto; solo limpiamos el output de error previo
cell["outputs"] = []
cell["execution_count"] = None

# ═══════════════════════════════════════════════════════════════════════════
# FIX 3 – Celda 4657c707  (Features)
#   • candidatas_cat incluye 'area', 'area_geo', 'lugar_ocu' que NO existen
#     en el dataset (columna real es 'areag', 'ocur').
#     El código ya filtra con `if c in datos.columns`, pero queda lista vacía.
#     Añadimos 'areag' a las candidatas para que sí se incluya.
# ═══════════════════════════════════════════════════════════════════════════
cell = cell_by_id["4657c707"]
cell["source"] = [
    "# Variables predictoras disponibles\n",
    "FEATURES_CAT = []\n",
    "FEATURES_NUM = []\n",
    "\n",
    "# Columnas reales del dataset de defunciones Guatemala\n",
    "candidatas_cat = ['sexo', 'areag', 'depocu', 'depreg',\n",
    "                  'ocur', 'causa_capitulo', 'mesreg']\n",
    "candidatas_num = ['edad_anios', 'anoreg']\n",
    "\n",
    "for c in candidatas_cat:\n",
    "    if c in datos.columns:\n",
    "        FEATURES_CAT.append(c)\n",
    "\n",
    "for c in candidatas_num:\n",
    "    if c in datos.columns:\n",
    "        FEATURES_NUM.append(c)\n",
    "\n",
    "print(\"Variables categóricas a usar:\", FEATURES_CAT)\n",
    "print(\"Variables numéricas a usar  :\", FEATURES_NUM)\n",
    "\n",
    "if not FEATURES_CAT and not FEATURES_NUM:\n",
    "    raise RuntimeError(\"No se encontraron features válidas. Verifica los nombres de columnas.\")\n",
]
cell["outputs"] = []
cell["execution_count"] = None

# ═══════════════════════════════════════════════════════════════════════════
# FIX 4 – Celda 241fe089  (Construcción df_model)
#   • Si FEATURES_NUM está vacío, scaler.fit_transform falla con array vacío.
#     Añadimos guarda para ese caso.
# ═══════════════════════════════════════════════════════════════════════════
cell = cell_by_id["241fe089"]
cell["source"] = [
    "# Construir dataframe de modelado\n",
    "FEATURES = FEATURES_NUM + FEATURES_CAT\n",
    "TARGET   = 'asis_med_bin'\n",
    "\n",
    "df_model = datos[FEATURES + [TARGET]].dropna().copy()\n",
    "print(f\"Registros para modelado: {len(df_model):,}\")\n",
    "\n",
    "# Codificar variables categóricas con LabelEncoder\n",
    "le_dict = {}\n",
    "for col in FEATURES_CAT:\n",
    "    le = LabelEncoder()\n",
    "    df_model[col] = le.fit_transform(df_model[col].astype(str))\n",
    "    le_dict[col] = le\n",
    "\n",
    "# Escalar numéricas (para Regresión Logística)\n",
    "scaler = StandardScaler()\n",
    "df_model_scaled = df_model.copy()\n",
    "if FEATURES_NUM:\n",
    "    df_model_scaled[FEATURES_NUM] = scaler.fit_transform(df_model[FEATURES_NUM])\n",
    "\n",
    "X    = df_model[FEATURES].values\n",
    "y    = df_model[TARGET].values.astype(int)\n",
    "X_sc = df_model_scaled[FEATURES].values\n",
    "\n",
    "print(f\"\\nShape X: {X.shape} | Shape y: {y.shape}\")\n",
    "print(f\"Balance → Clase 1: {y.mean()*100:.1f}% | Clase 0: {(1-y.mean())*100:.1f}%\")\n",
]
cell["outputs"] = []
cell["execution_count"] = None

# ═══════════════════════════════════════════════════════════════════════════
# FIX 5 – Celda 8e91e578  (inspección columna asistencia) – limpiar output
# ═══════════════════════════════════════════════════════════════════════════
cell = cell_by_id["8e91e578"]
cell["outputs"] = []
cell["execution_count"] = None

# ═══════════════════════════════════════════════════════════════════════════
# Guardar el notebook corregido
# ═══════════════════════════════════════════════════════════════════════════
with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("✅ Notebook corregido y guardado:", NB_PATH)
print()
print("Fixes aplicados:")
print("  1. cf3852a8 – edad_en_anios: 'AÑO' en lugar de duplicado 'ANO'")
print("  2. 966e5bdf – output de SyntaxError anterior limpiado")
print("  3. 4657c707 – candidatas_cat corregidas a nombres reales del dataset ('areag')")
print("  4. 241fe089 – guarda para FEATURES_NUM vacío antes del StandardScaler")
print("  5. 8e91e578 – output de KeyError anterior limpiado")
