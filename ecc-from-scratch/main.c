#include <stdio.h>
#include <string.h>
#include "bignum.h"
#include "eccrypt.h"

int main() {

    char buff[256];

    printf("Hello, world!\n");

    bignum_digit_t alpha[BIGNUM_MAX_DIGITS];
    bignum_digit_t beta[BIGNUM_MAX_DIGITS];
    bignum_digit_t mod[BIGNUM_MAX_DIGITS];

    bignum_fromhex(alpha, "2A", BIGNUM_DIGITS(sizeof(alpha)));
    bignum_fromhex(beta, "3", BIGNUM_DIGITS(sizeof(beta)));    
    bignum_add(alpha, beta, BIGNUM_DIGITS(sizeof(alpha)));

    bignum_tohex(alpha, buff, sizeof(buff), BIGNUM_DIGITS(sizeof(alpha)));
    printf("%s\n", buff);

    bignum_fromhex(alpha, "2A", BIGNUM_DIGITS(sizeof(alpha)));
    bignum_mul(alpha, beta, BIGNUM_DIGITS(sizeof(alpha)));

    bignum_tohex(alpha, buff, sizeof(buff), BIGNUM_DIGITS(sizeof(alpha)));
    printf("%s\n", buff);

    bignum_fromhex(alpha, "2A", BIGNUM_DIGITS(sizeof(alpha)));
    bignum_fromhex(mod, "100", BIGNUM_DIGITS(sizeof(mod)));
    bignum_mdiv(alpha, beta, mod, BIGNUM_DIGITS(sizeof(alpha)));

    bignum_tohex(alpha, buff, sizeof(buff), BIGNUM_DIGITS(sizeof(alpha)));
    printf("%s\n", buff);

    // NIST P-256
    char a[]  = "FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC";
    char b[]  = "5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b";
    char p[]  = "FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF";
    char gx[] = "6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296";
    char gy[] = "4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5";    

    struct eccrypt_curve_t curve;
    struct eccrypt_point_t p1, p2, rslt;        

    bignum_fromhex(curve.a, a, ECCRYPT_BIGNUM_DIGITS);
    bignum_fromhex(curve.b, b, ECCRYPT_BIGNUM_DIGITS);
    bignum_fromhex(curve.m, p, ECCRYPT_BIGNUM_DIGITS);
    bignum_fromhex(curve.g.x, gx, ECCRYPT_BIGNUM_DIGITS);
    bignum_fromhex(curve.g.y, gy, ECCRYPT_BIGNUM_DIGITS);
    curve.g.is_inf = 0;

    bignum_fromhex(p1.x, "2", ECCRYPT_BIGNUM_DIGITS);
    bignum_fromhex(p1.y, "0", ECCRYPT_BIGNUM_DIGITS);

    bignum_fromhex(p2.x, "2", ECCRYPT_BIGNUM_DIGITS);
    bignum_fromhex(p2.y, "0", ECCRYPT_BIGNUM_DIGITS);    

    eccrypt_point_add(&rslt, &p1, &p2, &curve);    

    bignum_tohex(rslt.x, buff, sizeof(buff), ECCRYPT_BIGNUM_DIGITS);
    printf("%s\n", buff);
    bignum_tohex(rslt.y, buff, sizeof(buff), ECCRYPT_BIGNUM_DIGITS);
    printf("%s\n", buff);

    return 0;
}
