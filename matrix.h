#ifndef MATRIX_H
#define MATRIX_H

#include <stdint.h>

typedef struct {
    double **matriz;
    uint8_t filas;
    uint8_t columnas;
} Matrix;

void inicializar_matriz(Matrix *mat, uint8_t filas, uint8_t columnas);
void imprimir_matriz(Matrix *mat);

#endif /* MATRIX_H */