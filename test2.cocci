@r@
expression e1, e2, stdout;
@@
(printf(e1);
|
printf(e1, e2);
|
fprintf(stdout, e1);
|
fprintf(stdout, e1, e2);
)

@script: python get_string@
e << r.e1;
tdres;
@@
if 'could not' in e.lower() or 'fail' in e.lower() \
or 'problem' in e.lower() or 'not set' in e.lower():
	coccinelle.tdres = e
else:
	cocci.include_match(False)

@r_match@
expression r.stdout, r.e1, r.e2;
identifier get_string.tdres;
@@
(
- printf(e1);
+ fprintf(stderr, tdres);
|
- printf(e1, e2);
+ fprintf(stderr, tdres, e2);
|
- fprintf(stdout, e1)
+ fprintf(stderr, tdres)
|
- fprintf(stdout, e1, e2)
+ fprintf(stderr, tdres, e2)
)
