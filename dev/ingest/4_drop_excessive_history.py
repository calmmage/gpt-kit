def process_history(self, messages, system_description, model):
    model_max_tokens = max_tokens_per_model[model]
    history_token_limit = model_max_tokens - self.MIN_TOKENS
    history_token_limit -= estimate_tokens(system_description)
    all_messages = messages
    messages = self.drop_excessive_history(messages, history_token_limit)
    if len(messages) == 0:
        return [], {
            "error":
                "Couldn't fit even a single message in history \n"
                "Calculated limit: " + str(history_token_limit) +
                " last message token count: " +
                str(estimate_tokens(all_messages[-1]['content']))
        }
    return messages, None
