import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    log_loss, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, confusion_matrix, classification_report
)
import argparse

# Define the command-line arguments
parser = argparse.ArgumentParser(description='Test a sentiment analysis model.')
parser.add_argument('--mode', type=str, required=True, help='Mode of the model: nonbin or bin')
parser.add_argument('--file_name', type=str, required=True, help='Name of the file')
args = parser.parse_args()

# Access the mode arguments
mode = args.mode
file_name = args.file_name

model_path = f"savedmodel{mode}/savedmodel{mode}.keras"
model = load_model(model_path)

with open(f'savedmodel{mode}/count_vectorizer.pkl', 'rb') as f:
    vec = pickle.load(f)

new_dataset_path = f"testdatasets/{file_name}{mode}.csv"
new_df = pd.read_csv(new_dataset_path)
X_new = new_df["reviews"].values
Y_new = new_df["sentiment"].values

x_new = vec.transform(X_new.astype("U"))

if mode == "nonbin":
    Y_new += 1
    Y_new = to_categorical(Y_new) # One-hot encode for non-binary classification

# No need for one-hot encoding in binary mode
probabilities = model.predict(x_new)

if mode == "bin":
    predictions = (probabilities > 0.5).astype(int)

results_df = pd.DataFrame({
    'Review': X_new,
    'Actual': Y_new,
    'Predicted': predictions.flatten()
})

results_df = results_df.sort_values(by=['Actual', 'Review'])

plt.figure(figsize=(10, 6))
plt.scatter(range(len(Y_new)), Y_new, alpha=0.5, label='Actual')
plt.scatter(range(len(Y_new)), predictions, alpha=0.5, label='Predicted', c='r')
plt.title("Actual vs Predicted Sentiment")
plt.xlabel("Samples")
plt.ylabel("Sentiment")
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(Y_new, label='Actual')
plt.plot(predictions, label='Predicted', linestyle='--')
plt.title("Actual vs Predicted Sentiment")
plt.xlabel("Samples")
plt.ylabel("Sentiment")
plt.legend()
plt.show()

# Interpret probabilities and print confidence
# for i, prob in enumerate(probabilities):
#     predicted_sentiment = 'Positive' if prob > 0.5 else 'Negative'
#     confidence = float(prob * 100) if predicted_sentiment == 'Positive' else float((1 - prob) * 100)
#     print(f"Review: {X_new[i]}")
#     print(f"True Sentiment: {Y_new[i]}")
#     print(f"Predicted Sentiment: {predicted_sentiment}")
#     print(f"Confidence: {confidence:.2f}%")
#     print("-" * 50)
    
# Plot confidence scores

plt.figure(figsize=(10, 6))
plt.hist(probabilities, bins=50, alpha=0.75, color='blue', label='Predicted Probabilities')
plt.axvline(0.5, color='red', linestyle='dashed', linewidth=1, label='Threshold = 0.5')
plt.title('Distribution of Predicted Probabilities')
plt.xlabel('Predicted Probability')
plt.ylabel('Frequency')
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(predictions, bins=50, alpha=0.75, color='blue', label='Predicted Probabilities')
plt.axvline(0.5, color='red', linestyle='dashed', linewidth=1, label='Threshold = 0.5')
plt.title('Distribution of Predicted Probabilities')
plt.xlabel('Predicted Probability')
plt.ylabel('Frequency')
plt.legend()
plt.show()

roc_auc = roc_auc_score(Y_new, predictions)
print(f"ROC AUC Score: {roc_auc:.2f}")

correct_predictions = (Y_new == predictions)
weights = np.abs(probabilities - 0.5) * 2
weighted_accuracy = np.sum(correct_predictions * weights) / np.sum(weights)
print(f"Weighted Accuracy: {weighted_accuracy:.2f}")

brier_score = np.mean((probabilities - Y_new) ** 2)
print(f"Brier Score: {brier_score:.4f}")

logloss = log_loss(Y_new, probabilities)
print(f"Log Loss: {logloss:.4f}")

fpr, tpr, thresholds = roc_curve(Y_new, predictions)
plt.plot(fpr, tpr, label=f'Neural Network (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='lower right')
plt.show()

# Print actual vs predicted values
# for actual, predicted in zip(Y_new, predictions):
#     print(f"Actual: {actual}, Predicted: {predicted}")

conf_matrix = confusion_matrix(Y_new, predictions)
print("Confusion Matrix:\n", conf_matrix)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

loss, accuracy = model.evaluate(x_new, Y_new, verbose=True)
print(f"Loss: {loss}, Accuracy: {accuracy}")

precision = precision_score(Y_new, predictions)
recall = recall_score(Y_new, predictions)
f1 = f1_score(Y_new, predictions)

print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1:.2f}")

print("\nClassification Report:\n", classification_report(Y_new, predictions))

metrics_summary = pd.DataFrame({
    'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC AUC', 'Loss'],
    'Value': [accuracy, precision, recall, f1, roc_auc, loss]
})

print("\nSummary of Evaluation Metrics:\n", metrics_summary)

history_path = f"savedmodel{mode}/savedmodel{mode}.npy"
history = np.load(history_path, allow_pickle=True).item()

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history['accuracy'], label='Train Accuracy')
plt.plot(history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='upper left')

plt.subplot(1, 2, 2)
plt.plot(history['loss'], label='Train Loss')
plt.plot(history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(loc='upper left')

plt.tight_layout()
plt.show()
