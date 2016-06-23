#ifndef __PARSER_H__
#define __PARSER_H__

typedef struct {
	char val;
} msl_token;

typedef struct {
	int a;
	msl_token tokens[];
} msl_tokens_t;

msl_tokens_t *new_tokens();

msl_tokens_t *msl_parse(char string[]);

#endif
