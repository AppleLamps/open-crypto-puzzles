/*
 * floater_gen.c -- fast enumerator for the RO1-plus-one-video-floater space.
 *
 * Mirrors scan_unit() in sweep_coins.py loop for loop, so the candidates come
 * out in the identical order: per post word set (unit), per video layout, per
 * fork slot, per floater word, per pool row. Each 12-word arrangement is
 * filtered by the BIP39 checksum and the survivors are written to stdout as
 * 12 little-endian int32 word indices, ready for the multi-target ETH kernel
 * in engines/bip39_passphrase_engine.cu.
 *
 * The plan (anchors, floater words, layouts, pool rows, post word sets) is
 * built by floater_gpu.py from the same Python code as sweep_coins.py and read
 * from the file named on the command line, so this file holds no word lists.
 *
 *   cc -O3 -o floater_gen floater_gen.c
 *   ./floater_gen PLAN UNIT          # valid rows of one unit, binary, stdout
 *   ./floater_gen PLAN UNIT --count  # "arrangements valid" for one unit, text
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ---- SHA-256 of one 16-byte message (a single padded block) ---- */
static const uint32_t K[64] = {
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
#define ROR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))

/* Top 4 bits of SHA-256(ent[0..3] as 16 big-endian bytes). */
static unsigned sha_nibble(const uint32_t ent[4]) {
    uint32_t w[64], a, b, c, d, e, f, g, h;
    w[0] = ent[0]; w[1] = ent[1]; w[2] = ent[2]; w[3] = ent[3];
    w[4] = 0x80000000u;
    for (int i = 5; i < 15; i++) w[i] = 0;
    w[15] = 128;
    for (int i = 16; i < 64; i++) {
        uint32_t s0 = ROR(w[i-15], 7) ^ ROR(w[i-15], 18) ^ (w[i-15] >> 3);
        uint32_t s1 = ROR(w[i-2], 17) ^ ROR(w[i-2], 19) ^ (w[i-2] >> 10);
        w[i] = w[i-16] + s0 + w[i-7] + s1;
    }
    a = 0x6a09e667; b = 0xbb67ae85; c = 0x3c6ef372; d = 0xa54ff53a;
    e = 0x510e527f; f = 0x9b05688c; g = 0x1f83d9ab; h = 0x5be0cd19;
    for (int i = 0; i < 64; i++) {
        uint32_t t1 = h + (ROR(e, 6) ^ ROR(e, 11) ^ ROR(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + w[i];
        uint32_t t2 = (ROR(a, 2) ^ ROR(a, 13) ^ ROR(a, 22)) + ((a & b) ^ (a & c) ^ (b & c));
        h = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2;
    }
    return (0x6a09e667u + a) >> 28;
}

/* 12 indices -> 132 bits; returns 1 when the last 4 bits are the checksum. */
static int checksum_ok(const int32_t idx[12]) {
    uint32_t ent[4] = {0, 0, 0, 0};
    int bit = 0;
    for (int w = 0; w < 12; w++) {
        for (int b = 10; b >= 0; b--, bit++) {
            if (bit >= 128) continue;
            if ((idx[w] >> b) & 1) ent[bit >> 5] |= 0x80000000u >> (bit & 31);
        }
    }
    return sha_nibble(ent) == (unsigned)(idx[11] & 0xF);
}

/* ---- plan ---- */
typedef struct {
    int floater_slot, npool, pool_slots[4], nvideo, video_slots[12], nrows;
    int32_t *rows;                     /* nrows * npool */
} Layout;

static int rd(FILE *f) {
    int v;
    if (fscanf(f, "%d", &v) != 1) { fprintf(stderr, "bad plan\n"); exit(2); }
    return v;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: floater_gen PLAN UNIT [--count]\n"); return 2; }
    int count_only = argc > 3 && !strcmp(argv[3], "--count");
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror(argv[1]); return 2; }
    int dutch = rd(f), fog = rd(f), parrot = rd(f), fork = rd(f);
    int nfl = rd(f);
    int32_t *fl = malloc(sizeof(int32_t) * nfl);
    for (int i = 0; i < nfl; i++) fl[i] = rd(f);
    int nlay = rd(f);
    Layout *L = calloc(nlay, sizeof(Layout));
    for (int i = 0; i < nlay; i++) {
        L[i].floater_slot = rd(f);
        L[i].npool = rd(f);
        for (int j = 0; j < L[i].npool; j++) L[i].pool_slots[j] = rd(f);
        L[i].nvideo = rd(f);
        for (int j = 0; j < L[i].nvideo; j++) L[i].video_slots[j] = rd(f);
        L[i].nrows = rd(f);
        L[i].rows = malloc(sizeof(int32_t) * L[i].nrows * L[i].npool);
        for (int j = 0; j < L[i].nrows * L[i].npool; j++) L[i].rows[j] = rd(f);
    }
    int nunits = rd(f);
    int unit = atoi(argv[2]);
    if (unit < 0 || unit >= nunits) { fprintf(stderr, "unit out of range\n"); return 2; }
    int32_t ord4[4];
    for (int u = 0; u <= unit; u++)
        for (int j = 0; j < 4; j++) ord4[j] = rd(f);
    fclose(f);

    enum { BUF = 4096 };
    static int32_t out[BUF * 12];
    int nout = 0;
    unsigned long long n = 0, d = 0;
    for (int li = 0; li < nlay; li++) {
        Layout *l = &L[li];
        int used[12] = {0};
        for (int j = 0; j < l->nvideo; j++) used[l->video_slots[j]] = 1;
        used[0] = used[4] = used[11] = 1;
        int post[12], np = 0;
        for (int p = 0; p < 12; p++) if (!used[p]) post[np++] = p;
        for (int fi = 0; fi < np; fi++) {
            int32_t row[12];
            memset(row, 0, sizeof row);
            row[0] = dutch; row[4] = fog; row[11] = parrot;
            row[post[fi]] = fork;
            for (int j = 0, k = 0; j < np; j++)
                if (j != fi) row[post[j]] = ord4[k++];
            for (int c = 0; c < nfl; c++) {
                row[l->floater_slot] = fl[c];
                const int32_t *r = l->rows;
                for (int v = 0; v < l->nrows; v++, r += l->npool) {
                    for (int j = 0; j < l->npool; j++) row[l->pool_slots[j]] = r[j];
                    n++;
                    if (!checksum_ok(row)) continue;
                    d++;
                    if (count_only) continue;
                    memcpy(out + nout * 12, row, sizeof row);
                    if (++nout == BUF) { fwrite(out, sizeof(int32_t) * 12, BUF, stdout); nout = 0; }
                }
            }
        }
    }
    if (count_only) { printf("%llu %llu\n", n, d); return 0; }
    if (nout) fwrite(out, sizeof(int32_t) * 12, nout, stdout);
    return 0;
}
