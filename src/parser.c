#include <stdio.h>
#include <stdlib.h>

typedef struct {
	char val;
} msl_token;

typedef struct {
	int a;
	msl_token tokens[];
} msl_tokens_t;

msl_tokens_t *new_tokens(){
	msl_tokens_t *tok = malloc(sizeof(msl_tokens_t));

	return tok;
}

msl_tokens_t *msl_parse(char string[]){
	char *string_ptr;
	msl_tokens_t *ret = new_tokens();

	for(string_ptr = string; *string_ptr != '\0'; string_ptr++){
		*string_ptr = 'A';
	}
	return ret;
}
