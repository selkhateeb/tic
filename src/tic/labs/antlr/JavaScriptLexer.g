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
    
StringLiteral
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

RegularExpressionLiteral
    : '/' ~('/'|'*'|LineTerminator) ~('/'|LineTerminator)* '/' Identifier*
    ;

WhiteSpace  :   
	( ' '
        | '\t'
        )
        ;
LineTerminator
	: ('\n'
	| '\r')
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

Punctuator:
CurlyBracketOpen
| CurlyBracketClose
| RoundBracketOpen
| RoundBracketClose
| SquareBracketOpen
| SquareBracketClose
| Dot
| Semicolon
| Comma
| LessThan
| GreaterThan
| LessThanEqual
| GreaterThanEqual
| EqualEqual
| ExclamationEqual
| EqualEqualEqual
| ExclamationEqualEqual
| Plus
| Minus
| Asterisk
| Percent
| PlusPlus
| MinusMinus
| LessThanLessThan
| GreaterThanGreaterThan
| GreaterThanGreaterThanGreaterThan
| Ampersand
| Pipe
| Caret
| Exclamation
| Tilde
| AmpersandAmpersand
| PipePipe
| QuestionMark
| Colon
| Equal
| PlusEqual
| MinusEqual
| AsteriskEqual
| PercentEqual
| LessThanLessThanEqual
| GreaterThanGreaterThanEqual
| GreaterThanGreaterThanGreaterThanEqual
| AmpersandEqual
| PipeEqual
| CaretEqual
| Divide
| DivideEqual
;
fragment CurlyBracketOpen: '{';
fragment CurlyBracketClose: '}';
fragment RoundBracketOpen: '(';
fragment RoundBracketClose: ')';
fragment SquareBracketOpen: '[';
fragment SquareBracketClose: ']';
fragment Dot: '.';
fragment Semicolon: ';';
fragment Comma: ',';
fragment LessThan: '<';
fragment GreaterThan: '>';
fragment LessThanEqual: LessThan Equal;
fragment GreaterThanEqual: GreaterThan Equal;
fragment EqualEqual: Equal Equal;
fragment ExclamationEqual: Exclamation Equal;
fragment EqualEqualEqual: Equal Equal Equal;
fragment ExclamationEqualEqual: Exclamation Equal Equal;
fragment Plus: '+';
fragment Minus: '-';
fragment Asterisk: '*';
fragment Percent: '%';
fragment PlusPlus: '++';
fragment MinusMinus: Minus Minus;
fragment LessThanLessThan: LessThan LessThan;
fragment GreaterThanGreaterThan: GreaterThan GreaterThan;
fragment GreaterThanGreaterThanGreaterThan: GreaterThan GreaterThan GreaterThan;
fragment Ampersand: '&';
fragment Pipe: '|';
fragment Caret: '^';
fragment Exclamation: '!';
fragment Tilde: '~';
fragment AmpersandAmpersand: Ampersand Ampersand;
fragment PipePipe: Pipe Pipe;
fragment QuestionMark: '?';
fragment Colon: ':';
fragment Equal: '=';
fragment PlusEqual: Plus Equal;
fragment MinusEqual: Minus Equal;
fragment AsteriskEqual: Asterisk Equal;
fragment PercentEqual: Percent Equal;
fragment LessThanLessThanEqual: LessThanLessThan Equal;
fragment GreaterThanGreaterThanEqual: GreaterThanGreaterThan Equal;
fragment GreaterThanGreaterThanGreaterThanEqual: GreaterThanGreaterThanGreaterThan Equal;
fragment AmpersandEqual: Ampersand Equal;
fragment PipeEqual: Pipe Equal;
fragment CaretEqual: Caret Equal;
fragment Divide: '/';
fragment DivideEqual: Divide Equal;


