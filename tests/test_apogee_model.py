import unittest

import numpy as np

from astroNN.models import ApogeeCNN, ApogeeBCNN, StarNet2017, ApogeeCVAE
from astroNN.models import load_folder
from astroNN.nn.callbacks import ErrorOnNaN

# Data preparation, keep the data size large (>800 data points to prevent issues)
random_xdata = np.random.normal(0, 1, (1000, 7514))
random_ydata = np.random.normal(0, 1, (1000, 25))


class ApogeeModelTestCase(unittest.TestCase):
    def test_apogee_cnn(self):
        # Apogee_CNN
        print("======Apogee_CNN======")
        neuralnet = ApogeeCNN()
        neuralnet.max_epochs = 1
        neuralnet.callbacks = ErrorOnNaN()
        neuralnet.train(random_xdata, random_ydata)
        prediction = neuralnet.test(random_xdata)
        jacobian = neuralnet.jacobian(random_xdata[:10])

        np.testing.assert_array_equal(prediction.shape, random_ydata.shape)
        np.testing.assert_array_equal(jacobian.shape, [random_xdata[:10].shape[0], random_ydata.shape[1],
                                                       random_xdata.shape[1]])
        neuralnet.save(name='apogee_cnn')

        neuralnet_loaded = load_folder("apogee_cnn")
        neuralnet_loaded.max_epochs = 1
        neuralnet_loaded.callbacks = ErrorOnNaN()
        prediction_loaded = neuralnet_loaded.test(random_xdata)

        # Apogee_CNN is deterministic
        np.testing.assert_array_equal(prediction, prediction_loaded)

        # Fine tuning test
        neuralnet_loaded.train(random_xdata, random_ydata)
        prediction_loaded = neuralnet_loaded.test(random_xdata)
        # prediction should not be equal after fine-tuning
        self.assertRaises(AssertionError, np.testing.assert_array_equal, prediction, prediction_loaded)

    def test_apogee_bcnn(self):
        random_xdata = np.random.normal(0, 1, (1000, 7514))
        random_ydata = np.random.normal(0, 1, (1000, 7))

        # Apogee_BCNN
        print("======Apogee_BCNN======")
        bneuralnet = ApogeeBCNN()
        bneuralnet.targetname = ['teff', 'logg', 'M', 'alpha', 'C1', 'Ti', 'Ti2']

        bneuralnet.max_epochs = 1
        bneuralnet.callbacks = ErrorOnNaN()
        bneuralnet.train(random_xdata, random_ydata)
        # prevent memory issue on Tavis CI
        bneuralnet.mc_num = 3
        prediction, prediction_err = bneuralnet.test(random_xdata)
        bneuralnet.plot_dense_stats()
        jacobian = bneuralnet.jacobian(random_xdata[:10], mean_output=True)

        np.testing.assert_array_equal(prediction.shape, random_ydata.shape)
        bneuralnet.save(name='apogee_bcnn')

        # just to make sure it can load it back without error
        bneuralnet_loaded = load_folder("apogee_bcnn")
        bneuralnet_loaded.plot_dense_stats()
        bneuralnet_loaded.callbacks = ErrorOnNaN()

        # prevent memory issue on Tavis CI
        bneuralnet_loaded.mc_num = 3
        pred, pred_err = bneuralnet_loaded.test(random_xdata)
        bneuralnet_loaded.aspcap_residue_plot(pred, pred, pred_err['total'])
        bneuralnet_loaded.jacobian_aspcap(jacobian)

        # Fine-tuning test
        bneuralnet_loaded.max_epochs = 1
        bneuralnet_loaded.train(random_xdata, random_ydata)

        pred, pred_err = bneuralnet_loaded.test_old(random_xdata)

    def test_apogee_cvae(self):
        # Data preparation, keep the data size large (>800 data points to prevent issues)
        random_xdata = np.random.normal(0, 1, (1000, 7514))

        # Apogee_CVAE
        print("======Apogee_CVAE======")
        cvae_net = ApogeeCVAE()
        cvae_net.max_epochs = 1
        cvae_net.latent_dim = 2
        cvae_net.callbacks = ErrorOnNaN()
        cvae_net.train(random_xdata, random_xdata)
        prediction = cvae_net.test(random_xdata)
        encoding = cvae_net.test_encoder(random_xdata)

        np.testing.assert_array_equal(prediction.shape, np.expand_dims(random_xdata, axis=-1).shape)
        np.testing.assert_array_equal(encoding.shape, [random_xdata.shape[0], cvae_net.latent_dim])
        cvae_net.save(name='apogee_cvae')

        # just to make sure it can load it back without error
        cvae_net_loaded = load_folder("apogee_cvae")
        encoding = cvae_net_loaded.test_encoder(random_xdata)
        np.testing.assert_array_equal(encoding.shape, [random_xdata.shape[0], cvae_net.latent_dim])

        # Fine-tuning test
        cvae_net_loaded.max_epochs = 1
        cvae_net.callbacks = ErrorOnNaN()
        cvae_net_loaded.train(random_xdata, random_xdata)

    def test_starnet2017(self):
        # StarNet2017
        print("======StarNet2017======")
        starnet2017 = StarNet2017()
        starnet2017.max_epochs = 1
        starnet2017.callbacks = ErrorOnNaN()
        starnet2017.train(random_xdata, random_ydata)
        prediction = starnet2017.test(random_xdata)
        jacobian = starnet2017.jacobian(random_xdata[:10])

        np.testing.assert_array_equal(prediction.shape, random_ydata.shape)
        np.testing.assert_array_equal(jacobian.shape, [random_xdata[:10].shape[0], random_ydata.shape[1],
                                                       random_xdata.shape[1]])
        starnet2017.save(name='starnet2017')

        starnet2017_loaded = load_folder("starnet2017")
        prediction_loaded = starnet2017_loaded.test(random_xdata)
        # StarNet2017 is deterministic
        np.testing.assert_array_equal(prediction, prediction_loaded)

        # Fine-tuning test
        starnet2017_loaded.max_epochs = 1
        starnet2017.callbacks = ErrorOnNaN()
        starnet2017_loaded.train(random_xdata, random_ydata)


if __name__ == '__main__':
    unittest.main()
