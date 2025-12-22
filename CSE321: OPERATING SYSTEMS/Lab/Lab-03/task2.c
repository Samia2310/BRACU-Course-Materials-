#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/wait.h>

#define MAX_TEXT 6

struct msg {
    long int type;
    char txt[MAX_TEXT];
};

int main() {
    key_t key = 1234;
    int msgid;
    struct msg message;
    char buffer[MAX_TEXT];

    msgid = msgget(key, 0666 | IPC_CREAT);
    if (msgid == -1) {
        perror("msgget");
        exit(1);
    }

    printf("Please enter the workspace name:\n");
    scanf("%s", buffer);

    if (strcmp(buffer, "cse321") != 0) {
        printf("Invalid workspace name\n");
        msgctl(msgid, IPC_RMID, NULL);
        return 0;
    }

    message.type = 1;
    strcpy(message.txt, buffer);
    if (msgsnd(msgid, &message, sizeof(message.txt), 0) == -1) {
        perror("msgsnd");
        exit(1);
    }
    printf("Workspace name sent to otp generator from log in: %s\n\n", message.txt);

    pid_t pid1 = fork();

    if (pid1 < 0) {
        perror("fork");
        exit(1);
    }

    if (pid1 == 0) {
        if (msgrcv(msgid, &message, sizeof(message.txt), 1, 0) == -1) {
            perror("msgrcv");
            exit(1);
        }
        printf("OTP generator received workspace name from log in: %s\n\n", message.txt);

        message.type = 2;
        sprintf(message.txt, "%d", getpid());
        if (msgsnd(msgid, &message, sizeof(message.txt), 0) == -1) {
            perror("msgsnd");
            exit(1);
        }
        printf("OTP sent to log in from OTP generator: %s\n", message.txt);

        pid_t pid2 = fork();

        if (pid2 < 0) {
            perror("fork");
            exit(1);
        }

        if (pid2 == 0) {
            message.type = 3;
            if (msgsnd(msgid, &message, sizeof(message.txt), 0) == -1) {
                perror("msgsnd");
                exit(1);
            }
            printf("OTP sent to mail from OTP generator: %s\n", message.txt);

            if (msgrcv(msgid, &message, sizeof(message.txt), 3, 0) == -1) {
                perror("msgrcv");
                exit(1);
            }
            printf("Mail received OTP from OTP generator: %s\n", message.txt);

            message.type = 4;
            if (msgsnd(msgid, &message, sizeof(message.txt), 0) == -1) {
                perror("msgsnd");
                exit(1);
            }
            printf("OTP sent to log in from mail: %s\n", message.txt);

            exit(0);
        } else {
            wait(NULL);
            exit(0);
        }
    } else {
        wait(NULL);

        char otp_from_otp_gen[MAX_TEXT];
        if (msgrcv(msgid, &message, sizeof(message.txt), 2, 0) == -1) {
            perror("msgrcv");
            exit(1);
        }
        strcpy(otp_from_otp_gen, message.txt);
        printf("Log in received OTP from OTP generator: %s\n", otp_from_otp_gen);

        char otp_from_mail[MAX_TEXT];
        if (msgrcv(msgid, &message, sizeof(message.txt), 4, 0) == -1) {
            perror("msgrcv");
            exit(1);
        }
        strcpy(otp_from_mail, message.txt);
        printf("Log in received OTP from mail: %s\n", otp_from_mail);

        if (strcmp(otp_from_otp_gen, otp_from_mail) == 0) {
            printf("OTP Verified\n");
        } else {
            printf("OTP Incorrect\n");
        }

        msgctl(msgid, IPC_RMID, NULL);
    }
    return 0;
}