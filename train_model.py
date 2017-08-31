import tensorflow as tf
from numpy import *

node1 = tf.constant(3.0, dtype=tf.float32)
node2 = tf.constant(4.0)
print(node1, node2)

sess = tf.Session()
print(sess.run([node1, node2]))

data = array([[1, 2, 3], [1, 2, 3]])
print(data)
