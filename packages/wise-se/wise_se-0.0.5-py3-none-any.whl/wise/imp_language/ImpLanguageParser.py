# Generated from ImpLanguage.g4 by ANTLR 4.11.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,30,104,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,3,1,18,8,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,26,8,1,10,1,
        12,1,29,9,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,
        59,8,2,1,2,1,2,1,2,1,2,1,2,1,2,5,2,67,8,2,10,2,12,2,70,9,2,1,3,1,
        3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,
        3,1,3,1,3,1,3,1,3,3,3,94,8,3,1,3,1,3,1,3,5,3,99,8,3,10,3,12,3,102,
        9,3,1,3,0,3,2,4,6,4,0,2,4,6,0,1,1,0,25,26,118,0,8,1,0,0,0,2,17,1,
        0,0,0,4,58,1,0,0,0,6,93,1,0,0,0,8,9,3,6,3,0,9,1,1,0,0,0,10,11,6,
        1,-1,0,11,18,5,28,0,0,12,18,5,27,0,0,13,14,5,3,0,0,14,15,3,2,1,0,
        15,16,5,4,0,0,16,18,1,0,0,0,17,10,1,0,0,0,17,12,1,0,0,0,17,13,1,
        0,0,0,18,27,1,0,0,0,19,20,10,3,0,0,20,21,5,1,0,0,21,26,3,2,1,4,22,
        23,10,2,0,0,23,24,5,2,0,0,24,26,3,2,1,3,25,19,1,0,0,0,25,22,1,0,
        0,0,26,29,1,0,0,0,27,25,1,0,0,0,27,28,1,0,0,0,28,3,1,0,0,0,29,27,
        1,0,0,0,30,31,6,2,-1,0,31,59,7,0,0,0,32,33,3,2,1,0,33,34,5,5,0,0,
        34,35,3,2,1,0,35,59,1,0,0,0,36,37,3,2,1,0,37,38,5,6,0,0,38,39,3,
        2,1,0,39,59,1,0,0,0,40,41,3,2,1,0,41,42,5,7,0,0,42,43,3,2,1,0,43,
        59,1,0,0,0,44,45,3,2,1,0,45,46,5,8,0,0,46,47,3,2,1,0,47,59,1,0,0,
        0,48,49,3,2,1,0,49,50,5,9,0,0,50,51,3,2,1,0,51,59,1,0,0,0,52,53,
        5,10,0,0,53,59,3,4,2,4,54,55,5,3,0,0,55,56,3,4,2,0,56,57,5,4,0,0,
        57,59,1,0,0,0,58,30,1,0,0,0,58,32,1,0,0,0,58,36,1,0,0,0,58,40,1,
        0,0,0,58,44,1,0,0,0,58,48,1,0,0,0,58,52,1,0,0,0,58,54,1,0,0,0,59,
        68,1,0,0,0,60,61,10,3,0,0,61,62,5,11,0,0,62,67,3,4,2,4,63,64,10,
        2,0,0,64,65,5,12,0,0,65,67,3,4,2,3,66,60,1,0,0,0,66,63,1,0,0,0,67,
        70,1,0,0,0,68,66,1,0,0,0,68,69,1,0,0,0,69,5,1,0,0,0,70,68,1,0,0,
        0,71,72,6,3,-1,0,72,94,5,13,0,0,73,94,5,14,0,0,74,75,5,28,0,0,75,
        76,5,15,0,0,76,94,3,2,1,0,77,78,5,16,0,0,78,94,3,4,2,0,79,80,5,17,
        0,0,80,81,3,4,2,0,81,82,5,18,0,0,82,83,3,6,3,0,83,84,5,19,0,0,84,
        85,3,6,3,0,85,86,5,20,0,0,86,94,1,0,0,0,87,88,5,21,0,0,88,89,3,4,
        2,0,89,90,5,22,0,0,90,91,3,6,3,0,91,92,5,23,0,0,92,94,1,0,0,0,93,
        71,1,0,0,0,93,73,1,0,0,0,93,74,1,0,0,0,93,77,1,0,0,0,93,79,1,0,0,
        0,93,87,1,0,0,0,94,100,1,0,0,0,95,96,10,1,0,0,96,97,5,24,0,0,97,
        99,3,6,3,2,98,95,1,0,0,0,99,102,1,0,0,0,100,98,1,0,0,0,100,101,1,
        0,0,0,101,7,1,0,0,0,102,100,1,0,0,0,8,17,25,27,58,66,68,93,100
    ]

