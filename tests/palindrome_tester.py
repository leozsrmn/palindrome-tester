import sys
import subprocess
import json
import colorama
import multiprocessing.pool
import functools


## SRC : https://stackoverflow.com/questions/492519/timeout-on-a-function-call
## timeout bf tests
def timeout(max_timeout):
    def timeout_decorator(item):
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator


@timeout(3)
def exec_test(name, args, ans, testid):
    utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)  # fd 1 is stdout
    if len(args) > 0:
        cmd = ["./palindrome_tmp"] + args.split(' ')
    else:
        cmd = ["./palindrome_tmp"]
    tests_data = subprocess.run(cmd, capture_output=True, encoding='ascii')
    print(f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}---" + name + f"---{colorama.Style.RESET_ALL}")
    print("args: \"" + args + "\" (args count: " + str(len(args.split(' '))) + ").")
    if tests_data.stdout == ans:
        print(f"{colorama.Fore.GREEN}Passed.{colorama.Style.RESET_ALL}")
    else:
        print(f"{colorama.Fore.RED}Failed.{colorama.Style.RESET_ALL}")
        print(f"\n{colorama.Fore.YELLOW}Get:")
        print(tests_data.stdout.encode('utf-8'))
        print(f"{colorama.Fore.CYAN}Expected:{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.GREEN}")
        print(str(ans).encode('utf-8'))
        print(f"{colorama.Style.RESET_ALL}")
    print("")


def run_tests(tests):
    for key, test in tests.items():
        exec_test(test['name'], test['arg'], test['ans'], key)


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("miss path")
        exit(84)
    file = open(sys.argv[1], "r")
    raw = json.load(file)
    run_tests(raw)