% Post-processing for counterbalance.lp results

histo(X, N) :-
  count(p(AA, BB), X),
  N = { count(p(A, B), X) : count(p(A, B), X) }.

#show histo/2.

ctotal(Y) :-
  Y = #sum { X,A,B : count(p(A, B), X) }.

#show ctotal/1.

group(g(A, B, C, D, E)) :-
  assigned(G, A),
  assigned(G, B),
  assigned(G, C),
  assigned(G, D),
  assigned(G, E),
  A < B,
  B < C,
  C < D,
  D < E.

#show group/1.
