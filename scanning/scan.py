#!/usr/bin/env python
# coding: utf-8

# In[3]:


import enum
import sys

class Lexeme:
    def __init__(self, tokenText, tokenType):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers
        self.type = tokenType   # The TokenType that this token is classified as
    
    def KeywordChecker(tokenText):
        for type in TOKEN:
            if type.name == tokenText and type.value >= 100 and type.value < 200:
                return type
        return None
    
class TOKEN(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords
    PRINT = 101
    INPUT = 102
    LET = 103
    IF = 104
    THEN = 105
    ENDIF = 106
    WHILE = 107
    REPEAT = 108
    ENDWHILE = 109
    # Operators
    PLUS = 201
    MINUS = 202
    ASTERISK = 203
    SLASH = 204
    EQUAL = 205
    EQUALEQUAL = 206
    NOTEQUAL = 207
    GT = 208
    LT = 209
    GTEQUAL = 210
    LTEQUAL = 211
    
class Scanner:
    def __init__(self, input):
        self.INPUT = input + '\n' 
        self.Char = '' # Current character in the string
        self.Pos = -1 # Current position in the string
        self.nextChar()
    
    # Process the next character
    def nextChar(self):
        self.Pos += 1
        if self.Pos >= len(self.INPUT):
            self.Char = '\E' # EOF(end-of-file)
        else:
            self.Char = self.INPUT[self.Pos]
    
    # Return the lookahead character
    def glimpse(self):
        if self.Pos + 1 >= len(self.INPUT):
            return '\E'
        return self.INPUT[self.Pos+1]
    
     # Invalid token found, print error message and exit
    def errorMessage(self, message):
        sys.exit("Lexing error. "+ message)
    
    # Skip whitespace except newlines, which we will use to indicate the end of a statement
    def skipWhitespace(self):
        while self.Char == ' 'or self.Char =='\t' or self.Char =='\r':
            self.nextChar()
    
    # Skip comments in the code
    def skipComment(self):
        if self.Char == "#":
            while self.Char != '\n':
                self.nextChar()
    
    # Return the next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None
        
        if self.Char == '+':
            token = Lexeme(self.Char, TOKEN.PLUS)
        elif self.Char == '-':
            token = Lexeme(self.Char, TOKEN.MINUS)
        elif self.Char == '*':
            token = Lexeme(self.Char, TOKEN.ASTERISK)
        elif self.Char == '/':
            token = Lexeme(self.Char, TOKEN.SLASH)
        elif self.Char == '\n':
            token = Lexeme(self.Char, TOKEN.NEWLINE)
        elif self.Char == '\E':
            token = Lexeme(self.Char, TOKEN.EOF)
        elif self.Char == '=':
            if self.glimpse() == '=':
                lastChar = self.Char
                self.nextChar()
                token = Lexeme(lastChar + self.Char, TOKEN.EQUALEQUAL)
            else:
                token = Lexeme(self.Char, TOKEN.EQUAL)
        elif self.Char == '>':
            if self.glimpse() == '=':
                lastChar = self.Char
                self.nextChar()
                token = Lexeme(lastChar + self.Char, TOKEN.GTEQUAL)
            else:
                token = Lexeme(self.Char, TOKEN.GT) 
        elif self.Char == '<':
            if self.glimpse() == '=':
                lastChar = self.Char
                self.nextChar()
                token = Lexeme(lastChar + self.Char, TOKEN.LTEQUAL)
            else:
                token = Lexeme(self.Char, TOKEN.LT)
        elif self.Char == '!':
            if self.glimpse() == '=':
                lastChar = self.Char
                self.nextChar()
                token = Lexeme(lastChar + self.Char, TOKEN.NOTEQUAL)
            else:
                self.errorMessage("Expected !=, got !" + self.glimpse())
        elif self.Char == '"':
            self.nextChar()
            startPos = self.Pos
            
            while self.Char != '"':
                if self.Char == '\r' or self.Char == '\n' or self.Char == '\t' or self.Char == '\\' or self.Char == '%':
                    self.errorMessage("Illegal character in string")
                self.nextChar()
                
            tokText = self.INPUT[startPos : self.Pos]
            token = Lexeme(tokText, TOKEN.STRING)
        elif self.Char.isdigit():
            startPos = self.Pos
            while self.glimpse().isdigit():
                self.nextChar()
            if self.glimpse() == '.':
                self.nextChar()
                if not self.glimpse().isdigit():
                    self.errorMessage("Illegal character in number")
                while self.glimpse().isdigit():
                    self.nextChar()
            tokText = self.INPUT[startPos : self.Pos + 1]
            token = Lexeme(tokText, TOKEN.NUMBER)
            
        elif self.Char.isalpha():
            startPos = self.Pos
            while self.glimpse().isalnum():
                self.nextChar()
            tokText = self.INPUT[startPos : self.Pos + 1]
            keyword = Lexeme.KeywordChecker(tokText)
            if keyword == None:
                token = Lexeme(tokText, TOKEN.IDENT)
            else:
                token = Lexeme(tokText, keyword)
        else:
            # Unknown token!
            self.errorMessage("Unknown token: "+ self.Char)
    
        
        self.nextChar()
        return token
            

