%Aprende a superficie de transferencia de um controlador fuzzy por bkp
%utiliza funções do nntoolbox
clear;
close all; clc;
%arquivo com pontos da função a ser aprendida
fid=fopen('soccer_yellow.lrn', 'r');
[ball_distancev, ball_anglev, target_anglev, force_leftv, force_rightv] = textread('soccer_yellow.lrn', '%f %f %f %f %f');


%prepara entradas e saidas desejadas para a rede
ent=[ball_distancev ball_anglev target_anglev];
saidas=[force_leftv force_rightv];
%cria rede mlp
entradas = 3;
primCamada = 10;
segCamada = 10;
saidasCamada = 2;
net= newff([0 1000; -pi pi; -pi pi], [primCamada segCamada saidasCamada], {'logsig', 'tansig', 'purelin'},'trainlm');
net.trainParam.epochs = 400;
a = sim(net, ent');
net=train(net, ent', saidas');
out=sim(net, ent');

weight = net.IW{1};

first_layer_weights = [net.IW{1} net.b{1}]; %%toda uma linha são os pesos de UM neurônio da camada (mais fácil de tratar)
second_layer_weights = [net.LW{2} net.b{2}];
output_layer_weights = [net.LW{6} net.b{3}];

%% escrever no início: 3 10 10 2 (entradas, prim camada, seg camada, saídas)
file = fopen('ronaldo_weights.nrl','w');
fprintf(file, '%d %d %d %d\n', entradas, primCamada, segCamada, saidasCamada);
fclose(file)
dlmwrite('ronaldo_weights.nrl',first_layer_weights,'delimiter',' ','-append');
file = fopen('ronaldo_weights.nrl','at');
fprintf(file, '***\n');
fclose(file)
dlmwrite('ronaldo_weights.nrl',second_layer_weights,'delimiter',' ','-append');
file = fopen('ronaldo_weights.nrl','at');
fprintf(file, '***\n');
fclose(file)
dlmwrite('ronaldo_weights.nrl',output_layer_weights,'delimiter',' ','-append');

