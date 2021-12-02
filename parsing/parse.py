#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from scan import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.symbols = set()    # Variables declared so far.
        
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.

    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind == self.curToken.type

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.type

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.type.name)
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    # Return true if the current token is a comparison operator.
    def isComparisonOperator(self):
        return self.checkToken(TOKEN.GT) or self.checkToken(TOKEN.GTEQUAL) or self.checkToken(TOKEN.LT) or self.checkToken(TOKEN.LTEQUAL) or self.checkToken(TOKEN.EQUALEQUAL) or self.checkToken(TOKEN.NOTEQUAL)
    
    def abort(self, message):
        sys.exit("Error. " + message)

    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        # Since some newlines are required in our grammar, need to skip the excess.
        while self.checkToken(TOKEN.NEWLINE):
            self.nextToken()

        # Parse all the statements in the program.
        while not self.checkToken(TOKEN.EOF):
            self.statement()
            
    def statement(self):

        # "PRINT" (expression | string)
        if self.checkToken(TOKEN.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(TOKEN.STRING):
                self.nextToken()
            else:
                self.expression()
                
        # "LET" ident "=" expression
        elif self.checkToken(TOKEN.LET):
            self.nextToken()

            #  Check if ident exists in symbol table. If not, declare it.
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(TOKEN.IDENT)
            self.match(TOKEN.EQUAL)
            self.expression()
            
        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.checkToken(TOKEN.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()
            
            self.match(TOKEN.THEN)
            self.nl()

            # Zero or more statements in the body.
            while not self.checkToken(TOKEN.ENDIF):
                self.statement()
                
            self.match(TOKEN.ENDIF)
            
        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(TOKEN.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparison()
            
            self.match(TOKEN.REPEAT)
            self.nl()
            
            # Zero or more statements in the loop body.
            while not self.checkToken(TOKEN.ENDWHILE):
                self.statement()
                
            self.match(TOKEN.ENDWHILE)
            
        # "INPUT" ident
        elif self.checkToken(TOKEN.INPUT):
            self.nextToken()

            #If variable doesn't already exist, declare it.
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(TOKEN.IDENT)

        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.type.name + ")")

        # Newline.
        self.nl()
        
    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print("COMPARISON")

        self.expression()
        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            print ("Comparison Operator- "+self.curToken.type.name)
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text)

        # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()
            
     # expression ::= term {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")

        self.term()
        # Can have 0 or more +/- and expressions.
        while self.checkToken(TOKEN.PLUS) or self.checkToken(TOKEN.MINUS):
            print ("Operator- "+self.curToken.type.name)
            self.nextToken()
            self.term()
    
     # term ::= unary {( "/" | "*" ) unary}
    def term(self):
        print("TERM")

        self.unary()
        # Can have 0 or more *// and expressions.
        while self.checkToken(TOKEN.ASTERISK) or self.checkToken(TOKEN.SLASH):
            print ("Operator- "+self.curToken.type.name)
            self.nextToken()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):
        print("UNARY")

        # Optional unary +/-
        if self.checkToken(TOKEN.PLUS) or self.checkToken(TOKEN.MINUS):
            print (self.curToken.type.name)
            self.nextToken()        
        self.primary()
        
    # primary ::= number | ident
    def primary(self):
        print("PRIMARY (" + self.curToken.text + ")")

        if self.checkToken(TOKEN.NUMBER): 
            self.nextToken()
        elif self.checkToken(TOKEN.IDENT):
            # Ensure the variable already exists.
            if self.curToken.text not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.curToken.text)
            self.nextToken()
        else:
            self.abort("Unexpected token at " + self.curToken.text)
            
    # nl ::= '\n'+
    def nl(self):
        print("NEWLINE")

        # Require at least one newline.
        self.match(TOKEN.NEWLINE)
        while self.checkToken(TOKEN.NEWLINE):
            self.nextToken()

