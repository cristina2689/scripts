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

@r_match@
expression r.e2;
identifier get_string.tdres;
@@
(
- printf(tdres)
+ fprintf(stderr, tdres)
|
- printf(tdres, e2)
+ fprintf(stderr, tdres, e2)
)
