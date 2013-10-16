/*
 * example.c: очень простой пример для порта ввода/вывода
 *
 * Этот код не делает ничего полезного, только запись в порт, пауза,
 * и чтение из порта. Откомпилируйте `gcc -O2 -o example example.c',
 * и запустите под root `./example'.
 */

#include <stdio.h>
#include <unistd.h>
#include <sys/io.h>

#define BASEPORT 0x378 /* lp1 */
#define ADDPORT 0x37a /* lp1 */





int main()
{
  /* Получить доступ к порту */
  if (ioperm(BASEPORT, 3, 1)) {
	  perror("ioperm"); exit(1);
  }

  /* Вывод в порт (0) */
  outb(0, BASEPORT);

  /* Задержка (100 мс) */
  /*usleep(1000000);*/
  int c = 1;
  int DELAY = 100000;

  while (1)
  {
	c++;
	if( c > 1000) {
		break;
	}

	printf("статус: %d\n", c);
	outb(0x20, BASEPORT);
	outb(0x04, ADDPORT);
	usleep(100);
	outb(0x00, ADDPORT);
	usleep(DELAY);

	/*outb(0x30, BASEPORT);*/
	/*outb(0x04, ADDPORT);*/
	/*usleep(100);*/
	/*outb(0x00, ADDPORT);*/
	/*usleep(10000);*/

	outb(0x10, BASEPORT);
	outb(0x04, ADDPORT);
	usleep(100);
	outb(0x00, ADDPORT);
	usleep(DELAY);

	/*outb(0x60, BASEPORT);*/
	/*outb(0x04, ADDPORT);*/
	/*usleep(100);*/
	/*outb(0x00, ADDPORT);*/
	/*usleep(10000);*/

	outb(0x40, BASEPORT);
	outb(0x04, ADDPORT);
	usleep(100);
	outb(0x00, ADDPORT);
	usleep(DELAY);

	/*outb(0xc0, BASEPORT);*/
	/*outb(0x04, ADDPORT);*/
	/*usleep(100);*/
	/*outb(0x00, ADDPORT);*/
	/*usleep(10000);*/

	outb(0x80, BASEPORT);
	outb(0x04, ADDPORT);
	usleep(100);
	outb(0x00, ADDPORT);
	usleep(DELAY);

	/*outb(0x90, BASEPORT);*/
	/*outb(0x04, ADDPORT);*/
	/*usleep(100);*/
	/*outb(0x00, ADDPORT);*/
	/*usleep(10000);*/
  }
	outb(0x00, BASEPORT);
	outb(0x04, ADDPORT);
	usleep(100);
	outb(0x00, ADDPORT);

  /* Чтение из порта (BASEPORT+1) и вывод результатов на экран */
  printf("статус: %d\n", inb(BASEPORT + 1));

  /* Мы больше не нуждаемся больше в порту */
  if (ioperm(BASEPORT, 3, 0)) {
	  perror("ioperm"); exit(1);
  }

  exit(0);
}

/* конец example.c */
