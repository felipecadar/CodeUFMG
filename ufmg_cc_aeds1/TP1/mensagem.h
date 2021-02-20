struct tweetInfo{
    char post[140];
    int time;
    int id;
    int favs;
    int owner;
};
typedef struct tweetInfo tweet;

struct timeLine{
    tweet post;
    struct timeLine *prox;
};
typedef struct timeLine timeLine;


void insereTweet(int owner,int id, int time, char post[140], timeLine *tl);
timeLine *alocaTl();
int tl_vazia(timeLine *tl);
