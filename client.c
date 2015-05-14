#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <time.h>

void error(const char *msg)
{
  perror(msg);
  exit(0);
}

void reportShot(buffer, sockfd, n)
{
  char message[256];
  char buff[20];
  time_t now = time(NULL);
  strftime(buff, 20, "%Y-%m-%d %H:%M:%S", localtime(&now));
  snprintf(message, 255, "%s, %s", "shot", buff);
  n = write(sockfd,message,strlen(message));
  if (n < 0)
    error("ERROR writing to socket");
}

void reportHit(buffer, sockfd, n)
{
  int input;
  printf("Please enter the playerId that hit you: ");
  scanf("%d",&input);
  char message[256];
  char buff[20];
  time_t now = time(NULL);
  strftime(buff, 20, "%Y-%m-%d %H:%M:%S", localtime(&now));
  snprintf(message, 255, "%s, %s, %d", "hit", buff, input);
  n = write(sockfd,message,strlen(message));
  if (n < 0)
    error("ERROR writing to socket");
}

void reportError(buffer, sockfd, n)
{
  char message[256];
  char buff[20];
  time_t now = time(NULL);
  strftime(buff, 20, "%Y-%m-%d %H:%M:%S", localtime(&now));
  snprintf(message, 255, "%s, %s", "error", buff);
  n = write(sockfd,message,strlen(message));
  if (n < 0)
    error("ERROR writing to socket");
  printf("\nshot!\n");
}

int main(int argc, char *argv[])
{
  int sockfd, portno, n;
  struct sockaddr_in serv_addr;
  struct hostent *server;
  char buffer[256];
  if (argc < 3) {
    fprintf(stderr,"usage %s hostname port\n", argv[0]);
    exit(0);
  }
  portno = atoi(argv[2]);
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0)
    error("ERROR opening socket");
  server = gethostbyname(argv[1]);
  if (server == NULL) {
    fprintf(stderr,"ERROR, no such host\n");
    exit(0);
  }
  bzero((char *) &serv_addr, sizeof(serv_addr));
  serv_addr.sin_family = AF_INET;
  bcopy((char *)server->h_addr,
        (char *)&serv_addr.sin_addr.s_addr,
        server->h_length);
  serv_addr.sin_port = htons(portno);
  if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0)
    error("ERROR connecting");
  printf("Please enter the username: ");
  bzero(buffer,256);
  fgets(buffer,255,stdin);
  n = write(sockfd,buffer,strlen(buffer));
  if (n < 0)
    error("ERROR writing to socket");
  int choice;
  while(choice != 0)
    {

      printf("\n1. quit\n");
      printf("2. report shot\n");
      printf("3. report hit\n");
      printf("4. report error\n");
      printf("selection: ");

      scanf("%d",&choice);

      switch(choice)
        {
        case 1:
          return 0;
          break;
        case 2:
          reportShot(buffer, sockfd, n);
          break;
        case 3:
          reportHit(buffer, sockfd, n);
          break;
        case 4:
          reportError(buffer, sockfd, n);
          break;
        default:
          printf("\nBAD OPTION! Please choose again!");
        }


      /* bzero(buffer,256); */
      /* n = read(sockfd,buffer,255); */
      /* if (n < 0) */
      /*   error("ERROR reading from socket"); */
      /* printf("%s\n",buffer); */
      /* printf("\nPlease enter a command: "); */
      /* bzero(buffer,256); */
      /* fgets(buffer,255,stdin); */
      /* n = write(sockfd,buffer,strlen(buffer)); */
      /* if (n < 0) */
      /*   error("ERROR writing to socket"); */
    }
  close(sockfd);
  return 0;
}
