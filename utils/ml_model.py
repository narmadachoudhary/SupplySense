import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def prepare_ml_data(supplier_risk):
    data = supplier_risk.copy()

    features = [
        "on_time_rate",
        "average_delay_days",
        "defect_rate",
        "total_shipments",
        "total_orders"
    ]

    X = data[features]

    y = data["risk_category"].astype(str)

    return X, y


def train_supplier_risk_model(supplier_risk):
    X, y = prepare_ml_data(supplier_risk)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    return model, round(accuracy * 100, 2)


def predict_supplier_risk(model, supplier_data):
    features = [
        "on_time_rate",
        "average_delay_days",
        "defect_rate",
        "total_shipments",
        "total_orders"
    ]

    prediction = model.predict(
        supplier_data[features]
    )

    return prediction      