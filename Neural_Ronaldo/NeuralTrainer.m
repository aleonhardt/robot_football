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
net= newff([0 1000; -pi pi; -pi pi], [10 10 2], {'logsig', 'tansig', 'purelin'},'trainlm');
net.trainParam.epochs = 400;
a = sim(net, ent');
net=train(net, ent', saidas');
out=sim(net, ent');

weight = net.IW{1};

first_layer_weights = net.IW{1};
second_layer_weights = net.LW{2};
output_layer_weights = net.LW{6};
first_layer_weights = first_layer_weights*
second_layer_weights = second_layer_weights*
output_layer_weights = output_layer_weights*

dlmwrite('ronaldo_weights.nrl',first_layer_weights,'delimiter',' ');
file = fopen('ronaldo_weights.nrl','at');
fprintf(file, '***\n');
fclose(file)
dlmwrite('ronaldo_weights.nrl',second_layer_weights,'delimiter',' ','-append');
file = fopen('ronaldo_weights.nrl','at');
fprintf(file, '***\n');
fclose(file)
dlmwrite('ronaldo_weights.nrl',output_layer_weights,'delimiter',' ','-append');

