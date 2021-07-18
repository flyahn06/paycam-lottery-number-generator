from typing import Counter
from colored import fg, bg, attr
import traceback
import random
import math
import time
import sys

error = fg(1) + "[!]" + attr(0)
success = fg(46) + "[!]" + attr(0)
info = fg(6) + "[*]" + attr(0)
ask = fg(220) + "[?]" + attr(0)

one_to_nine = bg(220) + fg(0) + "{}" + attr(0) # 노랑
ten_to_nineteen = bg(19) + fg(7) + "{}" + attr(0) # 파랑
twenty_to_twentynine = bg(13) + fg(7) + "{}" + attr(0) # 보라
thirty_to_fourty = bg(10) + fg(0) + "{}" + attr(0) # 초록

logo = """
                                               < Initial Release >
 _______                                                              __                    __      __               
/       \                                                            /  |                  /  |    /  |              
$$$$$$$  | ______   __    __   _______   ______   _____  ____        $$ |        ______   _$$ |_  _$$ |_     ______  
$$ |__$$ |/      \ /  |  /  | /       | /      \ /     \/    \       $$ |       /      \ / $$   |/ $$   |   /      \ 
$$    $$/ $$$$$$  |$$ |  $$ |/$$$$$$$/  $$$$$$  |$$$$$$ $$$$  |      $$ |      /$$$$$$  |$$$$$$/ $$$$$$/   /$$$$$$  |
$$$$$$$/  /    $$ |$$ |  $$ |$$ |       /    $$ |$$ | $$ | $$ |      $$ |      $$ |  $$ |  $$ | __ $$ | __ $$ |  $$ |
$$ |     /$$$$$$$ |$$ \__$$ |$$ \_____ /$$$$$$$ |$$ | $$ | $$ |      $$ |_____ $$ \__$$ |  $$ |/  |$$ |/  |$$ \__$$ |
$$ |     $$    $$ |$$    $$ |$$       |$$    $$ |$$ | $$ | $$ |      $$       |$$    $$/   $$  $$/ $$  $$/ $$    $$/ 
$$/       $$$$$$$/  $$$$$$$ | $$$$$$$/  $$$$$$$/ $$/  $$/  $$/       $$$$$$$$/  $$$$$$/     $$$$/   $$$$/   $$$$$$/  
                   /  \__$$ |                                                                                        
                   $$    $$/                                                                                         
                    $$$$$$/                                                                                          
"""

help_msg = """
pick (analy | regul) <amount>\tamount개만큼 숫자를 추첨합니다.
\t\t\t\tanaly 는 분석에 기반하여, regul 은 쌩 랜덤으로 추첨합니다.
show [n]\t\t\t숫자 n에 대한 확률을 보여줍니다. n이 없으면 전체 숫자의 확률을 보여줍니다.
reload\t\t\t\tdata.ltn 파일을 다시 로드하여 분석합니다.
credit\t\t\t\t크레딧을 보여줍니다.
help\t\t\t\t명령어에 대한 도움말을 표시합니다.
exit\t\t\t\t프로그램을 종료합니다.
[참조] 모든 명령어는 앞 글자만을 이용해 사용할 수 있습니다.
예시) p a 3 은 pick analy 3 과 정확히 똑같은 작업을 수행합니다.
"""

credit_msg = """
개발 flyahn06 | 데이터베이스 제공 Odyssey
"""

def pend():
    while True:
        try:
            time.sleep(0.1)
        except:
            sys.exit()

# 데이터를 저장할 수 있는 형식으로 묶습니다
def pack(data: list) -> str:
    for index, value in enumerate(data):
        data[index] = " ".join(list(map(str, value))).strip() + "\n"
    
    data = "".join(data)
    
    return data

# 데이터를 가공하여 처리할 수 있는 리스트를 반환합니다
def unpack(data: str) -> list:
    data = data.strip()
    nums = data.split("\n")

    remove = []

    # 주석을 처리합니다
    for text in nums:
        if text.startswith("#") or text.startswith("//") or text == "\n" or text == "":
            remove.append(text)
    for text in remove:
        nums.remove(text)

    for index, value in enumerate(nums):
        nums[index] = list(map(int, value.split(" ")))

    # 데이터의 무결성을 확인합니다
    # 파일이 손상된 경우에는 trial의 하위 차원 리스트의 길이가 7을 만족하지 않습니다
    for trial in nums:
        assert len(trial) == 7
    
    return nums

def print_chance(data, index=None):
    if index:
        print("+------+--------+")
        print("| num  | chance |")
        print("+------+--------+")
        print(f"|  {index}  |   {data}   |")
        print("+-----+--------+")
        return


    print("+------+--------+")
    print("| num  | chance |")
    print("+------+--------+")
    for number, chance in enumerate(data):
        if number == 0:
            continue
        print(f"|  {number}  |   {chance}   |")
        print("+-----+--------+")

