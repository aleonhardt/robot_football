%Aprende a superficie de transferencia de um controlador fuzzy por bkp
%utiliza fun��es do nntoolbox
clear;
close all; clc;
%arquivo com pontos da fun��o a ser aprendida
fid=fopen('soccer_blue.lrn', 'r');
[ball_distancev, ball_anglev, target_anglev, force_leftv, force_rightv] = textread('soccer_yellow.lrn', '%f %f %f %f %f');


%prepara entradas e saidas desejadas para a rede
ent=[ball_distancev ball_anglev target_anglev];
saidas=[force_leftv force_rightv];
%cria rede mlp
entradas = 3;
primCamada = 22;
saidasCamada = 2;
net= newff([0 1000; -pi pi; -pi pi], [primCamada  saidasCamada], {'tansig', 'purelin'},'trainlm');
net.trainParam.epochs = 300;
a = sim(net, ent');
net=train(net, ent', saidas');
out=sim(net, ent');

weight = net.IW{1};

first_layer_weights = [net.IW{1} net.b{1}]; %%toda uma linha s�o os pesos de UM neur�nio da camada (mais f�cil de tratar)
second_layer_weights = [net.LW{2} net.b{2}];


% escrever no in�cio: 3 10 10 2 (entradas, prim camada, seg camada, sa�das)
file = fopen('ronaldo_weights.nrl','w');
fprintf(file, '%d %d %d \n', entradas, primCamada, saidasCamada);
fclose(file)
dlmwrite('ronaldo_weights.nrl',first_layer_weights,'delimiter',' ','-append');
file = fopen('ronaldo_weights.nrl','at');

dlmwrite('ronaldo_weights.nrl',second_layer_weights,'delimiter',' ','-append');
file = fopen('ronaldo_weights.nrl','at');



