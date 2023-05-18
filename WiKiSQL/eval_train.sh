# predict train
python tableqa/run_model.py eval --sub-dir train --max-tokens 14000 --dataset-dir dataset/wikisql/tapex.base --model-path checkpoints_st+syn_iter0_0204/checkpoint_best.pt \
--predict-dir predict_train_uctr_iter_1_0205