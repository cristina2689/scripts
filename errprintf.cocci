// This semantic script is used to replace occurences
// of printf(...) to fprintf(stderr, ...) whenever the
// message of printf() contains the word 'fail'.
//
// Target: Linux
// More info: http://coccinellery.org/

@r@
expression e1, e2;
@@
(printf(e1, e2);
|
printf(e1);
)

@script: python get_string@
e << r.e1;
tdres;
@@
if 'fail' in e.lower():
	print e
	coccinelle.tdres = e
else:
	cocci.include_match(False)

@r_match@
expression r.e1, r.e2;
identifier get_string.tdres;
@@
(
- printf(e1)
+ fprintf(stderr, tdres)
|
- printf(e1, e2)
+ fprintf(stderr, tdres, e2)
)
