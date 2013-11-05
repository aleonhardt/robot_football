%Aprende a superficie de transferencia de um controlador fuzzy por bkp
%utiliza funções do nntoolbox
clear;
close all; clc;
%arquivo com pontos da função a ser aprendida
fid=fopen('soccer.lrn', 'r');
[ball_distancev, ball_anglev, target_anglev, force_leftv, force_rightv] = textread('soccer.lrn', '%f %f %f %f %f');


%prepara entradas e saidas desejadas para a rede
ent=[ball_distancev ball_anglev target_anglev];
saidas=[force_leftv force_rightv];
%cria rede mlp
net= newff([0 1000; -180 180; -180 180], [6 7 5 2], {'tansig', 'tansig', 'tansig', 'purelin'},'trainlm');
net.trainParam.epochs = 500;
a = sim(net, ent');
net=train(net, ent', saidas');
out=sim(net, ent');


