#include <stdbool.h>

#include "matrix.c"

void escalar_fila(Matrix *mat, uint8_t fila, double escalar)
{
    /* Ciclamos por las columnas */
    for (uint8_t i = 0; i < mat->columnas; i++)
        mat->matriz[fila][i] *= escalar;
}

void sumar_fila(Matrix *mat, uint8_t fila_a, uint8_t fila_b)
{
    /* Ciclamos por las columnas */
    for (uint8_t i = 0; i < mat->columnas; i++)
        mat->matriz[fila_a][i] += mat->matriz[fila_b][i];
}

void sumar_escalar_fila(Matrix *mat, double escalar_a, uint8_t fila_a, double escalar_b, uint8_t fila_b)
{
    /* Ciclamos por las columnas */
    for (uint8_t i = 0; i < mat->columnas; i++)
        mat->matriz[fila_a][i] = (escalar_a * mat->matriz[fila_a][i]) + (escalar_b * mat->matriz[fila_b][i]);
}

void restar_fila(Matrix *mat, uint8_t fila_a, uint8_t fila_b)
{
    /* Ciclamos por las columnas */
    for (uint8_t i = 0; i < mat->columnas; i++)
        mat->matriz[fila_a][i] -= mat->matriz[fila_b][i];
}

void restar_escalar_fila(Matrix *mat, double escalar_a, uint8_t fila_a, double escalar_b, uint8_t fila_b)
{
    /* Ciclamos por las columnas */
    for (uint8_t i = 0; i < mat->columnas; i++)
        mat->matriz[fila_a][i] = (escalar_a * mat->matriz[fila_a][i]) - (escalar_b * mat->matriz[fila_b][i]);
}

void intercambiar_fila(Matrix *mat, uint8_t fila_a, uint8_t fila_b)
{
    /* Ciclamos por las columnas */
    for (uint8_t i = 0; i < mat->columnas; i++)
    {
        /* Intercambiamos cada una */
        double temp = mat->matriz[fila_a][i];
        mat->matriz[fila_a][i] = mat->matriz[fila_b][i];
        mat->matriz[fila_b][i] = temp;
    }
}

bool fila_nula(Matrix *mat, uint8_t fila)
{
    /* Ciclamos para ver si existe algun numero que no sea 0 */
    for (uint8_t i = 0; i < mat->columnas; i++)
        if(mat->matriz[fila][i] != 0)
            return false;
    return true;
}

bool columna_nula(Matrix *mat, uint8_t columna)
{
    /* Ciclamos para ver si existe algun numero que no sea 0 */
    for (uint8_t i = 0; i < mat->columnas; i++)
        if(mat->matriz[i][columna] != 0)
            return false;
    return true;
}