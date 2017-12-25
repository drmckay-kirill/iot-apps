
#include <stdio.h>
#include <string.h>
#include "bignum.h"

int main() {
    printf("Hello, world! 322 111");

    bignum_digit_t alpha[BIGNUM_MAX_DIGITS];
    bignum_digit_t beta[BIGNUM_MAX_DIGITS];

    bignum_fromhex(alpha, "2A", BIGNUM_DIGITS(sizeof(alpha)));
    bignum_fromhex(beta, "3", BIGNUM_DIGITS(sizeof(beta)));    

    return 0;
}
