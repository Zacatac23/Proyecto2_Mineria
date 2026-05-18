"""Flujo reproducible para el Proyecto 02 de Mineria de Datos.

Este script carga el dataset de defunciones, prepara la variable respuesta
`asis_med_bin`, entrena tres familias de modelos de clasificacion y guarda
metricas, tablas y figuras en `outputs/`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


RANDOM_STATE = 42
TEST_SIZE = 0.30
TARGET = "asis_med_bin"
DEFAULT_DATA = "datos_limpios_proyecto1.csv"

OUTPUT_DIR = Path("outputs")
FIGURES_DIR = OUTPUT_DIR / "figures"
RESULTS_DIR = OUTPUT_DIR / "results"

CLASS_LABELS = {
    0: "Sin asistencia",
    1: "Con asistencia",
}


def normalize_text(value: object) -> object:
    """Normaliza texto para reducir variantes por tildes, espacios y mayusculas."""
    if pd.isna(value):
        return np.nan
    if not isinstance(value, str):
        return value
    normalized = unicodedata.normalize("NFD", value)
    without_accents = "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    )
    return without_accents.upper().strip()


def normalize_column_name(column: object) -> str:
    text = normalize_text(str(column))
    text = str(text).lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def read_tabular_file(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)

    encodings = ["utf-8", "latin-1", "cp1252"]
    last_error: Exception | None = None
    for encoding in encodings:
        try:
            return pd.read_csv(path, encoding=encoding, low_memory=False)
        except UnicodeDecodeError as error:
            last_error = error
    raise RuntimeError(f"No se pudo leer {path} con las codificaciones esperadas") from last_error


def resolve_input_files(data_path: Path, data_dir: Path | None) -> list[Path]:
    if data_path.exists():
        return [data_path]

    if data_dir is not None and data_dir.exists():
        files: list[Path] = []
        for pattern in ("*.csv", "*.xlsx", "*.xls"):
            files.extend(sorted(data_dir.rglob(pattern)))
        if files:
            return files

    message = (
        "No se encontro el dataset. Coloque el archivo "
        f"`{DEFAULT_DATA}` en la raiz del repositorio o ejecute con "
        "`--data ruta/al/archivo.csv`. Tambien puede usar `--data-dir data/raw` "
        "si cuenta con varios CSV/XLSX originales para concatenar."
    )
    raise FileNotFoundError(message)


def load_dataset(data_path: Path, data_dir: Path | None) -> tuple[pd.DataFrame, list[Path]]:
    files = resolve_input_files(data_path, data_dir)
    frames: list[pd.DataFrame] = []

    for file_path in files:
        frame = read_tabular_file(file_path)
        frame["source_file"] = file_path.name
        frames.append(frame)

    data = pd.concat(frames, ignore_index=True) if len(frames) > 1 else frames[0]
    data.columns = [normalize_column_name(column) for column in data.columns]
    return data, files


def clean_dataset(data: pd.DataFrame) -> pd.DataFrame:
    cleaned = data.copy()

    for column in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[column] = cleaned[column].map(normalize_text)

    for column in ["anoreg", "mesreg", "diaocu", "edadif", "edad_anios"]:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    if "edad_anios" not in cleaned.columns and {"edadif", "perdif"}.issubset(cleaned.columns):
        cleaned["edad_anios"] = cleaned.apply(age_to_years, axis=1)

    if "causa_capitulo" not in cleaned.columns and "caudef" in cleaned.columns:
        cleaned["causa_capitulo"] = cleaned["caudef"].astype("string").str[:1]

    if "edad_anios" in cleaned.columns:
        valid_age = cleaned["edad_anios"].isna() | cleaned["edad_anios"].between(0, 115)
        cleaned = cleaned.loc[valid_age].copy()

    if TARGET not in cleaned.columns:
        if "asist" not in cleaned.columns:
            raise KeyError(
                "No se encontro `asist` ni `asis_med_bin`; no se puede crear la variable respuesta."
            )
        cleaned[TARGET] = cleaned["asist"].map(encode_assistance)
    else:
        cleaned[TARGET] = pd.to_numeric(cleaned[TARGET], errors="coerce")

    return cleaned


def age_to_years(row: pd.Series) -> float:
    period = normalize_text(row.get("perdif", ""))
    age = row.get("edadif", np.nan)
    if pd.isna(age):
        return np.nan
    if "ANO" in str(period):
        return float(age)
    if "MES" in str(period):
        return float(age) / 12
    if "DIA" in str(period):
        return float(age) / 365
    if "HORA" in str(period):
        return float(age) / 8760
    return np.nan


def encode_assistance(value: object) -> float:
    assisted_categories = {"MEDICA", "PARAMEDICA", "EMPIRICA", "COMADRONA"}
    no_assistance_categories = {"NINGUNA"}
    normalized = normalize_text(value)
    if pd.isna(normalized):
        return np.nan
    if str(normalized) in assisted_categories:
        return 1.0
    if str(normalized) in no_assistance_categories:
        return 0.0
    return np.nan


def select_features(data: pd.DataFrame, max_null_ratio: float = 0.60) -> tuple[list[str], list[str]]:
    categorical_candidates = [
        "sexo",
        "areag",
        "depocu",
        "depreg",
        "ocur",
        "causa_capitulo",
        "perdif",
        "mesreg",
    ]
    numeric_candidates = ["edad_anios", "anoreg"]

    categorical_features = [
        column
        for column in categorical_candidates
        if column in data.columns and data[column].isna().mean() <= max_null_ratio
    ]
    numeric_features = [
        column
        for column in numeric_candidates
        if column in data.columns and data[column].isna().mean() <= max_null_ratio
    ]

    if not categorical_features and not numeric_features:
        raise RuntimeError("No se encontraron variables predictoras con suficientes datos.")

    return numeric_features, categorical_features


def build_preprocessor(numeric_features: list[str], categorical_features: list[str]) -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="DESCONOCIDO")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
        ]
    )

    transformers = []
    if numeric_features:
        transformers.append(("numeric", numeric_pipeline, numeric_features))
    if categorical_features:
        transformers.append(("categorical", categorical_pipeline, categorical_features))

    return ColumnTransformer(transformers=transformers)


def model_specs() -> list[dict[str, object]]:
    return [
        {
            "algorithm": "Arbol de Decision",
            "model_name": "Arbol depth=3",
            "params": {"max_depth": 3},
            "estimator": DecisionTreeClassifier(
                max_depth=3,
                random_state=RANDOM_STATE,
                class_weight="balanced",
            ),
        },
        {
            "algorithm": "Arbol de Decision",
            "model_name": "Arbol depth=5",
            "params": {"max_depth": 5},
            "estimator": DecisionTreeClassifier(
                max_depth=5,
                random_state=RANDOM_STATE,
                class_weight="balanced",
            ),
        },
        {
            "algorithm": "Arbol de Decision",
            "model_name": "Arbol depth=10",
            "params": {"max_depth": 10},
            "estimator": DecisionTreeClassifier(
                max_depth=10,
                random_state=RANDOM_STATE,
                class_weight="balanced",
            ),
        },
        {
            "algorithm": "Random Forest",
            "model_name": "RF n=100 depth=5",
            "params": {"n_estimators": 100, "max_depth": 5},
            "estimator": RandomForestClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=RANDOM_STATE,
                class_weight="balanced",
                n_jobs=-1,
            ),
        },
        {
            "algorithm": "Random Forest",
            "model_name": "RF n=100 depth=10",
            "params": {"n_estimators": 100, "max_depth": 10},
            "estimator": RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=RANDOM_STATE,
                class_weight="balanced",
                n_jobs=-1,
            ),
        },
        {
            "algorithm": "Random Forest",
            "model_name": "RF n=200 depth=10",
            "params": {"n_estimators": 200, "max_depth": 10},
            "estimator": RandomForestClassifier(
                n_estimators=200,
                max_depth=10,
                random_state=RANDOM_STATE,
                class_weight="balanced",
                n_jobs=-1,
            ),
        },
        {
            "algorithm": "Regresion Logistica",
            "model_name": "Logistica C=0.01",
            "params": {"C": 0.01},
            "estimator": LogisticRegression(
                C=0.01,
                max_iter=1000,
                random_state=RANDOM_STATE,
                class_weight="balanced",
            ),
        },
        {
            "algorithm": "Regresion Logistica",
            "model_name": "Logistica C=1",
            "params": {"C": 1},
            "estimator": LogisticRegression(
                C=1,
                max_iter=1000,
                random_state=RANDOM_STATE,
                class_weight="balanced",
            ),
        },
        {
            "algorithm": "Regresion Logistica",
            "model_name": "Logistica C=10",
            "params": {"C": 10},
            "estimator": LogisticRegression(
                C=10,
                max_iter=1000,
                random_state=RANDOM_STATE,
                class_weight="balanced",
            ),
        },
    ]


def evaluate_pipeline(
    pipeline: Pipeline,
    algorithm: str,
    model_name: str,
    params: dict[str, object],
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> tuple[dict[str, object], np.ndarray, np.ndarray | None]:
    pipeline.fit(X_train, y_train)

    train_pred = pipeline.predict(X_train)
    test_pred = pipeline.predict(X_test)
    test_prob = (
        pipeline.predict_proba(X_test)[:, 1]
        if hasattr(pipeline.named_steps["model"], "predict_proba")
        else None
    )

    train_accuracy = accuracy_score(y_train, train_pred)
    test_accuracy = accuracy_score(y_test, test_pred)

    metrics: dict[str, object] = {
        "algorithm": algorithm,
        "model": model_name,
        "params": json.dumps(params, ensure_ascii=False),
        "train_accuracy": train_accuracy,
        "test_accuracy": test_accuracy,
        "test_balanced_accuracy": balanced_accuracy_score(y_test, test_pred),
        "test_precision": precision_score(y_test, test_pred, zero_division=0),
        "test_recall": recall_score(y_test, test_pred, zero_division=0),
        "test_f1": f1_score(y_test, test_pred, zero_division=0),
        "train_test_accuracy_gap": train_accuracy - test_accuracy,
    }

    if test_prob is not None and y_test.nunique() == 2:
        metrics["test_roc_auc"] = roc_auc_score(y_test, test_prob)
    else:
        metrics["test_roc_auc"] = np.nan

    return metrics, test_pred, test_prob


def class_balance(partitions: dict[str, pd.Series]) -> pd.DataFrame:
    rows = []
    for partition, values in partitions.items():
        counts = values.value_counts(dropna=False).sort_index()
        total = len(values)
        for class_value, count in counts.items():
            rows.append(
                {
                    "partition": partition,
                    "class": int(class_value),
                    "label": CLASS_LABELS.get(int(class_value), str(class_value)),
                    "count": int(count),
                    "percentage": count / total if total else np.nan,
                }
            )
    return pd.DataFrame(rows)


def dataframe_to_markdown(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_Sin filas._\n"

    string_frame = frame.copy()
    for column in string_frame.columns:
        string_frame[column] = string_frame[column].map(format_markdown_value)

    headers = list(string_frame.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in string_frame.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in headers) + " |")
    return "\n".join(lines) + "\n"


def format_markdown_value(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value).replace("\n", " ")


def save_target_distribution(y: pd.Series) -> None:
    counts = y.value_counts().reindex([0, 1], fill_value=0)
    labels = [CLASS_LABELS[0], CLASS_LABELS[1]]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(labels, counts.values, color=["#4C78A8", "#F58518"])
    ax.set_title("Distribucion de la variable respuesta")
    ax.set_xlabel("Clase")
    ax.set_ylabel("Registros")
    for index, value in enumerate(counts.values):
        ax.text(index, value, f"{value:,}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "target_distribution.png", bbox_inches="tight")
    plt.close(fig)


def save_confusion_matrix(y_test: pd.Series, y_pred: np.ndarray, model_name: str) -> pd.DataFrame:
    matrix = confusion_matrix(y_test, y_pred, labels=[0, 1])
    matrix_frame = pd.DataFrame(
        matrix,
        index=["real_sin_asistencia", "real_con_asistencia"],
        columns=["pred_sin_asistencia", "pred_con_asistencia"],
    )
    matrix_frame.to_csv(RESULTS_DIR / "confusion_matrix_best.csv")

    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=[CLASS_LABELS[0], CLASS_LABELS[1]],
    ).plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title(f"Matriz de confusion - {model_name}")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "confusion_matrix_best.png", bbox_inches="tight")
    plt.close(fig)
    return matrix_frame


def save_model_comparison(results: pd.DataFrame) -> None:
    metric = "test_roc_auc" if results["test_roc_auc"].notna().any() else "test_f1"
    plot_frame = results.sort_values(metric, ascending=False).copy()
    colors = {
        "Arbol de Decision": "#4C78A8",
        "Random Forest": "#54A24B",
        "Regresion Logistica": "#F58518",
    }

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(
        plot_frame["model"],
        plot_frame[metric],
        color=[colors.get(algorithm, "#777777") for algorithm in plot_frame["algorithm"]],
    )
    ax.invert_yaxis()
    ax.set_title(f"Comparacion de modelos por {metric}")
    ax.set_xlabel(metric)
    ax.set_ylabel("Modelo")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "model_comparison.png", bbox_inches="tight")
    plt.close(fig)


def save_feature_importance(best_pipeline: Pipeline) -> None:
    estimator = best_pipeline.named_steps["model"]
    preprocessor = best_pipeline.named_steps["preprocess"]

    try:
        feature_names = preprocessor.get_feature_names_out()
    except Exception:
        return

    values: np.ndarray | None = None
    if hasattr(estimator, "feature_importances_"):
        values = estimator.feature_importances_
    elif hasattr(estimator, "coef_"):
        values = np.abs(estimator.coef_[0])

    if values is None:
        return

    importance = (
        pd.DataFrame({"feature": feature_names, "importance": values})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )
    importance.to_csv(RESULTS_DIR / "feature_importance_best.csv", index=False)

    top = importance.head(20).sort_values("importance")
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(top["feature"], top["importance"], color="#4C78A8")
    ax.set_title("Importancia de variables del mejor modelo")
    ax.set_xlabel("Importancia")
    ax.set_ylabel("Variable codificada")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "feature_importance_best.png", bbox_inches="tight")
    plt.close(fig)


def write_run_summary(
    *,
    input_files: Iterable[Path],
    numeric_features: list[str],
    categorical_features: list[str],
    results: pd.DataFrame,
    best_row: pd.Series,
    total_rows: int,
    model_rows: int,
) -> None:
    summary = [
        "# Resumen de ejecucion",
        "",
        f"- Fecha de ejecucion: {datetime.now().isoformat(timespec='seconds')}",
        f"- Archivos de entrada: {', '.join(str(path) for path in input_files)}",
        f"- Registros despues de limpieza: {total_rows:,}",
        f"- Registros usados para modelado: {model_rows:,}",
        f"- Variable respuesta: `{TARGET}`",
        f"- Division train/test: {int((1 - TEST_SIZE) * 100)}/{int(TEST_SIZE * 100)} con estratificacion",
        f"- Variables numericas: {', '.join(numeric_features) if numeric_features else 'ninguna'}",
        f"- Variables categoricas: {', '.join(categorical_features) if categorical_features else 'ninguna'}",
        "",
        "## Mejor modelo",
        "",
        f"- Modelo: {best_row['model']}",
        f"- Algoritmo: {best_row['algorithm']}",
        f"- Parametros: {best_row['params']}",
        f"- Accuracy prueba: {best_row['test_accuracy']:.4f}",
        f"- Precision prueba: {best_row['test_precision']:.4f}",
        f"- Recall prueba: {best_row['test_recall']:.4f}",
        f"- F1 prueba: {best_row['test_f1']:.4f}",
        f"- ROC-AUC prueba: {best_row['test_roc_auc']:.4f}",
        "",
        "## Ranking de modelos",
        "",
        dataframe_to_markdown(results),
    ]
    (RESULTS_DIR / "summary.md").write_text("\n".join(summary), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Entrena y evalua modelos para el Proyecto 02 de Mineria de Datos."
    )
    parser.add_argument(
        "--data",
        default=DEFAULT_DATA,
        help=f"Ruta del CSV/XLSX limpio. Por defecto: {DEFAULT_DATA}",
    )
    parser.add_argument(
        "--data-dir",
        default=None,
        help="Carpeta con CSV/XLSX originales para concatenar si --data no existe.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    data_path = Path(args.data)
    data_dir = Path(args.data_dir) if args.data_dir else None

    raw_data, input_files = load_dataset(data_path, data_dir)
    cleaned = clean_dataset(raw_data)
    numeric_features, categorical_features = select_features(cleaned)

    features = numeric_features + categorical_features
    model_data = cleaned[features + [TARGET]].dropna(subset=[TARGET]).copy()
    model_data[TARGET] = model_data[TARGET].astype(int)

    if model_data[TARGET].nunique() != 2:
        raise RuntimeError("La variable respuesta debe tener exactamente dos clases para este flujo.")

    for column in categorical_features:
        model_data[column] = model_data[column].astype(object)
        model_data[column] = model_data[column].where(model_data[column].notna(), np.nan)

    X = model_data[features]
    y = model_data[TARGET]

    save_target_distribution(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    balance = class_balance({"all": y, "train": y_train, "test": y_test})
    balance.to_csv(RESULTS_DIR / "class_balance.csv", index=False)
    (RESULTS_DIR / "class_balance.md").write_text(
        dataframe_to_markdown(balance), encoding="utf-8"
    )

    results: list[dict[str, object]] = []
    fitted_models: dict[str, Pipeline] = {}
    predictions: dict[str, np.ndarray] = {}

    for spec in model_specs():
        pipeline = Pipeline(
            steps=[
                ("preprocess", build_preprocessor(numeric_features, categorical_features)),
                ("model", spec["estimator"]),
            ]
        )
        metrics, y_pred, _ = evaluate_pipeline(
            pipeline=pipeline,
            algorithm=str(spec["algorithm"]),
            model_name=str(spec["model_name"]),
            params=dict(spec["params"]),
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
        )
        results.append(metrics)
        fitted_models[str(spec["model_name"])] = pipeline
        predictions[str(spec["model_name"])] = y_pred

    results_frame = pd.DataFrame(results)
    results_frame = results_frame.sort_values(
        ["test_roc_auc", "test_f1", "test_accuracy"],
        ascending=False,
        na_position="last",
    ).reset_index(drop=True)

    metric_columns = [
        "train_accuracy",
        "test_accuracy",
        "test_balanced_accuracy",
        "test_precision",
        "test_recall",
        "test_f1",
        "train_test_accuracy_gap",
        "test_roc_auc",
    ]
    results_frame[metric_columns] = results_frame[metric_columns].round(4)

    results_frame.to_csv(RESULTS_DIR / "model_results.csv", index=False)
    (RESULTS_DIR / "model_results.md").write_text(
        dataframe_to_markdown(results_frame), encoding="utf-8"
    )

    best_row = results_frame.iloc[0]
    best_model_name = str(best_row["model"])
    best_pipeline = fitted_models[best_model_name]
    best_pred = predictions[best_model_name]

    save_confusion_matrix(y_test, best_pred, best_model_name)
    save_model_comparison(results_frame)
    save_feature_importance(best_pipeline)

    report = classification_report(
        y_test,
        best_pred,
        target_names=[CLASS_LABELS[0], CLASS_LABELS[1]],
        output_dict=True,
        zero_division=0,
    )
    pd.DataFrame(report).transpose().to_csv(RESULTS_DIR / "classification_report_best.csv")

    write_run_summary(
        input_files=input_files,
        numeric_features=numeric_features,
        categorical_features=categorical_features,
        results=results_frame,
        best_row=best_row,
        total_rows=len(cleaned),
        model_rows=len(model_data),
    )

    print("Proyecto 02 ejecutado correctamente.")
    print(f"Mejor modelo: {best_model_name}")
    print(f"Resultados: {RESULTS_DIR}")
    print(f"Figuras: {FIGURES_DIR}")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, KeyError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
