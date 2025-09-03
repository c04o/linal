#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

#include "matrix.h"
#include "operaciones.h"
#include "funciones.h"

uint8_t RETURN_VALUE = 0;

#define DEBUG

#ifdef DEBUG
#define DEBUG_PRINT(...) printf(__VA_ARGS__)
#else
#define DEBUG_PRINT(...) do {} while(0);
#endif

double *gauss_jordan(Matrix *mat)
{
    /* Si la matriz no cumple con la condicion, error */
    if(mat->columnas != mat->filas - 1)
    {
        printf("La matriz debe ser de n x n+1, y las dimensiones dadas fueron de %dx%d", mat->filas, mat->columnas);
        RETURN_VALUE = -1;
        return NULL;
    }

    /* Cantidad N */
    uint8_t n = mat->filas;
    for (uint8_t col = 0; col < n; col++)
    {
        #ifdef DEBUG
        printf("Columna #%d: \n", col);
        imprimir_matriz(mat);
        #endif

        /* Si la columna esta vacia, continuamos */
        if (columna_nula(mat, col))
            continue;

        /* Obtenemos el pivote */
        double pivote = mat->matriz[col][col];

        /* Si el pivote es 0, intercambiemos con alguno otro */
        if (pivote == 0)
            for (uint8_t fila = 0; fila < n; fila++)
                if(mat->matriz[fila][col] != 0) {
                    intercambiar_fila(mat, col, fila);
                    pivote = mat->matriz[col][col];
                    break;
                }
        
        /* Si el pivote sigue siendo 0, no se puede hacer nada mas */
        if (pivote == 0)
            continue;
        /* Ahora normalizamos el pivote */
        if (pivote != 1)
            escalar_fila(mat, col, 1.0 / pivote);

        /* Hacer ceros en la columna del pivote para las otras filas */
        for (uint8_t fila = 0; fila < n; fila++)
        {
            /* No editemos la fila actual */
            if (fila == col)
                continue;

            double factor = mat->matriz[fila][col];
            restar_escalar_fila(mat, 1, fila, factor, col);
        }

        #ifdef DEBUG
        printf("Despues del paso #%d... \n", col);
        imprimir_matriz(mat);
        #endif
    }

    #ifdef DEBUG
    printf("Matriz final:");
    imprimir_matriz(mat);
    #endif

    for(uint8_t fila = 0; fila < n; fila++)
    {
        /* Revisar que todos los coeficientes en 0 */
        bool fila_es_cero = true;
        for(uint8_t col = 1; col < n - 1; col++)
            if(mat->matriz[fila][col] != 0)
            {
                fila_es_cero = false;
                break;
            }
        
        /* Si la fila es 0, y el resultado no, hay una contradiccion */
        if(fila_es_cero && mat->matriz[fila][n] != 0)
        {
            RETURN_VALUE = 0;
            return NULL;
        }
    }

    /* Contar variables basicas */
    /* Si hay una fila nula, hay una variable libre y por ende infinitas soluciones */
    for (uint8_t fila = 0; fila < n; fila++)
        if(fila_nula(mat, fila))
        {
            RETURN_VALUE = 1;
            return NULL;
        }
    
    /* Si no, creamos el conjunto solucion */
    double *soluciones = calloc(sizeof(double), n);

    for(uint8_t i = 0; i < n; i++)
    {
        if(mat->matriz[i][i] == 1)
            soluciones[i] = mat->matriz[i][n];
        else {
            printf("Hubo un problema generando el conjunto solucion.");
            RETURN_VALUE = -1;
            free(soluciones);
            return NULL;
        }
    }

    return soluciones;
}

void resolve_gauss_jordan(Matrix *mat)
{

}