# coding: utf-8

import random
import numpy as np


class CRFeeder(object):
    """Helper for feed train data

    Attributes:
        feats: Features [train_size, feature_size]
        labels: labels [train_size]
    """

    def __init__(self, feats, labels, max_length: int, feat_size: int, batch_size: int):
        self._feats = feats
        self._labels = labels
        self._max_length = max_length
        self._feat_size = feat_size
        self._batch_size = batch_size

        self.size = len(feats)
        self.offset = 0
        self.epoch = 1

    @property
    def step_per_epoch(self):
        return (self.size - 1) // self._batch_size + 1

    def next_epoch(self):
        self.offset = 0
        self.epoch += 1

        # Shuffle
        tmp = list(zip(self._feats, self._labels))
        random.shuffle(tmp)
        self._feats, self._labels = zip(*tmp)

    def feed(self):
        next_offset = min(self.size, self.offset + self._batch_size)
        batch_size = next_offset - self.offset
        feats = self._feats[self.offset: next_offset]
        labels = self._labels[self.offset: next_offset]
        self.offset = next_offset

        '''
        Should change X to (indices, values, shape)
        Should change y to (batch_size, max_length)
        '''

        shape = np.array([batch_size, self._max_length, self._feat_size])
        indices = [
            [idx1, idx2, v3]
            for idx1, v1 in enumerate(feats)
            for idx2, v2 in enumerate(v1)
            for idx3, v3 in enumerate(v2)
        ]
        values = np.ones(len(indices))
        indices = np.array(indices)

        labels = list(map(lambda x: np.pad(x, (0, self._max_length - x.shape[0]), 'constant', constant_values=0),
                          labels))  # Pad zeors
        labels = np.array(labels, dtype=np.int32)

        return (indices, values, shape), labels

    def predict(self, feats):
        '''
        :param feats: [max_length, feat_size]
        :return: (indices, values, shape), len
        '''

        length = len(feats)

        shape = np.array([1, self._max_length, self._feat_size])
        indices = [
            [0, idx1, v2]
            for idx1, v1 in enumerate(feats)
            for idx2, v2 in enumerate(v1)
        ]
        values = np.ones(len(indices))
        indices = np.array(indices)

        return (indices, values, shape), length

    def test(self, feats):
        '''
        :param X: [batch_size, max_length, feat_size]
        :return: (indices, values, shape), len
        '''

        shape = np.array([len(feats), self._max_length, self._feat_size])
        indices = [
            [idx1, idx2, v3]
            for idx1, v1 in enumerate(feats)
            for idx2, v2 in enumerate(v1)
            for idx3, v3 in enumerate(v2)
        ]
        values = np.ones(len(indices))
        indices = np.array(indices)

        return (indices, values, shape)
