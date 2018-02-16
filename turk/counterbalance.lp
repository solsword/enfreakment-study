% counterbalance.lp
% Solver for counterbalanced study design

%#const items = 65.

count(X) :- X = { character(C, N) }.

% Study size parameters:
#const group_size = 5.
#const per_item = 7.

%#const groups = (items / group_size) * per_item.

group_count(N) :- count(X), N = (X * per_item) / group_size.

group(1..N) :- group_count(N).

item(X) :- character(C, X).
name(C) :- character(C, X).

gender_value(V) :- gender(C, V).
origin_value(V) :- origin(C, V).
game_value(V) :- game(C, V).

% five items per group
group_size = { assigned(G, C) : name(C) } :- group(G).

% no group is homogeneous in terms of character genders, origins, or games:
:- group(G), 1 = { gender_value(V): assigned(G, C), gender(C, V) }.
:- group(G), 1 = { origin_value(V): assigned(G, C), origin(C, V) }.
:- group(G), 1 = { game_value(V): assigned(G, C), game(C, V) }.

% each item appears in 'per_item' groups
per_item = { assigned(G, C) : group(G) } :- name(C).

#show assigned/2.

% Pairs handling:

exists(p(A, B)) :- name(A), name(B), A < B.

pair(G, p(A, B)) :- assigned(G, A), assigned(G, B), A < B.

appears(p(A, B)) :- pair(G, p(A, B)).

% Don't pair Akuma from SFV with Akuma from Tekken!
:- appears(p(akuma,akumat7)).

% Count the occurances of each pair:
count(p(A, B), X) :-
  exists(p(A, B)),
  X = { pair(G, p(A, B)) : pair(G, p(A, B)) }.

% Ensure each pair appears 0--1 times:
:- count(p(A, B), X), X > 1.

#show count/2.

% Ensure each pair appears 1--3 times:
%:- count(p(A, B), X), X > 1.
%:- count(p(A, B), X), X > 3.

%% Ensure each pair appears exactly once:
%%:- count(p(A, B), X), X != 1.
%
%
%%#show pair/2.
%%#show exists/1.
%
%%tpc(Y) :- Y = #sum { X : count(p(A, B), X) }.
%%#show tpc/1.
%
%% Triples handling:
%
%exists(t(A, B, C)) :- item(A), item(B), item(C), A < B, B < C.
%
%triple(G, t(A, B, C)) :-
%  assigned(G, A),
%  assigned(G, B),
%  assigned(G, C),
%  A < B,
%  B < C.
%
%appears(t(A, B, C)) :- triple(G, t(A, B, C)).
%
%% Every possible triple should appear at most once:
%%:- exists(t(A, B, C)), not appears(t(A, B, C)).
%:- triple(G1, t(A, B, C)), triple(G2, t(A, B, C)), G1 != G2.
