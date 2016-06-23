#ifndef __PARSER_H__
#define __PARSER_H__

#define MAX_TOKENS 512

typedef struct {
	char val;
} msl_token_t;

typedef struct {
	int a;
	msl_token_t **tokens;
} msl_tokens_t;

msl_tokens_t *new_tokens();

msl_tokens_t *msl_parse(char string[]);

#endif
