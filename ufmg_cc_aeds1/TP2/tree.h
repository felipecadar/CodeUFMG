#define SBB_VERTICAL 0
#define SBB_HORIZONTAL 1

struct jogos{
    char data[100];
    char team1[500];
    char team2[500];
    int team1_g;
    int team2_g;

    long long int chave;
    long long int colision_key;


};

typedef struct jogos jogo;

struct sbb {
    jogo reg;
    struct sbb *esq;
    struct sbb *dir;
    int esqtipo;
    int dirtipo;
};

struct sbb buscarArvore(struct sbb *A, int chave, FILE *out);

struct sbb ee(struct sbb *ptr);

struct sbb dd(struct sbb *ptr);

struct sbb ed(struct sbb *ptr);

struct sbb de(struct sbb *ptr);

void iinsere_aqui (jogo reg, struct sbb **ptr, int *incli, int *fim);

void inicializa(struct sbb **raiz);

void iinsere(jogo reg, struct sbb **ptr,int *incli, int *fim);

void insere(jogo reg, struct sbb **raiz);
