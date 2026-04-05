
DATA_PATH="../dataset/FlakyCat/flakycat_input.csv"
WEIGHTS_PATH="../replication_results/Replication_cross_validation_weights_on_FlakeFlagger_dataset.pt"
RESULTS_PATH="../replication_results/FlakyCatPredictionsUsingFlakeFlaggerWeights"

echo "Starting Flakify with FlakeFlagger Trained Weights"
python3 Flakify_Predict_FlakyCat.py "$DATA_PATH" "$WEIGHTS_PATH" "$RESULTS_PATH"

WEIGHTS_PATH="../replication_results/Replication_cross_validation_weights_on_IDoFT_dataset.pt"
RESULTS_PATH="../replication_results/FlakyCatPredictionsUsingIDoFTWeights"

echo "Starting Flakify with IDoFT Trained Weights"
python3 Flakify_Predict_FlakyCat.py "$DATA_PATH" "$WEIGHTS_PATH" "$RESULTS_PATH"