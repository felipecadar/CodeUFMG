#include "types.h"
#include "stat.h"
#include "user.h"

void do_op(){
    int pid = getpid();
    int i,j;
    switch (pid % 3)
    {
    case 0:
        // CPU-bound
        // printf(1,"Start CPU Boud %d\n", pid);
        for(i=0; i < 100; i++){
            j = 100000;
            while (j > 0)
            {
                j--;
            }
        }
        break;
    case 1:
        // S-CPU
        // printf(1,"Start S-CPU %d\n", pid);
        for(i=0; i < 100; i++){
            j = 100000;
            while (j > 0)
            {
                j--;
                if(j %100 == 0){
                    yield();
                }
            }
            
        }
    case 2:
        // IO-Bound
        // printf(1,"Start IO-Bound %d\n", pid);
        for(i=0; i < 100; i++){
            sleep(1);
        }

    default:
        break;
    }
}

int main(int argc, char *argv[]){
    if (argc < 2){
        // printf(1, "Missing positional param N\n");
        exit();
    }
    
    int n = atoi(argv[1]);
    printf(1, "[SANITY] - Running %d procs\n", n*5);
//////////////////////////////////////////////////////

    int retime;
    int rutime;
    int stime;

    int old_retime = 0;
    int old_rutime = 0;
    int old_stime = 0;

    int mean_retime[3];
    int mean_rutime[3];
    int mean_stime[3];

    int counter[3];
    
    memset(mean_retime, 0,3);
    memset(mean_rutime, 0,3);
    memset(mean_stime, 0,3);
    memset(counter, 0,3);

    int i = 0;
    for(i=0; i < n*5; i++){
        int f = fork();

        if(f == 0){
            do_op();
            exit();
        }else if (f > 0){
            wait2(&retime, &rutime, &stime);
            
            mean_retime[f % 3] += retime - old_retime ;
            mean_rutime[f % 3] += rutime - old_rutime ;
            mean_stime[f % 3] += stime - old_stime ;
            counter[f % 3] += 1;

            switch (f % 3)
            {
            case 0:
                printf(1, "PID: %d CPU-Bound - RET %d RUT %d ST %d\n", f, retime - old_retime, rutime - old_rutime, stime - old_stime);
                break;

            case 1:
                printf(1, "PID: %d S-CPU     - RET %d RUT %d ST %d\n", f, retime - old_retime, rutime - old_rutime, stime - old_stime);
                break;

            case 2:
                printf(1, "PID: %d IO-Bound  - RET %d RUT %d ST %d\n", f, retime - old_retime, rutime - old_rutime, stime - old_stime);
                break; 
            
            default:
                break;
            }

            old_retime = retime ;
            old_rutime = rutime ;
            old_stime = stime ;
        

        }else{
            printf(1, "Fail to fork\n");
        }


    }

    
    printf(1, "Results:\n");
    printf(1, "CPU-Boud: Sleep %d Ready %d Turnaround %d\n", mean_stime[0] / counter[0], mean_retime[0] / counter[0], (mean_stime[0] + mean_retime[0] + mean_rutime[0]) / counter[0] );
    printf(1, "S-CPU:    Sleep %d Ready %d Turnaround %d\n", mean_stime[1] / counter[1], mean_retime[1] / counter[1], (mean_stime[1] + mean_retime[1] + mean_rutime[1]) / counter[1] );
    printf(1, "IO-Bound: Sleep %d Ready %d Turnaround %d\n", mean_stime[2] / counter[2], mean_retime[2] / counter[2], (mean_stime[2] + mean_retime[2] + mean_rutime[2]) / counter[2] );

    exit();
}