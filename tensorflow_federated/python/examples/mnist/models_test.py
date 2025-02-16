# Lint as: python3
# Copyright 2019, The TensorFlow Federated Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections

import numpy as np
import tensorflow as tf
import tensorflow_federated as tff

from tensorflow_federated.python.examples.mnist import models


class MnistTest(tf.test.TestCase):

  def setUp(self):
    tf.keras.backend.clear_session()
    super(MnistTest, self).setUp()

  def test_something(self):
    it_process = tff.learning.build_federated_averaging_process(models.model_fn)
    self.assertIsInstance(it_process, tff.utils.IterativeProcess)
    federated_data_type = it_process.next.type_signature.parameter[1]
    self.assertEqual(
        str(federated_data_type), '{<x=float32[?,784],y=int64[?,1]>*}@CLIENTS')

  def test_simple_training(self):
    # Try to test the high-performance stack. If we are in Python 2, the new
    # executor API will not be available, and an exception will be raised.
    try:
      tff.framework.set_default_executor(tff.framework.create_local_executor())
      self._do_test_simple_training()
      tff.framework.set_default_executor()
    except AttributeError:
      pass
    self._do_test_simple_training()

  def _do_test_simple_training(self):
    it_process = tff.learning.build_federated_averaging_process(models.model_fn)
    server_state = it_process.initialize()
    Batch = collections.namedtuple('Batch', ['x', 'y'])  # pylint: disable=invalid-name

    # Test out manually setting weights:
    keras_model = models.create_keras_model(compile_model=True)
    server_state = tff.learning.state_with_new_model_weights(
        server_state,
        trainable_weights=self.evaluate(keras_model.trainable_weights),
        non_trainable_weights=self.evaluate(keras_model.non_trainable_weights))

    def deterministic_batch():
      return Batch(
          x=np.ones([1, 784], dtype=np.float32),
          y=np.ones([1, 1], dtype=np.int64))

    batch = tff.tf_computation(deterministic_batch)()
    federated_data = [[batch]]

    def keras_evaluate(state):
      tff.learning.assign_weights_to_keras_model(keras_model, state.model)
      # N.B. The loss computed here won't match the
      # loss computed by TFF because of the Dropout layer.
      keras_model.test_on_batch(batch.x, batch.y)

    loss_list = []
    for _ in range(3):
      keras_evaluate(server_state)
      server_state, loss = it_process.next(server_state, federated_data)
      loss_list.append(loss)
    keras_evaluate(server_state)

    self.assertLess(np.mean(loss_list[1:]), loss_list[0])

  def test_self_contained_example(self):
    num_rounds = 2
    num_clients = 3

    # Try to test the high-performance stack. If we are in Python 2, the new
    # executor API will not be available, and an exception will be raised.
    try:
      tff.framework.set_default_executor(
          tff.framework.create_local_executor(num_clients))
      self._do_test_self_contained_example(num_rounds, num_clients)
      tff.framework.set_default_executor()
    except AttributeError:
      pass
    self._do_test_self_contained_example(num_rounds, num_clients)

  def test_self_contained_example_clients_unspecified(self):
    num_rounds = 2
    num_clients = 3
    # Try to test the high-performance stack. If we are in Python 2, the new
    # executor API will not be available, and an exception will be raised.
    try:
      tff.framework.set_default_executor(tff.framework.create_local_executor())
      self._do_test_self_contained_example(num_rounds, num_clients)
      tff.framework.set_default_executor()
    except AttributeError:
      pass
    self._do_test_self_contained_example(num_rounds, num_clients)

  def _do_test_self_contained_example(self, num_rounds, num_clients):
    emnist_batch = collections.OrderedDict([('label', [5]),
                                            ('pixels', np.random.rand(28, 28))])

    output_types = collections.OrderedDict([('label', tf.int32),
                                            ('pixels', tf.float32)])

    output_shapes = collections.OrderedDict([
        ('label', tf.TensorShape([1])),
        ('pixels', tf.TensorShape([28, 28])),
    ])

    def generate_one_emnist_batch():
      yield emnist_batch

    dataset = tf.data.Dataset.from_generator(generate_one_emnist_batch,
                                             output_types, output_shapes)

    def client_data():
      # 1. Repeat the single element dataset once (-> two elements of size 2)
      # 2. Batch the dataset by size 2 (1 element of size 2)
      return models.keras_dataset_from_emnist(dataset).repeat(2).batch(2)

    train_data = [client_data()] * num_clients
    sample_batch = self.evaluate(next(iter(train_data[0])))

    def model_fn():
      return tff.learning.from_compiled_keras_model(
          models.create_simple_keras_model(), sample_batch)

    trainer = tff.learning.build_federated_averaging_process(model_fn)
    state = trainer.initialize()
    results = []
    for _ in range(num_rounds):
      state, result = trainer.next(state, train_data)
      # Track the loss.
      results.append(result)
    self.assertEqual([r.num_examples for r in results],
                     [2 * num_clients] * num_rounds)
    self.assertLess(results[-1].loss, results[-2].loss)


if __name__ == '__main__':
  tf.compat.v1.enable_v2_behavior()
  tf.test.main()
