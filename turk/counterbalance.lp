% counterbalance.lp
% Solver for counterbalanced study design

%#const items = 60.

count(X) :- X = { character(C) }.

% Study size parameters:
#const group_size = 5.
#const per_item = 7.

%#const groups = (items / group_size) * per_item.

group_count(N) :- count(X), N = (X * per_item) / group_size.

group(1..N) :- group_count(N).

pronoun(C, he) :- gender(C, male).
pronoun(C, he) :- gender(C, ambiguous_male).
pronoun(C, she) :- gender(C, female).
pronoun(C, she) :- gender(C, ambiguous_female).

gender_value(V) :- gender(C, V).
origin_value(V) :- origin(C, V).
game_value(V) :- game(C, V).
pronoun_value(V) :- pronoun(C, V).

% five items per group
group_size = { assigned(G, C) : character(C) } :- group(G).

% no group is homogeneous in terms of character genders, pronouns, origins, or
% games:
:- group(G), 1 = { gender_value(V): assigned(G, C), gender(C, V) }.
:- group(G), 1 = { pronoun_value(V): assigned(G, C), pronoun(C, V) }.
:- group(G), 1 = { origin_value(V): assigned(G, C), origin(C, V) }.
:- group(G), 1 = { game_value(V): assigned(G, C), game(C, V) }.

% each item appears in 'per_item' groups
per_item = { assigned(G, C) : group(G) } :- character(C).

#show assigned/2.

% Pairs handling:

exists(p(A, B)) :- character(A), character(B), A < B.

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
