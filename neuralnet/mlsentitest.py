import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt


mode = "bin"

# Step 1: Load the saved model and the saved CountVectorizer
model_path = "savedmodel" + mode + "/savedmodel" + mode + ".keras"
model = load_model(model_path)

with open('savedmodel' + mode + '/count_vectorizer.pkl', 'rb') as f:
    vec = pickle.load(f)

# Step 2: Load and preprocess the new dataset
new_dataset_path = "newdatasets/reviewstars" + mode+ ".csv"
new_df = pd.read_csv(new_dataset_path)

# Example: Assume new_df has columns 'reviews' and 'sentiment'
X_new = new_df["reviews"].values
Y_new = new_df["sentiment"].values

# Preprocess the text data using the same CountVectorizer
# vec = CountVectorizer()
# vec.fit(X_new.astype("U"))  # Fit the vectorizer on the new data
x_new = vec.transform(X_new.astype("U"))

if mode == "nonbin":
    Y_new = Y_new + 1  # Adjust if your original labels were -1, 0, 1
    Y_new = to_categorical(Y_new)  # One-hot encode for non-binary classification

# Step 3: Evaluate the model on the new dataset
# No need for one-hot encoding in binary mode

# Make predictions
predictions = model.predict(x_new)

# For binary mode, threshold the predictions at 0.5 to get binary class predictions
if mode == "bin":
    predictions = (predictions > 0.5).astype(int)
    

# Printing new linear plots

# Create a DataFrame for easier plotting
results_df = pd.DataFrame({
    'Review': X_new,
    'Actual': Y_new,
    'Predicted': predictions.flatten()
})

# Sort the DataFrame by actual values (and by review length as a secondary criterion)
results_df = results_df.sort_values(by=['Actual', 'Review'])

# Plotting
plt.figure(figsize=(14, 7))
plt.plot(results_df.index, results_df['Actual'], label='Actual', color='b', linestyle='-', marker='o')
plt.plot(results_df.index, results_df['Predicted'], label='Predicted', color='r', linestyle='-', marker='x')
plt.title('Actual vs Predicted Sentiments')
plt.xlabel('Index')
plt.ylabel('Sentiment')
plt.legend()
plt.show()

##############################################################################################################

# Print actual vs predicted values
for actual, predicted in zip(Y_new, predictions):
    print(f"Actual: {actual}, Predicted: {predicted}")

# Plot actual vs predicted
plt.figure(figsize=(12, 5))

# Scatter plot for actual vs predicted
plt.subplot(1, 2, 1)
plt.scatter(range(len(Y_new)), Y_new, color='blue', label='Actual')
plt.scatter(range(len(predictions)), predictions, color='red', label='Predicted', alpha=0.6)
plt.title('Actual vs Predicted')
plt.xlabel('Sample index')
plt.ylabel('Sentiment')
plt.legend()

# Line plot for actual vs predicted
plt.subplot(1, 2, 2)
plt.plot(range(len(Y_new)), Y_new, color='blue', marker='o', label='Actual')
plt.plot(range(len(predictions)), predictions, color='red', marker='x', label='Predicted', alpha=0.6)
plt.title('Actual vs Predicted')
plt.xlabel('Sample index')
plt.ylabel('Sentiment')
plt.legend()

plt.tight_layout()
plt.show()
  
  
# Step 4: Plot the accuracy and loss 
    
loss, accuracy = model.evaluate(x_new, Y_new, verbose=True)
print(f"Loss: {loss}, Accuracy: {accuracy}")


history_path = "savedmodel" + mode + "/savedmodel" + mode + ".npy"
history = np.load(history_path, allow_pickle=True).item()

plt.figure(figsize=(12, 5))

# Accuracy plot
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
