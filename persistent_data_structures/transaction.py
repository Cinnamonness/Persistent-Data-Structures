from time import sleep


def transaction(func: callable, *args, **kwargs) -> callable:
    transaction_complete = False
    return_value = None
    while transaction_complete is False:
        try:
            return_value = func(*args, **kwargs)
            transaction_complete = True
        except Exception:
            print('waiting...')
            sleep(0.6)
            continue
    return return_value
