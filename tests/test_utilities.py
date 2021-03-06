import os
import unittest

import numpy.testing as npt


class UtilitiesTestCase(unittest.TestCase):
    def test_checksum(self):
        import astroNN
        from astroNN.shared.downloader_tools import md5_checksum, sha1_checksum, sha256_checksum
        anderson2017_path = os.path.join(os.path.dirname(astroNN.__path__[0]), 'astroNN', 'data',
                                         'anderson_2017_dr14_parallax.npz')
        md5_pred = md5_checksum(anderson2017_path)
        sha1_pred = sha1_checksum(anderson2017_path)
        sha256_pred = sha256_checksum(anderson2017_path)

        # read answer hashed by Windows Get-FileHash
        self.assertEqual(md5_pred, '9C714F5FE22BB7C4FF9EA32F3E859D73'.lower())
        self.assertEqual(sha1_pred, '733C0227CF93DB0CD6106B5349402F251E7ED735'.lower())
        self.assertEqual(sha256_pred, '36C265C907F440114D747DA21D2A014D32B5E442D541F183C0EE862F5865FD26'.lower())

    def test_normalizer(self):
        from astroNN.nn.utilities.normalizer import Normalizer
        from astroNN.config import MAGIC_NUMBER
        import numpy as np

        data = np.random.normal(0, 1, (100, 10))
        magic_idx = (10, 5)
        data[magic_idx] = MAGIC_NUMBER

        # create a normalizer instance
        normer = Normalizer(mode=1)
        norm_data = normer.normalize(data)

        # make sure normalizer preserve magic_number
        self.assertEqual(norm_data[magic_idx], MAGIC_NUMBER)

        # test demoralize
        data_denorm = normer.denormalize(norm_data)
        # make sure demoralizer preserve magic_number
        self.assertEqual(data_denorm[magic_idx], MAGIC_NUMBER)
        npt.assert_array_almost_equal(data_denorm, data)

        errorous_norm = Normalizer(mode=-1234)

        self.assertRaises(ValueError, errorous_norm.normalize, data)

        # test mode='3s' can do identity transformation
        s3_norm = Normalizer(mode='3s')
        data = np.random.normal(0, 1, (100, 10))
        npt.assert_array_almost_equal(s3_norm.denormalize(s3_norm.normalize(data)), data)

    def test_cpu_gpu_management(self):
        from astroNN.shared.nn_tools import cpu_fallback

        cpu_fallback(flag=0)
        # os environ is string
        self.assertEqual(os.environ['CUDA_VISIBLE_DEVICES'], '-1')

        cpu_fallback(flag=1)
        # make sure flag =1 will delete the environ
        self.assertEqual(any(x == "CUDA_VISIBLE_DEVICES" for x in os.environ), False)

        # make sure flag=2 raise error
        self.assertRaises(ValueError, cpu_fallback, flag=2)

    def test_h5name_check(self):
        from astroNN.datasets.h5 import h5name_check

        # make sure h5name=None raise error
        self.assertRaises(ValueError, h5name_check, None)

    def test_config(self):
        from astroNN.config import config_path

        config_path(flag=0)
        config_path(flag=1)
        config_path(flag=2)

        from astroNN.config import switch_keras
        switch_keras('tensorflow')
        switch_keras('keras')
        # make sure flag=None raises error
        self.assertRaises(ValueError, switch_keras, flag=None)
        # make sure flag=numpy raises error
        self.assertRaises(ValueError, switch_keras, flag='numpy')


if __name__ == '__main__':
    unittest.main()
