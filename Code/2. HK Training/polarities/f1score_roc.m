%look at ROC curves and F1 scores
clear all; close all;

npts = 1000;
g1 = linspace(0,1,npts);  %Prob(X1>alpha)
g0 = linspace(0,1,npts);  %Pron(X0>alpha)
[G0,G1] = meshgrid(g1,g0);

N0 = 10; N1 = 100;
rho = N0/N1;
F1 = 2*G1./(G1+rho*G0+1);

figure
mesh(G0,G1,F1);
view([0 0 1]);
xlabel('False positive rate');
ylabel('True positive rate');
zlabel('F1 score');
colorbar