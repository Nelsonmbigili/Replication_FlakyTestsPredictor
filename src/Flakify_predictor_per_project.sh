#Flakify's flaky test prediction using cross-validation
dataset=$1
data_path="../dataset"
replication_results_path="../replication_results"
dataset_file="${data_path}/${dataset}/Flakify_${dataset}_dataset.csv" 
model_weights="${results_path}/Replication_per_project_weights_on_${dataset}_dataset.pt"
results_file="${results_path}/Replication_per_project_results_on_${dataset}_dataset.csv"

python3 Flakify_predictor_per_project.py $dataset_file $model_weights $results_file