#ifndef OPERATIONS_H
#define OPERATIONS_H

#include <stdint.h>
#include <stdbool.h>

#include "matrix.h"

void escalar_fila(Matrix *mat, uint8_t fila, double escalar);

void sumar_fila(Matrix *mat, uint8_t fila_a, uint8_t fila_b);

void sumar_escalar_fila(Matrix *mat, double escalar_a, uint8_t fila_a, double escalar_b, uint8_t fila_b);

void restar_fila(Matrix *mat, uint8_t fila_a, uint8_t fila_b);

void restar_escalar_fila(Matrix *mat, double escalar_a, uint8_t fila_a, double escalar_b, uint8_t fila_b);

void intercambiar_fila(Matrix *mat, uint8_t fila_a, uint8_t fila_b);

bool fila_nula(Matrix *mat, uint8_t fila);

bool columna_nula(Matrix *mat, uint8_t columna);

#endif /* OPERATIONS_H */