/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

#ifndef YY_YY_Y_TAB_H_INCLUDED
# define YY_YY_Y_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    PROGRAM = 258,
    INTEGER = 259,
    REAL = 260,
    BOOLEAN = 261,
    CHAR = 262,
    PROCEDURE = 263,
    VALUE = 264,
    REFERENCE = 265,
    BEGIN = 266,
    END = 267,
    IF = 268,
    THEN = 269,
    ELSE = 270,
    REPEAT = 271,
    UNTIL = 272,
    READ = 273,
    WRITE = 274,
    TFALSE = 275,
    TTRUE = 276,
    SEMICOLON = 277,
    LPARENTHESES = 278,
    RPARENTHESES = 279,
    TWOPOINTS = 280,
    COLON = 281,
    MINUS = 282,
    ASSIGNOP = 283,
    NOT = 284,
    RELOP = 285,
    ADDOP = 286,
    MULOP = 287,
    LETTER = 288,
    DIGIT = 289,
    IDENTIFIER = 290,
    UNSIGNED_INTEGER = 291,
    SIGN = 292,
    SCALE_FACTOR = 293,
    UNSIGNED_REAL = 294,
    INTEGER_CONSTANT = 295,
    REAL_CONSTANT = 296,
    CHAR_CONSTANT = 297
  };
#endif
/* Tokens.  */
#define PROGRAM 258
#define INTEGER 259
#define REAL 260
#define BOOLEAN 261
#define CHAR 262
#define PROCEDURE 263
#define VALUE 264
#define REFERENCE 265
#define BEGIN 266
#define END 267
#define IF 268
#define THEN 269
#define ELSE 270
#define REPEAT 271
#define UNTIL 272
#define READ 273
#define WRITE 274
#define TFALSE 275
#define TTRUE 276
#define SEMICOLON 277
#define LPARENTHESES 278
#define RPARENTHESES 279
#define TWOPOINTS 280
#define COLON 281
#define MINUS 282
#define ASSIGNOP 283
#define NOT 284
#define RELOP 285
#define ADDOP 286
#define MULOP 287
#define LETTER 288
#define DIGIT 289
#define IDENTIFIER 290
#define UNSIGNED_INTEGER 291
#define SIGN 292
#define SCALE_FACTOR 293
#define UNSIGNED_REAL 294
#define INTEGER_CONSTANT 295
#define REAL_CONSTANT 296
#define CHAR_CONSTANT 297

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
