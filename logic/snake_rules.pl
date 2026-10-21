% Regras lógicas do ambiente Snake.
% Python fornece os fatos atuais; Prolog decide quais células são permitidas.

:- dynamic board_size/2.
:- dynamic obstacle/2.
:- dynamic snake_segment/2.

% Uma posição precisa estar dentro do tabuleiro.

inside(X, Y) :-
    board_size(Width, Height),
    MaxX is Width - 1,
    MaxY is Height - 1,
    between(0, MaxX, X),
    between(0, MaxY, Y).

% Obstáculos e segmentos do corpo bloqueiam a passagem.
blocked(X, Y) :- obstacle(X, Y).
blocked(X, Y) :- snake_segment(X, Y).

% A cabeça é o ponto de partida, não uma célula bloqueada para a busca.
% O agente considera os demais segmentos como bloqueios estáticos durante
% uma busca; ele recalcula o caminho depois de cada movimento.
valid_position(X, Y) :-
    inside(X, Y),
    \+ blocked(X, Y).

% Uma ação corresponde a uma célula ortogonalmente adjacente.
neighbor(X, Y, NX, Y) :- NX is X + 1.
neighbor(X, Y, NX, Y) :- NX is X - 1.
neighbor(X, Y, X, NY) :- NY is Y + 1.
neighbor(X, Y, X, NY) :- NY is Y - 1.

valid_transition(X, Y, NX, NY) :-
    neighbor(X, Y, NX, NY),
    valid_position(NX, NY).
