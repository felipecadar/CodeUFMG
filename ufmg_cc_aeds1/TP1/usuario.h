#include "mensagem.h"

typedef struct
{
    int id;
    struct lstFollow *prox;
}lstFollow;

struct user
{
	int id;
    lstFollow *follow;
    char name[200];
    timeLine tl;
};
typedef struct user user;


void iniciarAmizade(user someone[], int user1, int user2, int n_users);
void cancelarAmizade(user someone[], int user1, int user2, int n_users);
void verAmigos();
int n_partes(char *line);
user scanFile(FILE *info);
void iniciaFollow(lstFollow *follow);
void insereFollow(lstFollow *follow, int id);
lstFollow *alocaFollow();
void postarMensagem(int message_id, int user_id, int time, char message[140], user someone[], int n_user);
int followSomeone(int id, lstFollow *follow);
user *curtirMensagem(user someone[], int mate,int message_id,int n_users);
timeLine* inverte_lista(timeLine **tl);
void imprime_rev_lista(timeLine tl, FILE *saida);
void exibirTimeline(user someone[], int mate,int n_users, FILE *saida);
