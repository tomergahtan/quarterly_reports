
from app.initializing_the_system import info_generate,stock_list

import time

start = time.time()
def split_list(lst, n):
    """Split a list into `n` roughly equal parts."""
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


#13.17

print(len(stock_list))
list_parts = split_list(stock_list, 6)
info_generate(stock_list)
# threads = []
# for part in list_parts:
#     thread = Thread(target=info_generate, args=(part,))
#     thread.start()
#     threads.append(thread)
# for thread in threads:
#     thread.join()
#
print(time.time()-start)