//************************************************************************************************
//* UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL (UFRGS) - Campus do Vale                          **
//* Doutorado em Ciencia da Computacao - PPGC                                                   **
//* Doutorando: Milton Roberto Heinen - 00145752                                                **
//* Orientador: Paulo Martins Engel                                                             **
//* Simulador de redes neurais com o algoritmo backpropagation padrao (sem momentum)            **
//************************************************************************************************

//*************************************** Includes ***********************************************
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "NeuralLib.h"


//************************************** Constantes **********************************************
#define MAX_LINHA 1024


//********************************** Variaveis globais *******************************************
static int iNumeroEntradas = 0;
static int iNumeroOcultosPrim = 0;
static int iNumeroOcultosSeg = 0;
static int iNumeroSaidas = 0;
static double **ppdPesoOcultoPrim = NULL;
static double **ppdPesoOcultoSeg = NULL;
static double *pdCampoOcultoPrim = NULL;
static double *pdCampoOcultoSeg = NULL;
static double **ppdPesoSaida = NULL;


//*************************************** Funcoes ************************************************
int InicializarAnn(const char *szArqPesos)
{
  char vcLinha[MAX_LINHA + 1];
  char *szPalavra = NULL;
  FILE* fp = NULL;
  int i, j;

  // Salva os pesos
  if ((fp = fopen(szArqPesos, "r")) == NULL)
    return 0;

  // Busca o numero de entradas, ocultos e saidas
  fgets(vcLinha, MAX_LINHA, fp);
  szPalavra = strtok(vcLinha, " ");
  iNumeroEntradas = atoi(szPalavra);
  szPalavra = strtok('\0', " ");
  iNumeroOcultosPrim = atoi(szPalavra);
  szPalavra = strtok('\0', " ");
  iNumeroOcultosSeg = atoi(szPalavra);
  szPalavra = strtok('\0', " ");
  iNumeroSaidas = atoi(szPalavra);
  if (iNumeroEntradas==0 || iNumeroOcultosPrim==0 || iNumeroOcultosSeg==0 || iNumeroSaidas==0)
    return 0;


  // Aloca memoria para a primeira camada oculta
  ppdPesoOcultoPrim = (double**) malloc(sizeof(double*) * iNumeroOcultosPrim);
  for (i = 0; i < iNumeroOcultosPrim; i++)
    ppdPesoOcultoPrim[i] = (double*) malloc(sizeof(double) * (iNumeroEntradas + 1));
  pdCampoOcultoPrim = (double*) malloc(sizeof(double) * iNumeroOcultosPrim);

    // Aloca memoria para a segunda camada oculta
  ppdPesoOcultoSeg = (double**) malloc(sizeof(double*) * iNumeroOcultosSeg);
  for (i = 0; i < iNumeroOcultosSeg; i++)
    ppdPesoOcultoSeg[i] = (double*) malloc(sizeof(double) * (iNumeroOcultosPrim + 1));
  pdCampoOcultoSeg = (double*) malloc(sizeof(double) * iNumeroOcultosSeg);

  // Aloca memoria para a camada de saida
  ppdPesoSaida = (double**) malloc(sizeof(double*) * iNumeroSaidas);
  for (i = 0; i < iNumeroSaidas; i++)
    ppdPesoSaida[i] = (double*) malloc(sizeof(double) * (iNumeroOcultosSeg + 1));

  // Carrega os pesos da primeira camada oculta
  for (i = 0; i < iNumeroOcultosPrim && !feof(fp); i++) {
    fgets(vcLinha, MAX_LINHA, fp);
    szPalavra = strtok(vcLinha, " ");
    for (j = 0; j <= iNumeroEntradas && szPalavra; j++) {
      ppdPesoOcultoPrim[i][j] = atof(szPalavra);
      szPalavra = strtok('\0', " ");
    }
    if (j <= iNumeroEntradas) {
      fclose(fp);
      return 0;
    }
  }
  if (i < iNumeroOcultosPrim) {
    fclose(fp);
    return 0;
  }
    fgets(vcLinha, MAX_LINHA, fp);
    if(strcmp(vcLinha, "***\n")!=0){
         fclose(fp);
    return 0;
  }

  // Carrega os pesos da segunda camada oculta
  for (i = 0; i < iNumeroOcultosSeg&& !feof(fp); i++) {
    fgets(vcLinha, MAX_LINHA, fp);
    szPalavra = strtok(vcLinha, " ");
    for (j = 0; j <= iNumeroOcultosPrim && szPalavra; j++) {
      ppdPesoOcultoSeg[i][j] = atof(szPalavra);
      szPalavra = strtok('\0', " ");
    }
    if (j <= iNumeroOcultosPrim ) {
      fclose(fp);
      return 0;
    }
  }
  if (i < iNumeroOcultosSeg) {
    fclose(fp);
    return 0;
  }

    fgets(vcLinha, MAX_LINHA, fp);
    if(strcmp(vcLinha, "***\n")!=0){
         fclose(fp);
    return 0;
  }
  // Carrega os pesos da camada de saida
  for (i = 0; i < iNumeroSaidas && !feof(fp); i++) {
    fgets(vcLinha, MAX_LINHA, fp);
    szPalavra = strtok(vcLinha, " ");
    for (j = 0; j <= iNumeroOcultosSeg && szPalavra; j++) {
      ppdPesoSaida[i][j] = atof(szPalavra);
      szPalavra = strtok('\0', " ");
    }
    if (j <= iNumeroOcultosSeg) {
      fclose(fp);
      return 0;
    }
  }
  fclose(fp);
  return (i < iNumeroSaidas ? 0 : 1);
}

