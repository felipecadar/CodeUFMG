all:
	flex -d src/mlm.lex
	yacc -d src/mlm.yacc
	-mv lex.yy.c y.tab.* build/
	cc -o bin/lexer build/lex.yy.c src/simb.c -lfl
	cc -o bin/analyzer build/lex.yy.c build/y.tab.c -ly -lfl
	# cc -o bin/frontend build/lexer.c build/semantic.c src/symtab.c -ly -lfl
	# javac src/translator.java -d bin

clean:
	rm bin/lexer

