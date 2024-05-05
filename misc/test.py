import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import roc_auc_score

# Define a simple autoencoder for outlier detection
class Autoencoder(nn.Module):
    def __init__(self, input_dim):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, input_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

# Assuming X_train, y_train are your training data
# Assuming X_test, y_test are your test data

# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train).float()
X_test_tensor = torch.tensor(X_test).float()

# Step 1: Train an autoencoder for outlier detection
autoencoder = Autoencoder(input_dim=X_train_tensor.shape[1])

criterion = nn.MSELoss()
optimizer = optim.Adam(autoencoder.parameters(), lr=0.001)

epochs = 10
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = autoencoder(X_train_tensor)
    loss = criterion(outputs, X_train_tensor)
    loss.backward()
    optimizer.step()

# Step 2: Use reconstruction error as outlier scores
with torch.no_grad():
    X_train_reconstructed = autoencoder(X_train_tensor)
    X_test_reconstructed = autoencoder(X_test_tensor)
    reconstruction_errors_train = torch.mean((X_train_tensor - X_train_reconstructed)**2, dim=1)
    reconstruction_errors_test = torch.mean((X_test_tensor - X_test_reconstructed)**2, dim=1)

# Step 3: Train a classifier on the combined feature set (original features + reconstruction errors)
X_train_combined = torch.cat((X_train_tensor, reconstruction_errors_train.unsqueeze(1)), dim=1)
X_test_combined = torch.cat((X_test_tensor, reconstruction_errors_test.unsqueeze(1)), dim=1)

input_dim_combined = X_train_combined.shape[1]
classifier = Classifier(input_dim_combined)

criterion_classifier = nn.BCELoss()
optimizer_classifier = optim.Adam(classifier.parameters(), lr=0.001)

epochs_classifier = 10
for epoch in range(epochs_classifier):
    optimizer_classifier.zero_grad()
    outputs_classifier = classifier(X_train_combined)
    loss_classifier = criterion_classifier(outputs_classifier, y_train.view(-1, 1).float())
    loss_classifier.backward()
    optimizer_classifier.step()

# Step 4: Evaluate the classifier on the test set
classifier.eval()
with torch.no_grad():
    outputs_test = classifier(X_test_combined)
    y_pred_test = (outputs_test > 0.5).float()

auc_score_test = roc_auc_score(y_test, y_pred_test)
print("AUC Score on Test Set:", auc_score_test)
