#include "uECC.h"

#include <stdio.h>
#include <string.h>

void vli_print(uint8_t *vli, unsigned int size) {
    for(unsigned i=0; i<size; ++i) {
        printf("%02X ", (unsigned)vli[i]);
    }
    printf("\n");
}

int main() {

    uint8_t public[64];
    uint8_t private[32];
    uint8_t compressed_point[33];
    uint8_t decompressed_point[64];

    int i;

    const struct uECC_Curve_t * curve = uECC_secp160r1();

    printf("Generate random points.\n");
    for(i = 0; i < 10; i++) {
        fflush(stdout);
        memset(public, 0, sizeof(public));

        if (!uECC_make_key(public, private, curve)) {
            printf("uECC_make_key() failed\n");
            continue;
        }
        vli_print(public, sizeof(public));

    }

    return 0;
}