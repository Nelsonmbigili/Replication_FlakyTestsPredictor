
DATA_PATH="../replication_results/selected_20_samples.csv"
WEIGHTS_PATH="../replication_results/Replication_cross_validation_weights_on_FlakeFlagger_dataset.pt"
RESULTS_PATH="../replication_results"

echo "Starting Flakify"
python3 Flakify_Predict_FlakyCat.py "$DATA_PATH" "$WEIGHTS_PATH" "$RESULTS_PATH"