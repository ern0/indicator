# include <stdio.h>
# include <fcntl.h>
# include <unistd.h>
# include <errno.h>
# include <string.h>

int main() {

	const char* portname = "/dev/ttyACM0";
	int fd = open (portname, O_RDWR | O_NOCTTY | O_SYNC);
	if (fd < 0) {
		printf("error\n");
		perror("yep");
		return 1;
	}
	char x[] = "+8:400000000000047407408409;";
	int len = strlen(x);
	for (int n = 0; n < len; n++) {
		write(fd,&x[n],1);
		usleep(5 * 1000);
	}
	close(fd);

	return 0;
}
