import numpy as np
import tensorflow as tf
import base64
from io import BytesIO
from PIL import Image
from seefood_config import root_folder


class see_food:

    def __init__(self):
        self.sess = tf.Session()
        self.saver = tf.train.import_meta_graph(root_folder + '/saved_model/model_epoch5.ckpt.meta')
        self.saver.restore(self.sess, tf.train.latest_checkpoint(root_folder + '/saved_model/'))
        self.graph = tf.get_default_graph()
        self.x_input = self.graph.get_tensor_by_name('Input_xn/Placeholder:0')
        self.keep_prob = self.graph.get_tensor_by_name('Placeholder:0')
        self.class_scores = self.graph.get_tensor_by_name("fc8/fc8:0")

    def is_food(self, data):
        image = Image.open(BytesIO(base64.b64decode(data))).convert('RGB')
        image = image.resize((227, 227), Image.BILINEAR)
        img_tensor = [np.asarray(image, dtype=np.float32)]
        # Run the image in the model.
        scores = self.sess.run(self.class_scores, {self.x_input: img_tensor, self.keep_prob: 1.})

        return (scores, np.argmax(scores) != 1)

# ai = see_food()
# print ai.is_food('''R0lGODlhDwAPAKECAAAAzMzM/////wAAACwAAAAADwAPAAACIISPeQHsrZ5ModrLlN48CXF8m2iQ3YmmKqVlRtW4MLwWACH+H09wdGltaXplZCBieSBVbGVhZCBTbWFydFNhdmVyIQAAOw==''')
