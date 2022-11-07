import sys

# TODO: подумать над форматом сообщения
fmt = "{time} | {level} | {name}:{function}:{line} -> {message}"

# TODO: подумать над тем, как передавать эти данные в configure().
# можно использовать pydantic model
log_format = {
    "handlers": [
        {"sink": sys.stdout, "format": fmt},
    ]
}
