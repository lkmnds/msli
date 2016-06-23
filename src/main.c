#include <stdio.h>
#include <stdlib.h>

#ifdef __UNIX__
	#include <readline/readline.h>
	#include <readline/history.h>
#elif __OSX__
	#include <editline/readline.h>
	#include <editline/history.h>
#elif _WIN32
	#include <string.h>

	static char buffer[2048];

	char *readline(char *prompt){
		fputs(prompt, stdout);
		fgets(buffer, 2048, stdin);
		char *cpy = malloc(strlen(buffer)+1);
		strcpy(cpy, buffer);
		cpy[strlen(cpy)-1] = '\0';
		return cpy;
	}

	void add_history(char *used){}
#endif

#include "parser.h"
#include "ast.h"

#define MSL_VERSION "0.0.0.1"
#define MSL_BUILD "1"

int main(int argc, char** argv) {
	printf("MSL v%s\n", MSL_VERSION);
	printf("Press Ctrl+c to Exit\n");

	while (1) {
		// prompt and read
		char *input = readline("msl> ");
		add_history(input);

		printf("%s\n", input);

		msl_tokens_t *tokens_table = msl_parse(input);
		msl_ast_t *ast = msl_new_ast(tokens_table);

		printf("freeing ast\n", input);
		free(ast);

		printf("freeing toktable\n", input);
		free(tokens_table);
		free(input);
	}

	return 0;
}
