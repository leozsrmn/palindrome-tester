import sys
import subprocess
import json
import colorama


def exec_test(name, args, ans, testid):
    tests_data = subprocess.run(["./palindrome_tmp"] + args.split(' '), capture_output=True, encoding='ascii')
    print(f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLUE_EX}---" + name + f"---{colorama.Style.RESET_ALL}")
    print("args: " + args)
    if tests_data.stdout == ans:
        print(f"{colorama.Fore.GREEN}Passed.{colorama.Style.RESET_ALL}")
    else:
        print(f"{colorama.Fore.RED}Failed.{colorama.Style.RESET_ALL}")
        print(f"\n{colorama.Fore.YELLOW}Get:")
        print(tests_data.stdout)
        print(f"{colorama.Fore.CYAN}Expected:{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.GREEN}" +ans)
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