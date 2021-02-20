%{ /* Declarações */
#include <stdio.h>
%}

%token PROGRAM
%token INTEGER
%token REAL
%token BOOLEAN
%token CHAR
%token PROCEDURE

%token ATRIB
%token VALUE
%token REFERENCE
%token _BEGIN
%token END
%token IF
%token THEN
%token ELSE
%token REPEAT
%token UNTIL
%token READ
%token WRITE
%token TFALSE
%token TTRUE
%token SEMICOLON
%token LPARENTHESES
%token RPARENTHESES
%token TWOPOINTS
%token COLON
%token MINUS
%token ASSIGNOP
%token NOT
%token RELOP
%token ADDOP
%token MULOP
%token LETTER
%token DIGIT
%token IDENTIFIER
%token UNSIGNED_INTEGER
%token SIGN
%token SCALE_FACTOR
%token UNSIGNED_REAL
%token INTEGER_CONSTANT
%token REAL_CONSTANT
%token CHAR_CONSTANT

%%
program : PROGRAM IDENTIFIER SEMICOLON decl_list
compound_stmt
;
decl_list : decl_list SEMICOLON decl
| decl
;

decl : dcl_var
| dcl_proc
;
dcl_var : ident_list TWOPOINTS type
;
ident_list : ident_list COLON IDENTIFIER
| IDENTIFIER
;
type : INTEGER
| REAL
| BOOLEAN
| CHAR
;
dcl_proc : tipo_retornado PROCEDURE IDENTIFIER
espec_parametros corpo
;
tipo_retornado : INTEGER
| REAL
| BOOLEAN
| CHAR
| %empty/* empty */
;
corpo : TWOPOINTS decl_list SEMICOLON
compound_stmt id_return
;
id_return : IDENTIFIER
| %empty/* empty */
;

espec_parametros : LPARENTHESES lista_de_parametros RPARENTHESES
;
lista_de_parametros : parametro
| lista_de_parametros COLON parametro
;
parametro : modo type TWOPOINTS IDENTIFIER
;

modo : VALUE
| REFERENCE
;
compound_stmt : _BEGIN stmt_list END
;
stmt_list : stmt_list SEMICOLON stmt
| stmt
;
stmt : assign_stmt
| if_stmt
| repeat_stmt
| read_stmt
| write_stmt
| compound_stmt
| function_ref_par
;
assign_stmt : IDENTIFIER ASSIGNOP expr
;
if_stmt : IF cond THEN stmt
| IF cond THEN stmt ELSE stmt
;
cond : expr
;

repeat_stmt : REPEAT stmt_list UNTIL expr
;
read_stmt : READ LPARENTHESES ident_list RPARENTHESES
;
write_stmt : WRITE LPARENTHESES expr_list RPARENTHESES
;
expr_list : expr
| expr_list COLON expr
;
expr : Simple_expr
| Simple_expr RELOP Simple_expr
;

Simple_expr : term
| Simple_expr ADDOP term
;
term : factor_a
| term MULOP term
;
factor_a : MINUS factor
| factor
;
factor : IDENTIFIER
| constant
| LPARENTHESES expr RPARENTHESES
| NOT factor
| function_ref_par
;
function_ref_par : variable LPARENTHESES expr_list RPARENTHESES
;
variable : Simple_variable_or_proc
;
Simple_variable_or_proc : IDENTIFIER
;

constant : INTEGER_CONSTANT
| REAL_CONSTANT
| CHAR_CONSTANT
| boolean_constant
;
boolean_constant : TFALSE
| TTRUE
;
%%
int yywrap(){
return 1;
}
int main(){
yyparse();

return 1;
}