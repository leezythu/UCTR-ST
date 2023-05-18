CUDA_VISIBLE_DEVICES=4 PYTHONPATH=$PYTHONPATH:$(pwd) python tag_op/predictor.py --data_dir tag_op/cache/ --test_data_dir tag_op/cache/ \
--save_dir predict_st_for_iter1/ --eval_batch_size 32 --model_path ./checkpoint_0210_iter0_seed_1_syn+pseudo_train --encoder roberta --mode train
