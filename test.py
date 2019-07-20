file1 = "small.ans"
file2 = "my_small2.ans"


# file1 = "large.ans"
# file2 = "my_large.ans"

def test_corr(mine, correct):
    is_right = True
    with open(mine, "r") as f:
        mine_lines = f.readlines()
    with open(correct, "r") as f:
        correct_lines = f.readlines()

    if len(mine_lines) != len(correct_lines):
        print("Wrong")
        exit(1)

    for i in range(min(len(mine_lines), len(correct_lines))):
        if mine_lines[i] != correct_lines[i]:
            print("incorrect at i = {}, should be {}, but got {}".format(i, correct_lines[i].strip(), mine_lines[i].strip()))
            # print(lines1[i].strip())
            # print(lines2[i].strip())
            is_right = False
        # exit(1)
    if is_right:
        print("Right!")