class LottoGen:
    def __init__(self):
        self.nums = []
        self.lotto = []
        self.control = [1 if not i == 0 else 0 for i in range(40)]
        self.prevdata = ""

    def load(self):
        try:
            with open("data.ltn", 'r', encoding='utf-8') as f:
                    data = f.read()
                    print(success, "data.ltn 파일을 정상적으로 잘 읽어들였습니다.")

                    if self.prevdata and data == self.prevdata:
                        print(info, "data.ltn 파일에 변화가 없습니다. 전에 처리해놨던 데이터를 사용합니다.")
                        return
                    
                    self.nums = unpack(data)

        except FileNotFoundError:
            # 파일이 없는 경우의 예외 처리입니다
            print(error, "data.ltn 파일이 없습니다. 프로그램을 시작할 수 없습니다.")
            pend()

        except AssertionError:
            # 파일 무결성 검사 중 통과하지 못한 경우입니다
            print(error, "data.ltn 파일이 손상되었습니다. nums의 배열은 길이가 반드시 7이여야 합니다.")
            pend()

        except:
            print(error, "알 수 없는 오류가 발생했습니다.")
            etype, value, tb = sys.exc_info()
            print(''.join(traceback.format_exception(etype, value, tb)))
            pend()

        else:
            print(success, "data.ltn 파일의 처리가 완료되었습니다.")
            self.prevdata = data

        # 숫자의 빈도 수를 control의 숫자 번째 인덱스에 저장합니다.
        # O(n^2)
        for trial in self.nums:
            for n in trial:
                self.control[n] += 1

        # 전체 빈도수의 합계입니다
        total = sum(self.control)

        # 빈도수가 저장되어 있는 control 을 백분위로 바꿉니다
        for index, value in enumerate(self.control):
            # 1을 죽이지 않기 위해 올림합니다
            self.control[index] = math.ceil(value / total * 100)
    
    def generate_lotto(self, mode):
        self.lotto = []

        if mode == "analy" or mode == "a":
            for index, value in enumerate(self.control):
                for i in range(value):
                    self.lotto.append(index)
            return True
        
        elif mode == "regul" or mode == "r":
            for i in range(1, 40):
                self.lotto.append(i)
            return True
        
        else:
            print(error, "mode의 값이 정확하지 않습니다. mode는 analy | regul 이 되어야 합니다.\n자세한 내용은 help또는 ?를 참조하십시오.")
            return False
    
    def get_control(self, n):
        if n == "all":
            return self.control
        else:
            return self.control[n]

    def pick(self, mode, amount):
        is_succeed = self.generate_lotto(mode)

        if not is_succeed:
            return

        for i in range(1, amount+1):
            temp = []
            lotto_copied = self.lotto[:]

            for j in range(6):
                random.shuffle(lotto_copied)

                number = lotto_copied.pop()

                for _ in range(lotto_copied.count(number)):
                    lotto_copied.remove(number)

                temp.append(number)
            temp.sort()
        
            for index, value in enumerate(temp):
                if 1 <= value <= 9:
                    temp[index] = one_to_nine.format(str(value) + " ")
                elif 10 <= value <= 19:
                    temp[index] = ten_to_nineteen.format(value)
                elif 20 <= value <= 29:
                    temp[index] = twenty_to_twentynine.format(value)
                elif 30 <= value <= 40:
                    temp[index] = thirty_to_fourty.format(value)
            print("[{}]\t{}".format(i, "\t".join(temp)))


print(logo)

gen = LottoGen()
first = True
while True:
    if first:
        gen.load()
        first = not first
    print("ltng> ", end="")
    try:
        command = input().strip().lower()
    except KeyboardInterrupt:
        sys.exit()
    except EOFError:
        sys.exit()

    if command.startswith("pick") or command.startswith("p"):
        param = command.split(" ")

        if not len(param) == 3:
            print("사용법: pick (analy | regul) <amount>\n자세한 내용은 help 또는 ? 를 참조하십시오.")
            continue

        try:
            param[2] = int(param[2])
        except:
            print(error, "amount의 값은 정수가 되어야 합니다.")
            continue

        gen.pick(param[1], param[2])

    elif command.startswith("show") or command.startswith("s"):
        param = command.split()

        if len(param) == 1:
            data = gen.get_control("all")
            print_chance(data)
        else:
            try:
                param[1] = int(param[1])
            except:
                print("사용법: show [n]\nn의 값은 정수가 되어야 합니다. 자세한 내용은 help 또는 ?를 참조하십시오.")
                continue

            if not 1 <= param[1] <= 39:
                print("n의 값은 1부터 39사이의 정수가 되어야 합니다.")
                continue

            data = gen.get_control(param[1])
            print_chance(data, param[1])
    elif command == "credit" or command == "c":
        print(credit_msg)
    elif command == "reload" or command == "r":
        gen.load()
    elif command == "help" or command == "h" or command == "?":
        print(help_msg)
    elif command == "exit" or command == "quit" or command == "e" or command == "q":
        sys.exit()