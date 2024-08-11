def determine_max_tokens(self, user, model, messages, system_description):
    max_tokens_preference = user.max_tokens_preference
    model_max_tokens = max_tokens_per_model[model]
    total_text = system_description + '\n'.join(
        [m['content'] for m in messages])
    current_token_count = estimate_tokens(total_text)
    remaining_tokens = model_max_tokens - current_token_count - self.TOKEN_COUNT_BUFFER

    if max_tokens_preference == 'maximum':
        max_tokens = remaining_tokens
    elif max_tokens_preference == 'moderate':
        f1 = self.MIN_TOKENS * 2 + (current_token_count // 2)
        max_tokens = min(f1, remaining_tokens)
    elif max_tokens_preference == 'minimum':
        max_tokens = min(self.MIN_TOKENS, remaining_tokens)
    else:
        raise ValueError(
            f'Unknown max_tokens_preference {max_tokens_preference}')

    if max_tokens < self.MIN_TOKENS:
        logger.warning(
            f'Available tokens {max_tokens} is less than reasonable minimum'
            f' {self.MIN_TOKENS}')

    return max_tokens