class ImpLanguageParser ( Parser ):

    grammarFileName = "ImpLanguage.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'+'", "'-'", "'('", "')'", "'<='", "'<'", 
                     "'>='", "'>'", "'=='", "'not'", "'and'", "'or'", "'skip'", 
                     "'fail'", "'='", "'assert'", "'if'", "'then'", "'else'", 
                     "'fi'", "'while'", "'do'", "'od'", "';'", "'true'", 
                     "'false'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "TRUE", "FALSE", "NUM", "ID", "WS", "COMMENT" ]

    RULE_start = 0
    RULE_aexpr = 1
    RULE_bexpr = 2
    RULE_imp = 3

    ruleNames =  [ "start", "aexpr", "bexpr", "imp" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    T__19=20
    T__20=21
    T__21=22
    T__22=23
    T__23=24
    TRUE=25
    FALSE=26
    NUM=27
    ID=28
    WS=29
    COMMENT=30

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.11.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def imp(self):
            return self.getTypedRuleContext(ImpLanguageParser.ImpContext,0)


        def getRuleIndex(self):
            return ImpLanguageParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)




    def start(self):

        localctx = ImpLanguageParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self.imp(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AexprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ImpLanguageParser.RULE_aexpr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AddContext(AexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.AexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def aexpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ImpLanguageParser.AexprContext)
            else:
                return self.getTypedRuleContext(ImpLanguageParser.AexprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdd" ):
                listener.enterAdd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdd" ):
                listener.exitAdd(self)


    class SubContext(AexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.AexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def aexpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ImpLanguageParser.AexprContext)
            else:
                return self.getTypedRuleContext(ImpLanguageParser.AexprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSub" ):
                listener.enterSub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSub" ):
                listener.exitSub(self)


    class CstContext(AexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.AexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUM(self):
            return self.getToken(ImpLanguageParser.NUM, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCst" ):
                listener.enterCst(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCst" ):
                listener.exitCst(self)


    class VarContext(AexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.AexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(ImpLanguageParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVar" ):
                listener.enterVar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVar" ):
                listener.exitVar(self)


    class AparContext(AexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.AexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def aexpr(self):
            return self.getTypedRuleContext(ImpLanguageParser.AexprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterApar" ):
                listener.enterApar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitApar" ):
                listener.exitApar(self)



    def aexpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ImpLanguageParser.AexprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_aexpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [28]:
                localctx = ImpLanguageParser.VarContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 11
                self.match(ImpLanguageParser.ID)
                pass
            elif token in [27]:
                localctx = ImpLanguageParser.CstContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 12
                self.match(ImpLanguageParser.NUM)
                pass
            elif token in [3]:
                localctx = ImpLanguageParser.AparContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 13
                self.match(ImpLanguageParser.T__2)
                self.state = 14
                self.aexpr(0)
                self.state = 15
                self.match(ImpLanguageParser.T__3)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 27
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 25
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = ImpLanguageParser.AddContext(self, ImpLanguageParser.AexprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_aexpr)
                        self.state = 19
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 20
                        self.match(ImpLanguageParser.T__0)
                        self.state = 21
                        self.aexpr(4)
                        pass

                    elif la_ == 2:
                        localctx = ImpLanguageParser.SubContext(self, ImpLanguageParser.AexprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_aexpr)
                        self.state = 22
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 23
                        self.match(ImpLanguageParser.T__1)
                        self.state = 24
                        self.aexpr(3)
                        pass

             
                self.state = 29
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class BexprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ImpLanguageParser.RULE_bexpr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class BgeContext(BexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.BexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def aexpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ImpLanguageParser.AexprContext)
            else:
                return self.getTypedRuleContext(ImpLanguageParser.AexprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBge" ):
                listener.enterBge(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBge" ):
                listener.exitBge(self)


    class BparContext(BexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.BexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def bexpr(self):
            return self.getTypedRuleContext(ImpLanguageParser.BexprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBpar" ):
                listener.enterBpar(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBpar" ):
                listener.exitBpar(self)


    class BorContext(BexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.BexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def bexpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ImpLanguageParser.BexprContext)
            else:
                return self.getTypedRuleContext(ImpLanguageParser.BexprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBor" ):
                listener.enterBor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBor" ):
                listener.exitBor(self)


    class BleContext(BexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.BexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def aexpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ImpLanguageParser.AexprContext)
            else:
                return self.getTypedRuleContext(ImpLanguageParser.AexprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBle" ):
                listener.enterBle(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBle" ):
                listener.exitBle(self)


    class BltContext(BexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.BexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def aexpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ImpLanguageParser.AexprContext)
            else:
                return self.getTypedRuleContext(ImpLanguageParser.AexprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlt" ):
                listener.enterBlt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlt" ):
                listener.exitBlt(self)


    class BandContext(BexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.BexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def bexpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ImpLanguageParser.BexprContext)
            else:
                return self.getTypedRuleContext(ImpLanguageParser.BexprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBand" ):
                listener.enterBand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBand" ):
                listener.exitBand(self)


    class BcstContext(BexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.BexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def TRUE(self):
            return self.getToken(ImpLanguageParser.TRUE, 0)
        def FALSE(self):
            return self.getToken(ImpLanguageParser.FALSE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBcst" ):
                listener.enterBcst(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBcst" ):
                listener.exitBcst(self)


    class BgtContext(BexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.BexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def aexpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ImpLanguageParser.AexprContext)
            else:
                return self.getTypedRuleContext(ImpLanguageParser.AexprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBgt" ):
                listener.enterBgt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBgt" ):
                listener.exitBgt(self)


    class BeqContext(BexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.BexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def aexpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ImpLanguageParser.AexprContext)
            else:
                return self.getTypedRuleContext(ImpLanguageParser.AexprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBeq" ):
                listener.enterBeq(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBeq" ):
                listener.exitBeq(self)


    class BnotContext(BexprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.BexprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def bexpr(self):
            return self.getTypedRuleContext(ImpLanguageParser.BexprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBnot" ):
                listener.enterBnot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBnot" ):
                listener.exitBnot(self)



    def bexpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ImpLanguageParser.BexprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_bexpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = ImpLanguageParser.BcstContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 31
                _la = self._input.LA(1)
                if not(_la==25 or _la==26):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 2:
                localctx = ImpLanguageParser.BleContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 32
                self.aexpr(0)
                self.state = 33
                self.match(ImpLanguageParser.T__4)
                self.state = 34
                self.aexpr(0)
                pass

            elif la_ == 3:
                localctx = ImpLanguageParser.BltContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 36
                self.aexpr(0)
                self.state = 37
                self.match(ImpLanguageParser.T__5)
                self.state = 38
                self.aexpr(0)
                pass

            elif la_ == 4:
                localctx = ImpLanguageParser.BgeContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 40
                self.aexpr(0)
                self.state = 41
                self.match(ImpLanguageParser.T__6)
                self.state = 42
                self.aexpr(0)
                pass

            elif la_ == 5:
                localctx = ImpLanguageParser.BgtContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 44
                self.aexpr(0)
                self.state = 45
                self.match(ImpLanguageParser.T__7)
                self.state = 46
                self.aexpr(0)
                pass

            elif la_ == 6:
                localctx = ImpLanguageParser.BeqContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 48
                self.aexpr(0)
                self.state = 49
                self.match(ImpLanguageParser.T__8)
                self.state = 50
                self.aexpr(0)
                pass

            elif la_ == 7:
                localctx = ImpLanguageParser.BnotContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 52
                self.match(ImpLanguageParser.T__9)
                self.state = 53
                self.bexpr(4)
                pass

            elif la_ == 8:
                localctx = ImpLanguageParser.BparContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 54
                self.match(ImpLanguageParser.T__2)
                self.state = 55
                self.bexpr(0)
                self.state = 56
                self.match(ImpLanguageParser.T__3)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 68
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 66
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                    if la_ == 1:
                        localctx = ImpLanguageParser.BandContext(self, ImpLanguageParser.BexprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_bexpr)
                        self.state = 60
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 61
                        self.match(ImpLanguageParser.T__10)
                        self.state = 62
                        self.bexpr(4)
                        pass

                    elif la_ == 2:
                        localctx = ImpLanguageParser.BorContext(self, ImpLanguageParser.BexprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_bexpr)
                        self.state = 63
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 64
                        self.match(ImpLanguageParser.T__11)
                        self.state = 65
                        self.bexpr(3)
                        pass

             
                self.state = 70
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ImpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ImpLanguageParser.RULE_imp

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AffContext(ImpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.ImpContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(ImpLanguageParser.ID, 0)
        def aexpr(self):
            return self.getTypedRuleContext(ImpLanguageParser.AexprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAff" ):
                listener.enterAff(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAff" ):
                listener.exitAff(self)


    class ErrContext(ImpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.ImpContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterErr" ):
                listener.enterErr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitErr" ):
                listener.exitErr(self)


    class AssertContext(ImpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.ImpContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def bexpr(self):
            return self.getTypedRuleContext(ImpLanguageParser.BexprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssert" ):
                listener.enterAssert(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssert" ):
                listener.exitAssert(self)


    class LoopContext(ImpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.ImpContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def bexpr(self):
            return self.getTypedRuleContext(ImpLanguageParser.BexprContext,0)

        def imp(self):
            return self.getTypedRuleContext(ImpLanguageParser.ImpContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLoop" ):
                listener.enterLoop(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLoop" ):
                listener.exitLoop(self)


    class SkipContext(ImpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.ImpContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSkip" ):
                listener.enterSkip(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSkip" ):
                listener.exitSkip(self)


    class IteContext(ImpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.ImpContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def bexpr(self):
            return self.getTypedRuleContext(ImpLanguageParser.BexprContext,0)

        def imp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ImpLanguageParser.ImpContext)
            else:
                return self.getTypedRuleContext(ImpLanguageParser.ImpContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIte" ):
                listener.enterIte(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIte" ):
                listener.exitIte(self)


    class SeqContext(ImpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ImpLanguageParser.ImpContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def imp(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ImpLanguageParser.ImpContext)
            else:
                return self.getTypedRuleContext(ImpLanguageParser.ImpContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSeq" ):
                listener.enterSeq(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSeq" ):
                listener.exitSeq(self)



    def imp(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ImpLanguageParser.ImpContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_imp, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [13]:
                localctx = ImpLanguageParser.SkipContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 72
                self.match(ImpLanguageParser.T__12)
                pass
            elif token in [14]:
                localctx = ImpLanguageParser.ErrContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 73
                self.match(ImpLanguageParser.T__13)
                pass
            elif token in [28]:
                localctx = ImpLanguageParser.AffContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 74
                self.match(ImpLanguageParser.ID)
                self.state = 75
                self.match(ImpLanguageParser.T__14)
                self.state = 76
                self.aexpr(0)
                pass
            elif token in [16]:
                localctx = ImpLanguageParser.AssertContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 77
                self.match(ImpLanguageParser.T__15)
                self.state = 78
                self.bexpr(0)
                pass
            elif token in [17]:
                localctx = ImpLanguageParser.IteContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 79
                self.match(ImpLanguageParser.T__16)
                self.state = 80
                self.bexpr(0)
                self.state = 81
                self.match(ImpLanguageParser.T__17)
                self.state = 82
                self.imp(0)
                self.state = 83
                self.match(ImpLanguageParser.T__18)
                self.state = 84
                self.imp(0)
                self.state = 85
                self.match(ImpLanguageParser.T__19)
                pass
            elif token in [21]:
                localctx = ImpLanguageParser.LoopContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 87
                self.match(ImpLanguageParser.T__20)
                self.state = 88
                self.bexpr(0)
                self.state = 89
                self.match(ImpLanguageParser.T__21)
                self.state = 90
                self.imp(0)
                self.state = 91
                self.match(ImpLanguageParser.T__22)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 100
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = ImpLanguageParser.SeqContext(self, ImpLanguageParser.ImpContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_imp)
                    self.state = 95
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 96
                    self.match(ImpLanguageParser.T__23)
                    self.state = 97
                    self.imp(2) 
                self.state = 102
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.aexpr_sempred
        self._predicates[2] = self.bexpr_sempred
        self._predicates[3] = self.imp_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def aexpr_sempred(self, localctx:AexprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         

    def bexpr_sempred(self, localctx:BexprContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 2)
         

    def imp_sempred(self, localctx:ImpContext, predIndex:int):
            if predIndex == 4:
                return self.precpred(self._ctx, 1)
         




