# tfrq - an easy way to parallelize processing a function

This library provides an easy way to parallelize the execution of a function in python using the concurrent.futures
library. It allows you to run multiple instances of a function simultaneously, making your code run faster and more
efficiently. It also provides a simple API for managing the process, allowing you to cancel or wait for the completion
of a task. With this library, you can easily take advantage of the power of parallel processing in python.

Here's an example of how you can use the library to parallelize the execution of the `print` function:

# Example 1:

```
from tfrq import tfrq
params = ["Hello", "World", "!"]
func = print
tfrq(func=func, params=params, num_cores=3)
```

# Example 2:

```
def calculate_sum_of_pairs(list_of_pairs):
    results = []
    for pair in list_of_pairs:
        results.append(sum(pair))

    return results


def huge_list_of_data_to_process(data_list):
    params = []

    for data_row in data_list:
        params.append((data_row[0], data_row[1]))

    list_of_results_for_all_pairs = tfrq(calculate_sum_of_pairs, params)

    list_of_results_for_all_pairs = sum(list_of_results_for_all_pairs, [])
    return list_of_results_for_all_pairs
    
input_list = [[1, 2], [3, 4], [5, 5], [6, 7]]
list_of_results_for_all_pairs = huge_list_of_data_to_process(input_list)
print(list_of_results_for_all_pairs)
```

This code will call the `print` function in parallel with the given parameters and use 3 cores, so it will print the
given parameters in parallel.

Tfrq is an arabic word meaning "To Split", which is the purpose of this simple method, to split the work of a single
function into multiple processes as easy as possible.