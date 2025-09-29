% -*- mode: prolog; coding: utf-8 -*-
% Ontology and reasoning rules

:- module(ontology, [
    % core facts
    class/1,
    is_a/2,
    part_of/2,
    has_property/2,
    instance_of/2,

    % helpers and metadata
    alias/2,
    resolve/2,
    practical_class/1,

    % derived relations
    is_a_transitive/2,
    part_of_transitive/2,
    has_part/2,
    has_part_transitive/2,
    connected/2,
    connected_names/2
]).

% -------------------------------
% Classes (>= 20)
% -------------------------------
class(entity).
class(physical_object).
class(organism).
class(animal).
class(plant).
class(vertebrate).
class(invertebrate).
class(mammal).
class(bird).
class(fish).
class(reptile).
class(amphibian).
class(arthropod).
class(canine).
class(feline).
class(dog).
class(wolf).
class(fox).
class(cat).
class(lion).
class(sparrow).
class(eagle).
class(salmon).
class(tuna).
class(snake).
class(lizard).
class(spider).
class(beetle).
class(oak).
class(rose).
class(body_part).
class(appendage).
class(tail).
class(leg).
class(wing).
class(head).
class(eye).
class(fur).
class(feather).
class(fin).
class(scale).
class(skin).

% -------------------------------
% is_a hierarchy (>= 4 levels along one chain)
% entity <- physical_object <- organism <- animal <- vertebrate <- mammal <- canine <- dog
% -------------------------------
is_a(physical_object, entity).
is_a(organism, physical_object).
is_a(animal, organism).
is_a(plant, organism).

is_a(vertebrate, animal).
is_a(invertebrate, animal).

is_a(mammal, vertebrate).
is_a(bird, vertebrate).
is_a(fish, vertebrate).
is_a(reptile, vertebrate).
is_a(amphibian, vertebrate).

is_a(arthropod, invertebrate).

is_a(canine, mammal).
is_a(feline, mammal).

is_a(dog, canine).
is_a(wolf, canine).
is_a(fox, canine).

is_a(cat, feline).
is_a(lion, feline).

is_a(sparrow, bird).
is_a(eagle, bird).

is_a(salmon, fish).
is_a(tuna, fish).

is_a(snake, reptile).
is_a(lizard, reptile).

is_a(spider, arthropod).
is_a(beetle, arthropod).

is_a(oak, plant).
is_a(rose, plant).

% Body parts taxonomy
is_a(body_part, physical_object).
is_a(appendage, body_part).
is_a(tail, appendage).
is_a(leg, appendage).
is_a(wing, appendage).
is_a(head, body_part).
is_a(eye, body_part).
is_a(fur, body_part).
is_a(feather, body_part).
is_a(fin, appendage).
is_a(scale, body_part).
is_a(skin, body_part).

% -------------------------------
% part_of facts (class-level)
% -------------------------------
% Generic body parts of vertebrates
part_of(head, vertebrate).
part_of(eye, head).
part_of(leg, vertebrate).
part_of(skin, vertebrate).

% Appendages by group
part_of(tail, mammal).
part_of(tail, reptile).
part_of(wing, bird).
part_of(fin, fish).

% Coverings / specific parts
part_of(feather, bird).
part_of(fur, mammal).
part_of(scale, reptile).

% -------------------------------
% has_property facts (third relation)
% -------------------------------
% Properties of parts
has_property(tail, fur).          % many mammal tails are furry
has_property(wing, feather).      % bird wings have feathers
has_property(snake, scale).       % snakes are covered with scales
has_property(fish, fin).          % fish have fins (also as parts)

% -------------------------------
% Instances (2+ per practical class)
% -------------------------------
% Define which classes are considered practical (leaf-like) for instance coverage
practical_class(dog).
practical_class(cat).
practical_class(wolf).
practical_class(fox).
practical_class(lion).
practical_class(sparrow).
practical_class(eagle).
practical_class(salmon).
practical_class(tuna).
practical_class(snake).
practical_class(lizard).
practical_class(spider).
practical_class(beetle).
practical_class(oak).
practical_class(rose).

% Instances for each practical class (at least two each)
instance_of(rex, dog).
instance_of(bim, dog).

instance_of(murka, cat).
instance_of(simba, cat).

instance_of(akela, wolf).
instance_of(ghost, wolf).

instance_of(alisa, fox).
instance_of(todd, fox).

instance_of(mufasa, lion).
instance_of(nala, lion).

instance_of(chirpy, sparrow).
instance_of(jack, sparrow).

instance_of(freedom, eagle).
instance_of(storm, eagle).

instance_of(silver, salmon).
instance_of(red, salmon).

instance_of(bluefin, tuna).
instance_of(yellowfin, tuna).

instance_of(kaa, snake).
instance_of(viper, snake).

instance_of(gecko, lizard).
instance_of(iguana, lizard).

instance_of(charlotte, spider).
instance_of(aragog, spider).

instance_of(scarab, beetle).
instance_of(ladybug, beetle).

