#include <stdio.h>
#include <stdlib.h>

#include "parser.h"

msl_token_t *new_token(char *val){
	msl_token_t *ret = malloc(sizeof(msl_token_t));
	ret->val = strdup(val);
	return ret;
}

msl_tokens_t *new_tokens(){
	msl_tokens_t *tok = malloc(sizeof(msl_tokens_t));
	return tok;
}

msl_tokens_t *msl_parse(char string[]){
	char *schar = string;
	msl_tokens_t *ret = new_tokens();

	long toklength = 0;

	while(*schar){
		if(strcmp("!", schar) != 0){
			ret->tokens[toklength] = new_token(schar);
		}

		toklength++;
		*schar++;
	}
	return ret;
}
