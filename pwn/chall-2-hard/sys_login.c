//gcc source.c -o vuln-32 -no-pie -fstack-protector -m32
//gcc source.c -o vuln-64 -no-pie -fstack-protector

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

void vuln() {
    char buffer[64];

    puts("Leak me");
    gets(buffer);

    printf(buffer);
    puts("");

    puts("Overflow me");
    gets(buffer);
}

int main() {
    vuln();
}

void win() {
    setuid(0);
    system("id");
    system("/bin/cat /flag");
}
