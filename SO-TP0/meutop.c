
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <string.h>
#include <sys/types.h>
#include <pwd.h>
// #include <pthread.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>


void print_top()
{
    char filename[300];
    char pname[300];
    char pstate[300];
    struct passwd *pw;
    struct stat info;
    DIR *d;
    FILE *fp;
    struct dirent *dir;
    d = opendir("/proc/");
    if (d)
    {
        printf("                                                        \n");
        printf("%6s | %10s | %20s | %2s\n", "PID", "USER", "PROC NAME", "STATE");
        printf("-------|------------|----------------------|--------\n");
        int i = 0;
        while ((dir = readdir(d)) != NULL && i < 20)
        {
            // printf("%s\n", dir->d_name);
            sprintf(filename, "/proc/%s/stat", dir->d_name);
            // printf("%s -- ", filename);
            stat(filename, &info); // Error check omitted
            pw = getpwuid(info.st_uid);
            if (pw != 0)
            {
                char *puser = pw->pw_name;
                int pid;

                fp = fopen(filename, "r");
                if (fp != NULL)
                {
                    fscanf(fp, "%d %s %s", &pid, pname, pstate);
                    fclose(fp);
                    sscanf(pname, "(%999[^)])", pname); // Remove "(" ")"
                    if(strcmp(pname, "'") != 0){  // remove first 2 process
                        printf("%6i | %10s | %20s | %2s\n", pid, puser, pname, pstate);
                        i += 1; // Only top 20
                    }
                }
            }
        }
        printf("> ");
        closedir(d);
    }
}

void *threadproc(void *arg)
{
    while(1)
    {
        sleep(1);
        print_top();
    }
    return 0;
}

int main(int argc, char const *argv[])
{
    // pthread_t tid;
    // pthread_create(&tid, NULL, &threadproc, NULL);
    printf("\033[2J");
    int p = fork();
    if(p == 0 ){
        while(1){
            sleep(1);
            // printf("\033[24A"); // Move up X lines;
            printf("\033[0;0H");
            print_top();
            printf("\n");
            printf("\033[23;10H");
            // printf("\033[8B"); // Move up X lines;
            // printf("\033[10D"); // Move up X lines;
        }
    }

    while(1){
        int pid = -1;
        int sig = -1;
        scanf("%i %i", &pid, &sig);
        printf("Send %i to %i\n", sig, pid);
        kill(pid, sig);
    }

    return (0);
}
