import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report

import joblib


file_path = r'C:\Users\filip\Desktop\S4_DTA\Memgraph_ML\invoice_with_fraud2.csv'  # Remplacez ce chemin par le chemin vers votre fichier CSV
data = pd.read_csv(file_path)


print(data.head())


data['due_date'] = pd.to_datetime(data['due_date'])
data['due_date'] = data['due_date'].apply(lambda x: x.timestamp())


label_encoder = LabelEncoder()
data['status'] = label_encoder.fit_transform(data['status'])


print(data[['status', 'due_date']].head())

X = data[['total_amount', 'status', 'due_date']]  
y = data['fraud']  



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Ensemble d'entraînement:", X_train.shape)
print("Ensemble de test:", X_test.shape)


# Sauvegarder le modèle

# Convertir les données en format DMatrix pour XGBoost
train_data = xgb.DMatrix(X_train, label=y_train)
test_data = xgb.DMatrix(X_test, label=y_test)

# Définir les paramètres du modèle XGBoost
params = {
    'objective': 'binary:logistic',  # Classification binaire (fraude ou non)
    'eval_metric': 'logloss',  # Logarithmic loss
    'max_depth': 5,  # Profondeur maximale de l'arbre
    'learning_rate': 0.1,  # Taux d'apprentissage
    'n_estimators': 100  # Nombre d'arbres
}

# Entraîner le modèle
model = xgb.train(params, train_data, num_boost_round=100)

# Prédictions sur l'ensemble de test
y_pred = model.predict(test_data)
y_pred = [1 if x > 0.5 else 0 for x in y_pred]  # Convertir les probabilités en classes

# Évaluer le modèle
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

joblib.dump(model, 'fraud_detection_model.pkl')

# Charger le modèle sauvegardé
model = joblib.load('fraud_detection_model.pkl')

# Exemple de nouvelle facture
new_invoice = pd.DataFrame({
    'total_amount': [30000000],
    'status': [label_encoder.transform(['paid'])[0]],  # Encoder le status
    'due_date': [pd.to_datetime('2025-12-31').timestamp()]
})

# Prédire si la facture est frauduleuse
new_data = xgb.DMatrix(new_invoice)
prediction = model.predict(new_data)

# Afficher la prédiction
if prediction[0] > 0.5:
    print("La facture est frauduleuse.")
else:
    print("La facture est légitime.")