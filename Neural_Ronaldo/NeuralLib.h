//************************************************************************************************
//* UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL (UFRGS) - Campus do Vale                          **
//* Doutorado em Ciencia da Computacao - PPGC                                                   **
//* Doutorando: Milton Roberto Heinen - 00145752                                                **
//* Orientador: Paulo Martins Engel                                                             **
//* Simulador de redes neurais com o algoritmo backpropagation padrao (sem momentum)            **
//************************************************************************************************
#ifndef NEURALLIB_H
#define NEURALLIB_H


//************************************** Prototipos **********************************************
int InicializarAnn(const char *szArqPesos);
void printNeuralNet();
void AtivarAnn(const double *pdEntrada, double *pdSaidaObtida);
void FinalizarAnn();

#endif
