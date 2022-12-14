#!/usr/bin/env python

"""Exposes classes and functions to perform the lexical
analysis of the models generated by SMT solvers.
"""

"""See the LICENSE file, located in the root directory of
the source distribution and
at http://verifun.eecs.berkeley.edu/gametime/about/LICENSE,
for details on the GameTime license and authors.
"""


import ply.lex as lex

from gametime.defaults import config
from gametime.gametimeError import GameTimeError


class ModelLexer(object):
    """Performs the lexical analysis of the models generated by SMT solvers."""

    def __init__(self):
        #: Underlying lexer (object of the `Lexer` class).
        self.plyLexer = None

        self._addRulesFromConfig()

    def _addRulesFromConfig(self):
        """Adds the rules for tokens that depend
        on the GameTime configuration.
        """
        ModelLexer.t_CONSTRAINT = config.IDENT_CONSTRAINT
        ModelLexer.t_EFC = config.IDENT_EFC
        ModelLexer.t_TEMPINDEX = config.IDENT_TEMPINDEX

    # List of token names.
    tokens = ("LANGLE", "RANGLE", "AT",
              "CONSTRAINT", "EFC", "TEMPINDEX",
              "NUMBER", "WORD")

    # Rules for the tokens.
    t_LANGLE = r"\<"
    t_RANGLE = r"\>"
    t_AT = r"@"

    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    t_WORD = r"\w+"

    # Rule that allows us to track line numbers.
    # From http://www.dabeaz.com/ply/ply.html.
    def t_newline(self, t):
        r"(\n|\r\n)+"
        t.lexer.lineno += len(t.value)

    # Rules to ignore characters.
    t_ignore = " \t\f\v"

    # Error handling rule.
    def t_error(self, t):
        errMsg = "Illegal character `%s'" % t.value[0]
        raise GameTimeError(errMsg)

    def build(self, **kwargs):
        """
        Builds this lexer. This method is an interface to the `lex'
        function of the `lex' module, which builds the underlying lexer.
        The keyworded arguments accepted are thus the same as those
        of the `lex' function.

        @param kwargs Keyworded, variable-length argument list that will
        be passed to the `lex' function.
        """
        self._addRulesFromConfig()
        self.plyLexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        """
        Stores a new string in this lexer. This method is an interface to
        the `input' function of the underlying lexer.

        @param data New string to store in this lexer.
        """
        self.plyLexer.input(data)

    def token(self):
        """
        Gets the new token from this lexer. This method is an interface to
        the `token' function of the underlying lexer.

        @retval New token from this lexer.
        """
        return self.plyLexer.token()

    def __getstate__(self):
        """
        Returns the pickled representation of a ModelLexer object.

        @retval Pickled representation of a ModelLexer object.
        """
        objectDict = self.__dict__.copy()
        if "plyLexer" in objectDict:
            del objectDict["plyLexer"]
        return objectDict

    def __setstate__(self, pickled):
        """
        Unpickles the provided pickled representation of a ModelLexer object.

        @param pickled Pickled representation of a ModelLexer object.
        """
        self.__dict__.update(pickled)
        self.plyLexer = None