instance_of(oak1, oak).
instance_of(oak2, oak).

instance_of(rose1, rose).
instance_of(rose2, rose).

% -------------------------------
% Ukrainian and English aliases for key terms
% -------------------------------
% alias(NameOrSynonym, CanonicalAtom).
alias('собака', dog).
alias('пес', dog).
alias(dog, dog).
alias('кіт', cat).
alias('кішка', cat).
alias(cat, cat).
alias('вовк', wolf).
alias(wolf, wolf).
alias('лисиця', fox).
alias(fox, fox).
alias('лев', lion).
alias(lion, lion).
alias('хвіст', tail).
alias(tail, tail).
alias('шерсть', fur).
alias(fur, fur).
alias('перо', feather).
alias(feather, feather).
alias('крило', wing).
alias(wing, wing).
alias('око', eye).
alias(eye, eye).
alias('голова', head).
alias(head, head).
alias('луска', scale).
alias(scale, scale).
alias('шкіра', skin).
alias(skin, skin).
alias('птах', bird).
alias(bird, bird).
alias('риба', fish).
alias(fish, fish).
alias('ссавець', mammal).
alias(mammal, mammal).
alias('хребетний', vertebrate).
alias(vertebrate, vertebrate).
alias('безхребетний', invertebrate).
alias(invertebrate, invertebrate).
alias('плазун', reptile).
alias(reptile, reptile).
alias('земноводне', amphibian).
alias(amphibian, amphibian).
alias('горобець', sparrow).
alias(sparrow, sparrow).
alias('орел', eagle).
alias(eagle, eagle).
alias('лосось', salmon).
alias(salmon, salmon).
alias('тунець', tuna).
alias(tuna, tuna).
alias('змія', snake).
alias(snake, snake).
alias('ящірка', lizard).
alias(lizard, lizard).
alias('павук', spider).
alias(spider, spider).
alias('жук', beetle).
alias(beetle, beetle).
alias('дуб', oak).
alias(oak, oak).
alias('троянда', rose).
alias(rose, rose).

% -------------------------------
% Helpers
% -------------------------------
% resolve(+NameOrAtom, -Canonical)
resolve(Name, Canonical) :-
    (   atom(Name)
    ->  alias(Name, Canonical)
    ;   string(Name)
    ->  atom_string(A, Name), alias(A, Canonical)
    ).

% -------------------------------
% Derived relations and reasoning
% -------------------------------
% Transitive closure of is_a
is_a_transitive(X, Y) :- is_a(X, Y).
is_a_transitive(X, Y) :- is_a(X, Z), is_a_transitive(Z, Y).

% part_of transitive over parts hierarchy and whole hierarchy
part_of_transitive(Part, Whole) :- part_of(Part, Whole).
part_of_transitive(Part, Whole) :- part_of(Part, Mid), part_of_transitive(Mid, Whole).
% Inherit parts down the subclass chain of the whole
part_of_transitive(Part, SubclassWhole) :-
    part_of(Part, Whole),
    is_a_transitive(SubclassWhole, Whole).
% Inherit parts up the subclass chain of the part
part_of_transitive(SubclassPart, Whole) :-
    is_a_transitive(SubclassPart, Part),
    part_of(Part, Whole).

% has_part as inverse of part_of
has_part(Whole, Part) :- part_of(Part, Whole).
% transitive has_part via chaining
has_part_transitive(Whole, Part) :- has_part(Whole, Part).
has_part_transitive(Whole, Part) :- has_part(Whole, Mid), has_part_transitive(Mid, Part).
% inherit has_part down subclass of Whole
has_part_transitive(SubclassWhole, Part) :-
    is_a_transitive(SubclassWhole, Whole),
    has_part(Whole, Part).
% inherit has_part up subclass of Part
has_part_transitive(Whole, SubclassPart) :-
    has_part(Whole, Part),
    is_a_transitive(SubclassPart, Part).

% Edges allowed for connectivity
edge(A, B) :- is_a(A, B).
edge(A, B) :- part_of(A, B).
edge(A, B) :- has_part(A, B).
edge(A, B) :- has_property(A, B).
edge(A, B) :- instance_of(A, B).

% To make connectivity powerful, also allow edges via transitive closures
edge_star(A, B) :- is_a_transitive(A, B).
edge_star(A, B) :- part_of_transitive(A, B).
edge_star(A, B) :- has_part_transitive(A, B).
edge_star(A, B) :- has_property(A, B).
edge_star(A, B) :- instance_of(A, B).

% Generic path search avoiding cycles
connected(A, B) :- connected(A, B, [A]).

connected(A, B, _) :- A == B, !.
connected(A, B, Visited) :-
    (   edge_star(A, C)
    ;   edge_star(C, A)  % allow undirected traversal for broader connectivity
    ),
    \+ member(C, Visited),
    connected(C, B, [C|Visited]).

% User-facing helper that accepts Ukrainian or English names or canonical atoms
connected_names(NameA, NameB) :-
    resolve(NameA, A),
    resolve(NameB, B),
    connected(A, B).

