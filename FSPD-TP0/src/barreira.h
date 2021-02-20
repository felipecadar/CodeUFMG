#include <pthread.h>
#include <unistd.h>

typedef pthread_mutex_t TBarreira;

void init_barreira(TBarreira* b, int n);
void barreira(TBarreira *b);