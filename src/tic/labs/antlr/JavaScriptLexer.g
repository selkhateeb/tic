lexer grammar JavaScriptLexer;

Comment
    :   SingleLineComment
    |   MultiLineComment
    ;

fragment
SingleLineComment
	:	'//' ~('\n'|'\r')* LineTerminator
	;

fragment
MultiLineComment
    : '/*' ( options {greedy=false;} : . )* '*/'
    ;
    
WhiteSpace  :   
	( ' '
        | '\t'
        )
        ;
LineTerminator
	: '\r'? '\n'
	| '\r'
	;

String
    :  DoubleQuoteString
    | SingleQuoteString
    ;

fragment
DoubleQuoteString
	: '"' ( EscapeSequence | ~('\\'|'"') )* '"'
	;
fragment
SingleQuoteString
	:	'\'' ( EscapeSequence | ~('\\'|'\'') )* '\''
	;

ReservedKeywords
	: NullLeteral
	| BooleanLiteral
	| FutureReservedWord
	| Keyword;

fragment FutureReservedWord
	:	
	CLASS
	|ENUM
	|EXTENDS
	|SUPER
	|CONST
	|EXPORT
	|IMPORT;

fragment Keyword :
	BREAK
	|CASE
	|CATCH
	|CONTINUE
	|DEBUGGER
	|DEFAULT
	|DELETE
	|DO
	|ELSE
	|FINALLY
	|FOR
	|FUNCTION
	|IF
	|IN
	|INSTANCEOF
	|TYPEOF
	|NEW
	|VAR
	|RETURN
	|VOID
	|SWITCH
	|WHILE
	|THIS
	|WITH
	|THROW
	|TRY
	;
//Future Reserved Words
fragment CLASS:'class';
fragment ENUM:'enum';
fragment EXTENDS:'extends';
fragment SUPER:'super';
fragment CONST:'const';
fragment EXPORT:'export';
fragment IMPORT:'import';
	
// Reserved Words
fragment BREAK:'break';
fragment CASE:'case';
fragment CATCH:'catch';
fragment CONTINUE:'continue';
fragment DEBUGGER:'debugger';
fragment DEFAULT:'default';
fragment DELETE:'delete';
fragment DO:'do';
fragment ELSE:'else';
fragment FINALLY:'finally';
fragment FOR:'for';
fragment FUNCTION:'function';
fragment IF:'if';
fragment IN:'in';
fragment INSTANCEOF:'instanceof';
fragment TYPEOF:'typeof';
fragment NEW:'new';
fragment VAR:'var';
fragment RETURN:'return';
fragment VOID:'void';
fragment SWITCH:'switch';
fragment WHILE:'while';
fragment THIS:'this';
fragment WITH:'with';
fragment THROW:'throw';
fragment TRY:'try';
fragment NullLeteral: 'null';
fragment BooleanLiteral: TRUE|FALSE;
fragment TRUE: 'true';
fragment FALSE: 'false';	

	
Identifier  :	('a'..'z'|'A'..'Z'|'_'|'$') ('a'..'z'|'A'..'Z'|'0'..'9'|'_'|'$')*
    ;


NumericLiteral
	: DecimalLitral
	| HexIntegerLiteral;

fragment DecimalLitral
	: ('+'|'-')? ('0'..'9')+ ;

fragment HexIntegerLiteral : ('0x'|'0X') HexDigit+;

fragment
HexDigit : ('0'..'9'|'a'..'f'|'A'..'F') ;


fragment
EscapeSequence
    :   '\\' ('b'|'t'|'n'|'f'|'r'|'v'|'\"'|'\''|'\\')
    |   UnicodeEscapeSequence
    |   HexEscapeCharacter
    ;

fragment
HexEscapeCharacter
	: '\\' 'x' HexDigit;

fragment
UnicodeEscapeSequence
    :   '\\' 'u' HexDigit HexDigit HexDigit HexDigit
    ;
    

