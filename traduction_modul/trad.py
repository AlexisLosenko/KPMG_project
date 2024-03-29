import time
import math
import sys
import pickle
import glob
import os
import tensorflow as tf
from seq2seq_model import Seq2Seq_Model
from corpus import *


path_l1_dict = "/tmp/l1_dict.p"
path_l2_dict = "/tmp/l2_dict.p"
model_dir = "/tmp/translate"
model_checkpoints = model_dir + "/translate.ckpt"

def build_dataset(use_stored_dictionary = False):
    sen_l1, sen_l2 = retrieve_corpora()
    clean_sen_l1 = [clean_sentence(s) for s in sen_l1]
    clean_sen_l2 = [clean_sentence(s) for s in sen_l2]
    filt_clean_sen_l1, filt_clean_sen_l2 = filter_sentence_length(clean_sen_l1, clean_sen_l2)
if not use_stored_dictionary:
    dict_l1 = create_indexed_dictionary(filt_clean_sen_l1, dict_size = 15000, storage_path = path_l1_dict)
    dict_l2 = create_indexed_dictionary(filt_clean_sen_l2, dict_size = 10000, storage_path = path_l2_dict)
else:
    dict_l1 = pickle.load(open(path_l1_dict, "rb"))
    dict_l2 = pickle.load(open(path_l2_dict, "rb"))

def cleanup_checkpoints(model_dir, model_checkpoints):
    for f in glob.glob(model_checkpoints + "*"):
        os.remove(f)
    try:
        os.mkdir(model_dir)
    except FileExistsError:
        pass

def get_seq2seq_model(session, forward_only, dict_lengths, max_sentence_lengths, model_dir):
    model = Seq2SeqModel(
            source_vocab_size=dict_lengths[0],
            target_vocab_size=dict_lengths[1],
            buckets=[max_sentence_lengths],
            size=256,
            num_layers=2,
            max_gradient_norm=5.0,
            batch_size=64,
            learning_rate=0.5,
            learning_rate_decay_factor=0.99,
            forward_only=forward_only,
            dtype=tf.float16)
    ckpt = tf.train.get_checkpoint_state(model_dir)
    if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
        print("Reading model parameters from {}".format(ckpt.model_checkpoint_path))
        model.saver.restore(session, ckpt.model_checkpoint_path)
    else:
        print("Created model with fresh parameters.")
        session.run(tf.global_variables_initializer())
    return model

def train():
    with tf.Session() as sess:
        model = get_seq2seq_model(sess, False, dict_lengths, max_sentence_lengths, model_dir)
        # This is the training loop.
        step_time, loss = 0.0, 0.0
        current_step = 0
        bucket = 0
        steps_per_checkpoint = 100
        max_steps = 20000
        while current_step:
            if __name__ == "__main__":
                _, data_set, max_sentence_lengths, dict_lengths = build_dataset(False)
                cleanup_checkpoints(model_dir, model_checkpoints)
                train()
