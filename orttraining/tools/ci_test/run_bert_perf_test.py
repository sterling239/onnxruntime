#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse
import subprocess
import sys
import tempfile
import os

from compare_results import compare_results_files, Comparisons

SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))

def parse_args():
  parser = argparse.ArgumentParser(description="Runs a BERT convergence test.")
  parser.add_argument("--binary_dir", required=True,
                      help="Path to the ORT binary directory.")
  parser.add_argument("--training_data_root", required=True,
                      help="Path to the training data root directory.")
  parser.add_argument("--model_root", required=True,
                      help="Path to the model root directory.")
  return parser.parse_args()

def main():
    args = parse_args()

    # run BERT training
    subprocess.run([
        os.path.join(args.binary_dir, "onnxruntime_training_bert"),
        "--model_name", os.path.join(
            args.model_root, "nv/bert-base/bert-base-uncased_L_12_H_768_A_12_V_30528_S_512_Dp_0.1_optimized_layer_norm"),
        "--train_data_dir", os.path.join(
            args.training_data_root, "128/books_wiki_en_corpus/train"),
        "--test_data_dir", os.path.join(
            args.training_data_root, "128/books_wiki_en_corpus/test"),
        "--train_batch_size", "64",
        "--mode", "train",
        "--num_train_steps", "100",
        "--display_loss_steps", "5",
        "--optimizer", "adam",
        "--learning_rate", "5e-4",
        "--warmup_ratio", "0.1",
        "--warmup_mode", "Linear",
        "--gradient_accumulation_steps", "1",
        "--max_predictions_per_seq=20",
        "--use_mixed_precision",
        "--allreduce_in_fp16",
        "--lambda", "0",
        "--use_nccl",
        "--seed", "42",
        "--enable_grad_norm_clip=false",
        "--perf_output_dir", os.path.join(SCRIPT_DIR, "results"), 
    ]).check_returncode()

    return 0

if __name__ == "__main__":
  sys.exit(main())
