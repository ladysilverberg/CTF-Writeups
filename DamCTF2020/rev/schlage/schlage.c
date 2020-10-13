#include <stdlib.h>
#include "schlage.h"

void seedRandom(unsigned int seed) {
    srand(seed);
}

int getRandom() {
    return rand();
}