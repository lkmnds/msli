#include <stdlib.h>
#include "parser.h"
#include "ast.h"

msl_ast_t *msl_new_ast(msl_tokens_t *tokens){
	msl_ast_t *ret = malloc(sizeof(msl_ast_t));
	//ret->tokens = tokens;
	return ret;
}
