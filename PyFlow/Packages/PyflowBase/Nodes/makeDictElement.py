from PyFlow import _HASHABLES
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class makeDictElement(NodeBase):
    def __init__(self, name):
        super(makeDictElement, self).__init__(name)
        self.bCacheEnabled = False
        self.key = self.createInputPin('key', 'AnyPin', structure=PinStructure.Single, constraint="1",allowedPins=_HASHABLES)
        self.value = self.createInputPin('value', 'AnyPin', structure=PinStructure.Multi, constraint="2")
        self.value.enableOptions(PinOptions.AllowAny)
        self.outArray = self.createOutputPin('out', 'AnyPin', defaultValue=dictElement(), structure=PinStructure.Single, constraint="2")
        self.outArray.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSuported)
        self.outArray.onPinConnected.connect(self.outPinConnected)
        self.outArray.onPinDisconnected.connect(self.outPinDisConnected)
        self.key.dataBeenSet.connect(self.dataBeenSet)
        self.value.dataBeenSet.connect(self.dataBeenSet)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(PinStructure.Single)
        helper.addInputStruct(PinStructure.Multi)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'Array'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Creates a Dict Element'

    def dataBeenSet(self,pin=None):
        try:
            self.outArray._data = dictElement(self.key.getData(), self.value.getData())
            self.checkForErrors()
        except:
            pass

    def outPinDisConnected(self,inp):
        dictNode = inp.getDictNode([])
        if dictNode:
            if dictNode.KeyType in self.constraints[self.key.constraint]:
                self.constraints[self.key.constraint].remove(dictNode.KeyType)
            if self.key in dictNode.constraints[self.key.constraint]:    
                dictNode.constraints[self.key.constraint].remove(self.key)

            if dictNode.ValueType in self.constraints[self.value.constraint]:
                self.constraints[self.value.constraint].remove(dictNode.ValueType)
            if self.value in dictNode.constraints[self.value.constraint]:    
                dictNode.constraints[self.value.constraint].remove(self.value)

        self.outPinConnected(self.outArray)

    def outPinConnected(self,inp):
        dictNode = inp.getDictNode([])
        if dictNode:
            if dictNode.KeyType not in self.constraints[self.key.constraint]:
                self.constraints[self.key.constraint].append(dictNode.KeyType)
            if self.key not in dictNode.constraints[self.key.constraint]:    
                dictNode.constraints[self.key.constraint].append(self.key)
            self.key.setType(dictNode.KeyType.dataType)

            if dictNode.ValueType not in self.constraints[self.value.constraint]:
                self.constraints[self.value.constraint].append(dictNode.ValueType)
            if self.value not in dictNode.constraints[self.value.constraint]:    
                dictNode.constraints[self.value.constraint].append(self.value)
            self.value.setType(dictNode.ValueType.dataType)

    def compute(self, *args, **kwargs):
        self.outArray.setData(dictElement(self.key.getData(), self.value.getData()))
