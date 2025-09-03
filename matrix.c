#include <stdio.h>
#include <stdlib.h>

#include "matrix.h"

void inicializar_matriz(Matrix *mat, uint8_t filas, uint8_t columnas)
{
    /* Asignamos las filas y columnas */
    mat->filas = filas;
    mat->columnas = columnas;

    /* Alocamos los punteros */
    mat->matriz = malloc( sizeof(double*) * filas );

    /* Si es nulo, retornamos */
    if(mat->matriz == NULL)
        return;

    /* Hacemos un for para alocar las columnas */
    for (int i = 0; i < columnas; i++)
    {
        /* Alocamos la memoria en 0s para los doubles */
        mat->matriz[i] = calloc( sizeof(double), columnas);
        /* Si hay algun problema alocando memoria desalocamos todo */
        if (mat->matriz[i] != NULL)
        {
            for (int j = i - 1; j >= 0; j--)
                free(mat->matriz[j]);
            free(mat->matriz);
            mat->matriz = NULL;
            return;
        }
    }
}

void imprimir_matriz(Matrix *mat)
{
    /* Ciclamos por la matriz y la imprimimos */
    for(int i = 0; i < mat->filas; i++)
    {
        for(int j = 0; j < mat->columnas; j++)
            printf("[%.2f]\t", mat->matriz[i][j]);
        printf("\n");
    }
}