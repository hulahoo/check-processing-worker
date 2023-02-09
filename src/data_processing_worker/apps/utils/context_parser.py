def _parse_chunk(chunk: dict):
    result = {}
    result_keys = []

    for key in chunk:
        if isinstance(chunk[key], dict):
            result_keys.append(key)

            res = _parse_chunk(chunk[key])

            for k in res:
                result['.'.join(result_keys) + '.' + k] = res[k]
        else:
            result[key] = chunk[key]

    return result


def parse_context(prefix, context):
    data = {}

    for chunk in context:
        data = _parse_chunk(chunk)

        break

    return {prefix: data}
