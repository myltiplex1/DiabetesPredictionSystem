# models/diabetes_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import streamlit as st
from utils.data_loader import load_data


@st.cache_resource
def train_model():
    df = load_data("diabetes_prediction_dataset.csv")
    X = df.drop("diabetes", axis=1)
    y = df["diabetes"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    gb_classifier = GradientBoostingClassifier(
        n_estimators=100, learning_rate=0.1, max_depth=3
    )
    pipeline = Pipeline([("scaler", StandardScaler()), ("classifier", gb_classifier)])
    pipeline.fit(X_train, y_train)

    return pipeline, X.columns.tolist()
