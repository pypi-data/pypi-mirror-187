/*
 * Implementation of a Multi-Layered Perceptron Neural Network
 */
#include "../../include/ml/mlp_network.hpp"
#include <stdio.h>
#include <time.h>
#include <math.h>
#include <string.h>


/*
 * Initialize randomly generated values for network's method
 */
void mtpk::mlp::PrimaryMLP::rand_init() {
    srand((uint64_t) time(NULL));
}

/* verify the random is an integer */
int64_t mtpk::mlp::PrimaryMLP::rand_int(int64_t hi, int64_t low) {
    return rand() % (hi - low + 1) + low;
}

/* verify generated random is a real number */
long double mtpk::mlp::PrimaryMLP::rand_real(long double low, 
                                            long double hi) {
    return ((long double) rand() / RAND_MAX) * (hi - low) + low;
}

/* MLP CONSTRUCTOR */
mtpk::mlp::PrimaryMLP::PrimaryMLP(int64_t nl, int64_t npl[]) : 
    num_layers(0), 
    layer_ptr(0),
    dEta(0.25),
    dAlpha(0.9),
    dGain(1.0),
    dMSE(0.0),
    dMAE(0.0),
    dAvgTestError(0.0)
    { 
        int64_t i, j;
}






