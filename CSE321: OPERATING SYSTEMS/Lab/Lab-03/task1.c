
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/wait.h>

#define SHM_SIZE sizeof(struct shared)

struct shared {
    char sel[100];
    int b;
};

int main() {
    key_t key = 1234; 
    int shmid;
    struct shared *shm_ptr;
    int pipe_fd[2]; 

    if (pipe(pipe_fd) == -1) {
        perror("Pipe creation failed");
        exit(1);
    }

    if ((shmid = shmget(key, SHM_SIZE, IPC_CREAT | 0666)) < 0) {
        perror("shmget failed");
        exit(1);
    }

    if ((shm_ptr = shmat(shmid, NULL, 0)) == (struct shared *) -1) {
        perror("shmat failed");
        exit(1);
    }
    
    shm_ptr->b = 1000;

    printf("Provide Your Input from Given Options:\n");
    printf("1. Type a to Add Money\n");
    printf("2. Type w to Withdraw Money\n");
    printf("3. Type c to Check Balance\n");
    printf("Enter your selection: ");
    scanf("%s", shm_ptr->sel);
    printf("Your selection: %s\n\n", shm_ptr->sel);
    
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        exit(1);
    }
    
    if (pid == 0) { 
        close(pipe_fd[0]); 
        
        char choice[100];
        strcpy(choice, shm_ptr->sel);
        int amount;

        if (strcmp(choice, "a") == 0) {
            printf("Enter amount to be added:\n");
            scanf("%d", &amount);
            if (amount > 0) {
                shm_ptr->b += amount;
                printf("Balance added successfully\n");
                printf("Updated balance after addition:\n");
                printf("%d\n", shm_ptr->b);
            } else {
                printf("Adding failed, Invalid amount\n");
            }
        } else if (strcmp(choice, "w") == 0) {
            printf("Enter amount to be withdrawn:\n");
            scanf("%d", &amount);
            if (amount > 0 && amount <= shm_ptr->b) {
                shm_ptr->b -= amount;
                printf("Balance withdrawn successfully\n");
                printf("Updated balance after withdrawal:\n");
                printf("%d\n", shm_ptr->b);
            } else {
                printf("Withdrawal failed, Invalid amount\n");
            }
        } else if (strcmp(choice, "c") == 0) {
            printf("Your current balance is:\n");
            printf("%d\n", shm_ptr->b);
        } else {
            printf("Invalid selection\n");
        }

        char *message = "Thank you for using";
        write(pipe_fd[1], message, strlen(message) + 1);
        close(pipe_fd[1]); 
        exit(0); 
    } 
    
    else {
        close(pipe_fd[1]); 
        wait(NULL); 

        char read_msg[100];
        read(pipe_fd[0], read_msg, sizeof(read_msg));
        close(pipe_fd[0]); 
        printf("%s\n", read_msg);

        shmdt(shm_ptr);
        shmctl(shmid, IPC_RMID, NULL);
    }
    
    return 0;
}