import sys
import numpy as np
import random
from itertools import compress
import multiprocessing as mp
# functions_selec =  [True, True, True, True, True, False, True, True, True, False, False, False, False, False, False]
functions_selec =  [True, True, True, False, True, True, False, True, False, False, True, False, False, False, False, True, True, False]

def randHex(lim=5):
    ran = random.randrange(10**80)
    myhex = "%064x" % ran
    # limit string to 'lim' characters
    return myhex[:lim]

class Tree(object):

    def __init__(self, level, var_size=2, max_level=6):
        self.data = None
        self.children = []
        self.all_children = []
        self.level = level
        self.id = randHex()
        self.required_children_size = 0
        self.father = None
        self.results = None
        self.max_level = max_level
        self.end_types = (int, float)
        self.var_size = var_size

        self.possible_variables = []
        for i in range(var_size):
            self.possible_variables.append(str(i))

    def isTerminal(self, data=None):
        if data == None:
            data = self.data
        if self.level == self.max_level or type(data) in self.end_types or data in self.possible_variables:
            return True
        else:
            return False

    def getMaxLevel(self):
        if self.isTerminal():
            return self.level
        else:
            max_level = 0
            for ch in self.children:
                l = ch.getMaxLevel() 
                if l > max_level:
                    max_level = l
            return max_level

    def getDepth(self):
        return self.getMaxLevel() - self.level

    def getAllChildren(self):
        children = [self]
        for ch in self.children:
            ch_ = ch.getAllChildren()
            # ch_.append(ch)
            children.extend(ch_)
        
        return children
        
    def printTree(self):
        ident = ("|" * (self.level) )+"->" 
        if self.father != None:
            print("{} Data {} id {}".format(ident, self.data, self.id))
        else:
            print("{} Data {} id {}".format(ident, self.data, self.id))
        for ch in self.children:
            ch.printTree()

    def printTreeComplete(self):
        ident = ("|" * (self.level) )+"->" 
        if self.father != None:
            print("{}Level: {} Data {} id {} father {}".format(
                ident, self.level, self.data, self.id, self.father.id))
        else:
            print("{}Level: {} Data {} id {} father None".format(
                ident, self.level, self.data, self.id))
        for ch in self.children:
            ch.printTreeComplete()

    def addChildren(self, node=None):
        if self.level < self.max_level:
            if node == None:
                node = Tree(self.level + 1, var_size=self.var_size, max_level=self.max_level)

            node.father = self
            node.max_level = self.max_level
            node.level = self.level + 1
            self.children.append(node)
            return node
        else:
            self.printTreeComplete()
            raise ValueError("Can not add children... Max level achived", "Max level:", self.max_level)


    def childrenResults(self, variables):
        if self.results == None:
            self.results = []
            for node in self.children:
                self.results.append(node.getData(variables))

    def setData(self, data):
        if self.level == self.max_level:
            if self.isTerminal(data):
                self.data = data
            else:
                print("Terminal node... Data need to be {} or an varible (string). You inserted {} ({})".format(
                    self.end_types, data, type(data)))
        else:
            self.data = data
            if not self.isTerminal(data):
                # print self.possible_variables
                # print("data {} self.level {} self.max {}".format(data, self.level, self.max_level))
                self.required_children_size = Operators().datasize[data]
                while self.required_children_size > len(self.children):
                    self.addChildren()
                
    def getData(self, variables):
        if type(self.data) in self.end_types:
            return self.data
        elif type(self.data) == str:
            return variables[int(self.data)]
        else:
            self.childrenResults(variables)
            return self.data(self.results)

    def correct_levels(self, level):
        self.level = level
        if self.level > self.max_level:
            raise ValueError("Level {} > {} max_level".format(self.level, self.max_level))
        for ch in self.children:
            ch.max_level = self.max_level
            ch.correct_levels(level + 1)

    def toMinRepr(self):
        # To Save
        pass

    def fromMinRepr(self):
        # To Load
        pass


class Function(object):
    def __init__(self, raw_function):
        self.raw_function = raw_function

    def __call__(self, *args, **kwargs):
        return self.raw_function(*args, **kwargs)

    def __str__(self):
        return self.raw_function.__name__


