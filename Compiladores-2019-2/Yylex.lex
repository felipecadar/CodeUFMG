%{ 
#include<stdlib.h>
#include<stdio.h>
#include "y.tab.h"
%}

DIGIT               [0-9]
LETTER              [A-zA-Z]
IDENTIFIER          {LETTER}({LETTER}|{DIGIT})*

RELOP               "="|"<"|"<="|">"|">="|"!="
ADDOP               "+"|"-"|"or"
MULOP               "*"|"/"|"div"|"mod"|"and"
SIGN                [+-]?

UNSIGNED_INTEGER    {DIGIT}+
SCALE_FACTOR        "E"{SIGN}{UNSIGNED_INTEGER}
UNSIGNED_REAL       {UNSIGNED_INTEGER}(("."{DIGIT}({DIGIT})*)?)(({SCALE_FACTOR})?)
INTEGER_CONSTANT    UNSIGNED_INTEGER
REAL_CONSTANT       UNSIGNED_REAL
CHAR_CONSTANT       "'"{LETTER}"'"

%%


program             {return PROGRAM;}
integer             {return INTEGER;}
real                {return REAL;}
boolean             {return BOOLEAN;}
char                {return CHAR;}
PROCEDURE           {return PROCEDURE;}
value               {return VALUE;}
reference           {return REFERENCE;}
begin               {return BEGIN;}
end                 {return END;}
if                  {return IF;}
then                {return THEN;}
else                {return ELSE;}
repeat              {return REPEAT;}
until               {return UNTIL;}
read                {return READ;}
write               {return WRITE;}
not                 {return NOT;}
false               {return TFALSE;}
true                {return TTRUE;}
[,]                 {return COLON;}
[;]                 {return SEMICOLON;}
[:]                 {return TWOPOINTS;}
[)]                 {return RPARENTHESES;}
[(]                 {return LPARENTHESES;}
":="                {return ATRIB;}
NOT                 {return NOT;}
{RELOP}             {return RELOP;}
{ADDOP}             {return ADDOP;}
{MULOP}             {return MULOP;}
{IDENTIFIER}        {return IDENTIFIER;}
{UNSIGNED_INTEGER}  {return UNSIGNED_INTEGER;}
{UNSIGNED_REAL}     {return UNSIGNED_REAL;}
{SIGN}              {return SIGN;}
{SCALE_FACTOR}      {return SCALE_FACTOR;}
{INTEGER_CONSTANT}  {return INTEGER_CONSTANT;}
{REAL_CONSTANT}     {return REAL_CONSTANT;}
{CHAR_CONSTANT}     {return CHAR_CONSTANT;}
\n                  {}
[ \t]+              {}    
%%
void yyerror(char const *error){
    printf("FAIL:%s\n",error);
}