#!/usr/bin/env python
'''
Created on 20 Jul 2020

@author: Christoph Minz
'''
from __future__ import annotations
import unittest
from event import CausetEvent
from causet import Causet
from embeddedcauset import EmbeddedCauset
import numpy as np
import os
from matplotlib import pyplot as plt


class CausetTestCase(unittest.TestCase):

    def assertCauset(self, S: Causet, size: int,
                     is_chain: bool, is_antichain: bool):
        self.assertEqual(S.Card, size)
        self.assertEqual(S.isPath(), is_chain and (size > 0))
        self.assertEqual(S.isChain(), is_chain)
        self.assertEqual(S.isAntichain(), is_antichain)


class TestCauset(CausetTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

#     def test_setoperations(self):
#         a = CausetEvent(label=1)
#         b = CausetEvent(label=2, past={a})
#         c = CausetEvent(label=3)
#         d = CausetEvent(label=4)
#         C1 = Causet(eventSet={a, b, c})
#         C2 = Causet(eventSet={a, b, d})
#         self.assertEqual(c in C1, True)
#         self.assertEqual(c not in C2, True)
#         self.assertEqual(C1 - C2, {c})
#         self.assertEqual(C2 - C1, {d})
#         self.assertEqual(C1 & C2, {a, b})
#         self.assertEqual(C1 | C2, {a, b, c, d})
#         self.assertEqual(C1 ^ C2, {c, d})
#
#     def test_NewChain(self):
#         self.assertCauset(Causet.NewChain(5), 5, True, False)
#         self.assertCauset(Causet.NewChain(0), 0, True, True)
#         self.assertCauset(Causet.NewChain(-5), 0, True, True)
#         self.assertRaises(TypeError, Causet.NewChain, 1.2)
#         self.assertRaises(TypeError, Causet.NewChain, 'chain')
#
#     def test_NewAntichain(self):
#         self.assertCauset(Causet.NewAntichain(5), 5, False, True)
#         self.assertCauset(Causet.NewAntichain(0), 0, True, True)
#         self.assertCauset(Causet.NewAntichain(-5), 0, True, True)
#         self.assertRaises(TypeError, Causet.NewAntichain, 1.2)
#         self.assertRaises(TypeError, Causet.NewAntichain, 'antichain')
#
#     def test_NewSimplex(self):
#         self.assertCauset(Causet.NewSimplex(0), 1, True, True)
#         self.assertCauset(Causet.NewSimplex(1), 3, False, False)
#         self.assertCauset(Causet.NewSimplex(2, False), 6, False, False)
#         self.assertCauset(Causet.NewSimplex(3), 15, False, False)
#         self.assertCauset(Causet.NewSimplex(4, False), 30, False, False)
#
#     def test_NewFence(self):
#         self.assertCauset(Causet.NewFence(-1), 0, True, True)
#         self.assertCauset(Causet.NewFence(1), 2, True, False)
#         self.assertCauset(Causet.NewFence(2), 4, False, False)
#         self.assertCauset(Causet.NewCrown(), 6, False, False)
#         self.assertCauset(Causet.NewFence(4, closed=False), 8, False, False)
#
#     def test_NewKROrder(self):
#         self.assertCauset(Causet.NewKROrder(2), 8, False, False)
#
#     def test_FromPastMatrix(self):
#         C: np.ndarray = np.array([[False, True, True],
#                                   [False, False, False],
#                                   [False, False, False],
#                                   [True, True, True],
#                                   [True, False, False]])
#         S: Causet = Causet.FromFutureMatrix(C)
#         self.assertCauset(S, 5, False, False)
#         self.assertRaises(ValueError, Causet.FromPastMatrix, C)
#         self.assertRaises(ValueError, Causet.FromPastMatrix,
#                           np.array([[False, True], [True, False]]))
#
#     def test_PastMatrix(self):
#         filename: str = 'test_causets.test_PastMatrix.csv'
#         S: Causet = Causet.NewChain(4)
#         S.saveAsCSV(filename)
#         S = Causet.FromTextFile(filename)
#         self.assertCauset(S, 4, True, False)
#         os.remove(filename)
#
#     def test_merge(self):
#         S_antichain: Causet = Causet.NewAntichain(5)
#         S_chain: Causet = Causet.NewChain(5)
#         S: Causet = Causet.merge(S_antichain, S_chain)
#         self.assertCauset(S, 10, False, False)
#         self.assertEqual(len(S.PastInf), 5)
#         self.assertEqual(len(S.FutureInf), 1)
#
#     def test_Paths(self):
#         S: Causet = Causet.NewAntichain(5)
#         self.assertEqual(list(S.Paths(S.find(1), S.find(5))), [])
#         S = Causet.FromPermutation([1, 5, 4, 3, 2, 6])
#         i: int = 0
#         bot: CausetEvent = S.find(1)
#         central: Set[CausetEvent] = S.findAll(2, 3, 4, 5)
#         top: CausetEvent = S.find(6)
#         for p in S.Paths(bot, top, length='min'):
#             i += 1
#             self.assertEqual(S.isPath(p), True)
#             self.assertEqual(len(p), 3)
#             self.assertEqual(p[0], bot)
#             self.assertIn(p[1], central)
#             self.assertEqual(p[2], top)
#         self.assertEqual(i, 4)
#         S = Causet.NewSimplex(3)
#         self.assertEqual(len(list(S.Paths(S.find('1'),
#                                           S.find('1-2-3-4')))), 6)
#
#     def test_Antipaths(self):
#         S = Causet.NewFence(6)
#         i: int = 0
#         first: CausetEvent = S.find('1')
#         between1: Set[CausetEvent] = S.findAll('2', '6')
#         between2: Set[CausetEvent] = S.findAll('3', '5')
#         last: CausetEvent = S.find('4')
#         for ap in S.Antipaths(first, last, along=S.PastInf):
#             i += 1
#             self.assertEqual(len(ap), 4)
#             self.assertEqual(ap[0], first)
#             self.assertIn(ap[1], between1)
#             self.assertIn(ap[2], between2)
#             self.assertEqual(ap[3], last)
#         self.assertEqual(i, 2)
#         i = 0
#         for ap in S.Antipaths(first, first, along=S.PastInf):
#             i += 1
#             self.assertEqual(len(ap), 1)
#             self.assertEqual(ap[0], first)
#         self.assertEqual(i, 1)

    def test_plotDiagram(self):
        # S: Causet = Causet.NewSimplex(3)
        # eventList: List[CausetEvent] = list(S._events)
        # S.plotDiagram(set([*eventList[1:12], *eventList[13:15]]))
        # S.plotDiagram(set([*eventList[2:8], eventList[0]]))
        # S = EmbeddedCauset.FromPermutation(
        #     [3, 8, 10, 11, 14, 7, 1, 5, 12, 9, 6, 2, 13, 4])
        #         S = Causet.NewFence(6)
        #         S._print_eventlist(S.sortedByLabels())
        S = Causet.FromPermutation([1, 7, 6, 9, 5, 3, 2, 8, 4])
        ac: List[CausetEvent] = S.sortedByLabels(S.findAll(2, 3, 5, 6, 7))
        S = Causet.NewFence(8)
        ac = S.sortedByLabels(S.PastInf)
        print(S.DistanceMatrix(ac, counting='intersection'))
        S.AntichainPermutations(ac)
        event = S.sortedByLabels(S.PastInf)
        S._print_eventlist(event)
        # S._print_eventlists(S.disjoint())
#         S = Causet.NewPermutation(
#             [1, 6, 8, 7, 9, 5, 12, 3, 2, 10, 11, 4])
        # eventList: List[CausetEvent] = list(S._events)
        # S.plotDiagram(set([*eventList[0:11], *eventList[13:14]]))
        # print('| '.join(', '.join(str(e)
        #                           for e in layer)
        #                 for layer in S.layered()))
        # S = Causet.NewAntichain(11)
#         S.plotDiagram()
#         plt.show()


if __name__ == '__main__':
    unittest.main()