class Operators(object):

    def __init__(self, op=None, selec=functions_selec):

        self.operators = {'+': 0, '-': 1, '*': 2, '^': 3, '/': 4, 'ln': 5,
                          '%': 6, '|/': 7, '||/': 8, '!': 9, '@': 10, '&': 11, '|': 12, '#': 13, '~': 14, 'sin':15, 'cos':16, 'tg': 17}

        self.functions = [self.sum_op, self.minus_op, self.times_op, self.power_op, self.div_op, self.ln_op, self.mod_op,
                          self.sqrt_op, self.cbrt_op, self.fat_op, self.abs_op, self.and_op, self.or_op, self.xor_op, self.not_op, self.sin_op, self.cos_op, self.tg_op]

        self.datasize = {self.sum_op: 2, self.minus_op: 2, self.times_op: 2, self.power_op: 2, self.div_op: 2, self.ln_op: 1, self.mod_op: 2,
                         self.sqrt_op: 1, self.cbrt_op: 1, self.fat_op: 1, self.abs_op: 1, self.and_op: 2, self.or_op: 2, self.xor_op: 2, self.not_op: 1, self.sin_op:1, self.cos_op:1, self.tg_op:1}

        self.all_ops = ['+', '-', '*',  '^', '/', 'ln', '%',
                        '|/', '||/', '!', '@', '&', '|', '#', '~', 'sin', 'cos', 'tg']

        if not selec == None:
            self.functions = list(compress(self.functions, selec))
            self.all_ops = list(compress(self.all_ops, selec))

        if not op == None:
            if op in self.operators:
                self.op = self.functions[self.operators[op]]
            else:
                print("Operator {} does not exists".format(op))

    def __str__(self):
        return str(self.op)

    def printOps(self):
        print(self.all_ops)

    def randOp(self):
        return self.functions[np.random.randint(0, len(self.functions))]

    # @Function
    @staticmethod
    def sum_op(data):
        """ Sum operation "+"

        Args:
            data (list): Number to sum
        Returns:
            Sum of the input values"""
        if len(data) == 2:
            return data[0]+data[1]
        else:
            raise ValueError(
                '[E] - sum_op {+} must have only 2 inputs, it has %i' % len(data))


    # @Function
    @staticmethod
    def minus_op(data):
        if len(data) == 2:
            return data[0]-data[1]
        else:
            raise ValueError(
                '[E] - minus_op {-} must have only 2 inputs, it has %i' % len(data))
            sys.exit()

    # @Function
    @staticmethod
    def times_op(data):
        if len(data) == 2:
            return data[0]*data[1]
        else:
            raise ValueError(
                '[E] - times_op {*} must have only 2 inputs, it has %i' % len(data))
            sys.exit()

    # @Function
    @staticmethod
    def power_op(data):
        if len(data) == 2:
            # print (data)
            return np.power(data[0], data[1])
        else:
            raise ValueError(
                '[E] - power_op {^} must have only 2 inputs, it has %i' % len(data))
            sys.exit()

    # @Function
    @staticmethod
    def div_op(data):
        if len(data) == 2:
            if data[1] == 0:
                data[1] = 0.00001
            return data[0]/data[1]
        else:
            raise ValueError(
                '[E] - div_op {/} must have only 2 inputs, it has %i' % len(data))
            sys.exit()

    # @Function
    @staticmethod
    def ln_op(data):
        if len(data) == 1:
            if data[0] == 0:
                data[0] = 0.0001

            return np.log(abs(data[0]))
        else:
            raise ValueError(
                '[E] - ln_op {/} must have only 1 input, it has %i' % len(data))
            sys.exit()

    # @Function
    @staticmethod
    def mod_op(data):
        if len(data) == 2:
            return data[0] % data[1]
        else:
            raise ValueError(
                '[E] - mod_op must have only 2 inputs, it has %i' % len(data))
            sys.exit()
        pass

    # @Function
    @staticmethod
    def sqrt_op(data):
        if len(data) == 1:
            return np.sqrt(abs(data[0]))
        else:
            raise ValueError(
                '[E] - sqrt_op must have only 1 input, it has %i' % len(data))
            sys.exit()
        pass

    # @Function
    @staticmethod
    def cbrt_op(data):
        if len(data) == 1:
            return np.cbrt(abs(data[0]))
        else:
            raise ValueError(
                '[E] - cbrt_op must have only 1 input, it has %i' % len(data))
            sys.exit()

        pass

    # @Function
    @staticmethod
    def fat_op(data):
        if len(data) == 1:
            return np.math.factorial(np.abs(data[0]))
        else:
            raise ValueError(
                '[E] - fat_op must have only 1 input, it has %i' % len(data))
            sys.exit()

    # @Function
    @staticmethod
    def abs_op(data):
        if len(data) == 1:
            return np.abs(data[0])
        else:
            raise ValueError(
                '[E] - abs_op must have only 1 input, it has %i' % len(data))
            sys.exit()


    # @Function
    @staticmethod
    def and_op(data):
        if len(data) == 2:
            return np.bitwise_and(data[0], data[1])
        else:
            raise ValueError(
                '[E] - and_op must have only 2 input, it has %i' % len(data))
            sys.exit()


    # @Function
    @staticmethod
    def or_op(data):
        if len(data) == 2:
            return np.bitwise_or(data[0], data[1])
        else:
            raise ValueError(
                '[E] - or_op must have only 2 input, it has %i' % len(data))
            sys.exit()

    # @Function
    @staticmethod
    def xor_op(data):
        if len(data) == 2:
            return np.bitwise_xor(data[0], data[1])
        else:
            raise ValueError(
                '[E] - xor_op must have only 2 input, it has %i' % len(data))
            sys.exit()
        pass

    # @Function
    @staticmethod
    def not_op(data):
        if len(data) == 1:
            return np.bitwise_not(data[0])
        else:
            raise ValueError(
                '[E] - not_op must have only 1 input, it has %i' % len(data))
            sys.exit()
        pass

    # @Function
    @staticmethod
    def sin_op(data):
        if len(data) == 1:
            return np.sin(data[0])
        else:
            raise ValueError(
                '[E] - sin_op must have only 1 input, it has %i' % len(data))
            sys.exit()
        pass

    # @Function
    @staticmethod
    def cos_op(data):
        if len(data) == 1:
            return np.cos(data[0])
        else:
            raise ValueError(
                '[E] - cos_op must have only 1 input, it has %i' % len(data))
            sys.exit()
        pass

    # @Function
    @staticmethod
    def tg_op(data):
        if len(data) == 1:
            return np.math.tan(data[0])
        else:
            raise ValueError(
                '[E] - tg_op must have only 1 input, it has %i' % len(data))
            sys.exit()
        pass