void printNeuralNet()
{
    int i, j, k;
    for(i=0; i<iNumeroOcultosPrim; i++)
    {
        printf("[");
        for (j = 0; j <= iNumeroEntradas; j++)
        {
           printf("%8.2f ", ppdPesoOcultoPrim[i][j]);
        }
        printf("] ");
    }
    printf("\n\n\n\n");
    for (i = 0; i < iNumeroOcultosSeg; i++) {
            printf("[");
            for (j = 0; j <= iNumeroOcultosPrim; j++)
            {
                printf("%8.2f ", ppdPesoOcultoSeg[i][j]);
            }
            printf("] ");
    }
     printf("\n\n\n\n");
    for (i = 0; i < iNumeroSaidas; i++) {
            printf("[");
            for (j = 0; j <= iNumeroOcultosSeg; j++)
            {
                printf("%8.2f ", ppdPesoSaida[i][j]);
            }
            printf("] ");
    }
    printf("\n\n\n\n");
}

void AtivarAnn(const double *pdEntrada, double *pdSaidaObtida)
{
  register int i, j;

  // Ativa a primeira camada oculta
  for (i = 0; i < iNumeroOcultosPrim; i++) {
    pdCampoOcultoPrim[i] = ppdPesoOcultoPrim[i][iNumeroEntradas];
    for (j = 0; j < iNumeroEntradas; j++)
      pdCampoOcultoPrim[i] += pdEntrada[j] * ppdPesoOcultoPrim[i][j];
    pdCampoOcultoPrim[i] = 1 / (1 + exp(-pdCampoOcultoPrim[i])); //logsig
  }

   // Ativa a segunda camada oculta
  for (i = 0; i < iNumeroOcultosSeg; i++) {
    pdCampoOcultoSeg[i] = ppdPesoOcultoSeg[i][iNumeroOcultosPrim];
    for (j = 0; j < iNumeroOcultosPrim; j++)
      pdCampoOcultoSeg[i] += pdCampoOcultoPrim[j] * ppdPesoOcultoSeg[i][j];
    pdCampoOcultoSeg[i] = tanh(-pdCampoOcultoSeg[i]); //tansig
  }

  // Ativa as saidas lineares
  for (i = 0; i < iNumeroSaidas; i++) {
    pdSaidaObtida[i] = ppdPesoSaida[i][iNumeroOcultosSeg];
    for (j = 0; j < iNumeroOcultosSeg; j++)
      pdSaidaObtida[i] += pdCampoOcultoSeg[j] * ppdPesoSaida[i][j];
  }
}


void FinalizarAnn()
{
  int i;

  // Desaloca a memoria das camadas ocultas
  if (pdCampoOcultoPrim != NULL) {
    free(pdCampoOcultoPrim);
    pdCampoOcultoPrim = NULL;
  }
  if (pdCampoOcultoSeg != NULL) {
    free(pdCampoOcultoSeg);
    pdCampoOcultoSeg = NULL;
  }
  if (ppdPesoOcultoPrim != NULL) {
    for (i = 0; i < iNumeroOcultosPrim; i++) {
      if (ppdPesoOcultoPrim[i] != NULL) {
        free(ppdPesoOcultoPrim[i]);
        ppdPesoOcultoPrim[i] = NULL;
      }
    }
    free(ppdPesoOcultoPrim);
    ppdPesoOcultoPrim = NULL;
  }

  if (ppdPesoOcultoSeg != NULL) {
    for (i = 0; i < iNumeroOcultosSeg; i++) {
      if (ppdPesoOcultoSeg[i] != NULL) {
        free(ppdPesoOcultoSeg[i]);
        ppdPesoOcultoSeg[i] = NULL;
      }
    }
    free(ppdPesoOcultoSeg);
    ppdPesoOcultoSeg= NULL;
  }

  // Desaloca a memoria da camada de saida
  if (ppdPesoSaida != NULL) {
    for (i = 0; i < iNumeroSaidas; i++) {
      if (ppdPesoSaida[i] != NULL) {
        free(ppdPesoSaida[i]);
        ppdPesoSaida[i] = NULL;
      }
    }
    free(ppdPesoSaida);
    ppdPesoSaida = NULL;
  }
}
