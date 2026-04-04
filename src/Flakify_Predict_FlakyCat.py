import sys
import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel, AutoConfig

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
print(f"PyTorch version: {torch.__version__}")

if len(sys.argv) < 4:
    print("Usage: python3 Flakify_Predict_FlakyCat.py <dataset_path> <weights_path> <results_dir>")
    sys.exit(1)

dataset_path       = sys.argv[1]
model_weights_path = sys.argv[2]
results_dir        = sys.argv[3]
results_file       = os.path.join(results_dir, "FlakeFlagger_final_predictions.csv")

if not os.path.exists(results_dir):
    os.makedirs(results_dir)
    print(f"Created directory: {results_dir}")

df = pd.read_csv(dataset_path)
print(f"Original dataset size: {len(df)}")
df = df.dropna(subset=['final_code'])
print(f"Cleaned dataset size: {len(df)}")

model_name = "./codebert-base-local"
model_config = AutoConfig.from_pretrained(
    model_name,
    return_dict=False,
    output_hidden_states=True
)
tokenizer  = AutoTokenizer.from_pretrained(model_name)
auto_model = AutoModel.from_pretrained(model_name, config=model_config)


class BERT_Arch(nn.Module):
    def __init__(self, bert):
        super(BERT_Arch, self).__init__()
        self.bert    = bert
        self.dropout = nn.Dropout(0.1)
        self.relu    = nn.ReLU()
        self.fc1     = nn.Linear(768, 512)
        self.fc2     = nn.Linear(512, 2)
        self.softmax = nn.LogSoftmax(dim=-1)

    def forward(self, sent_id, mask):
        cls_hs = self.bert(sent_id, attention_mask=mask)[1]
        x = self.fc1(cls_hs)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return self.softmax(x)

model = BERT_Arch(auto_model)

print(f"\nLoading pretrained weights from: {model_weights_path}")
print(f"File size: {os.path.getsize(model_weights_path) / (1024*1024):.1f} MB")

try:
    state_dict = torch.load(model_weights_path, map_location=device)
    print("Weights loaded successfully.")
except Exception as e:
    print(f"\nFailed to load weights: {e}")
    print("\nThe .pt file may be corrupted or truncated.")
    print("Please re-download it from the original source and try again.")
    sys.exit(1)

if isinstance(state_dict, dict):
    if 'model_state_dict' in state_dict:
        state_dict = state_dict['model_state_dict']
        print("Unwrapped key: model_state_dict")
    elif 'model' in state_dict:
        state_dict = state_dict['model']
        print("Unwrapped key: model")
    elif 'state_dict' in state_dict:
        state_dict = state_dict['state_dict']
        print("Unwrapped key: state_dict")

missing, unexpected = model.load_state_dict(state_dict, strict=False)
print(f"Missing keys   : {len(missing)}")
print(f"Unexpected keys: {len(unexpected)}")
if missing:
    print(f"  Missing  : {missing[:5]}{'...' if len(missing) > 5 else ''}")
if unexpected:
    print(f"  Unexpected: {unexpected[:5]}{'...' if len(unexpected) > 5 else ''}")

model.to(device)
model.eval()
print("Model ready for inference.\n")

def get_predictions(codes):
    preds_list = []
    total = len(codes)
    print(f"Starting inference on {total} samples...")

    with torch.no_grad():
        for i, code in enumerate(codes):
            inputs = tokenizer.encode_plus(
                str(code),
                max_length     = 510,
                pad_to_max_length = True,
                truncation     = True,
                return_tensors = 'pt'
            )
            sent_id = inputs['input_ids'].to(device)
            mask    = inputs['attention_mask'].to(device)

            output     = model(sent_id, mask)
            prediction = torch.argmax(output, dim=1).item()
            preds_list.append(prediction)

            if (i + 1) % 5 == 0 or (i + 1) == total:
                print(f"  Processed {i + 1}/{total} tests.")

    return preds_list

df['prediction'] = get_predictions(df['final_code'].tolist())

df.to_csv(results_file, index=False)

flagged     = df[df['prediction'] == 1].shape[0]
not_flagged = df[df['prediction'] == 0].shape[0]

print(f"\n--- REPLICATION TASK 3 COMPLETE ---")
print(f"Output saved to      : {results_file}")
print(f"Total FlakyCat Tests : {len(df)}")
print(f"Flagged as Flaky     : {flagged}")
print(f"Flagged as Non-Flaky : {not_flagged}")