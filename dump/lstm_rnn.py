from test3 import *

# Import necessary libraries
import tensorflow as tf
import numpy as np

# Create an instance of the LstmRNN class
model = LstmRNN(stock_count=1, input_size=3)

# Initialize a TensorFlow session
with tf.Session() as sess:
    model.sess = sess

    # Initialize all variables
    sess.run(tf.global_variables_initializer())

    # Prepare your data
    # For simplicity, we're just using random data here
    # In a real-world scenario, you would replace this with your actual data
    dataset_list = [np.random.rand(100, 30, 3), np.random.rand(100, 3)]
    config = {
        'batch_size': 10,
        'init_learning_rate': 0.001,
        'learning_rate_decay': 0.99,
        'init_epoch': 5,
        'max_epoch': 50,
        'keep_prob': 0.8,
        'sample_size': 5
    }

    # Train the model
    final_pred = model.train(dataset_list, config)

    # Print the final prediction
    print(final_pred)