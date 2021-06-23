#!/bin/bash
echo -e "Requirement tests:\n"
cc -fPIC -shared -o requirement.so ../requirement.c
python3 requirement_tester.py rq_tests.json
rm requirement.so
echo -e "Palindrome tests:\n"
make -C ../ > /dev/null
cp ../palindrome ./palindrome_tmp > /dev/null
python3 palindrome_tester.py ./tests.json
rm palindrome_tmp > /dev/null
make fclean -C ../ > /dev/null