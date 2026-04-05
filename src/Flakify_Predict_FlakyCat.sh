
DATA_PATH="../dataset/FlakyCat/flakycat_input.csv" # To run flakify on a sample of flakycat dataset 
# DATA_PATH="../dataset/FlakeFlagger/FlakeFlagger_sample_input_of_20.csv" ## To run flakify on a sample of FlakeFlagger dataset or other change path
WEIGHTS_PATH="../replication_results/Replication_cross_validation_weights_on_FlakeFlagger_dataset.pt"
RESULTS_PATH="../replication_results/FlakyCatPredictionsUsingFlakeFlaggerWeights" ## To run flakify on a sample of FlakeFlagger dataset or other change path

echo "Starting Flakify with FlakeFlagger Trained Weights"
python3 Flakify_Predict_FlakyCat.py "$DATA_PATH" "$WEIGHTS_PATH" "$RESULTS_PATH"

WEIGHTS_PATH="../replication_results/Replication_cross_validation_weights_on_IDoFT_dataset.pt"
RESULTS_PATH="../replication_results/FlakyCatPredictionsUsingIDoFTWeights"  ## To run flakify on a sample of FlakeFlagger dataset or other change path

echo "Starting Flakify with IDoFT Trained Weights"
python3 Flakify_Predict_FlakyCat.py "$DATA_PATH" "$WEIGHTS_PATH" "$RESULTS_PATH"