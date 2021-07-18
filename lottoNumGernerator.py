from colored import fg, bg, attr
import random
import math
import time

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

# 0번 인덱스는 사용하지 않습니다.
# data.ltn 파일에 나온 바가 없어도 나올 수 있는 기회를 균등히 마련하기 위해
# 기본적으로 1% 씩 확률이 부여됩니다
control = [1 if not i == 0 else 0 for i in range(41)]  

def pend():
    while True:
        time.sleep(0.1)

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

try:
    with open("data.ltn", 'r', encoding='utf-8') as f:
        data = f.read()
        print(success, "data.ltn 파일을 정상적으로 잘 읽어들였습니다.")
        nums = unpack(data)

except FileNotFoundError:
    # 파일이 없는 경우의 예외 처리입니다
    print(error, "data.ltn 파일이 없습니다. 프로그램을 시작할 수 없습니다.")
    pend()

except AssertionError:
    # 파일 무결성 검사 중 통과하지 못한 경우입니다
    print(error, "data.ltn 파일이 손상되었습니다. nums의 배열은 길이가 반드시 7이여야 합니다.")
    pend()



else:
    print(success, "data.ltn 파일의 처리가 완료되었습니다.")

# 숫자의 빈도 수를 control의 숫자 번째 인덱스에 저장합니다.
# O(n^2)
for trial in nums:
    for n in trial:
        control[n] += 1

# 전체 빈도수의 합계입니다
total = sum(control)

# 빈도수가 저장되어 있는 control 을 백분위로 바꿉니다
for index, value in enumerate(control):
    # 1을 죽이지 않기 위해 올림합니다
    control[index] = math.ceil(value / total * 100)

lotto = []

for index, value in enumerate(control):
    for i in range(value):
        lotto.append(index)

print(logo)

while True:
    n = input(ask + " 뽑을 개수를 입력하세요> ")
    try:
        n = int(n)
    except:
        print(error, "정수를 입력하셔야 합니다.")
        continue
    else:
        print(info, f"{n}개의 로또 번호 추첨을 진행합니다.")
        break

for i in range(1, n+1):
    temp = []
    lotto_copied = lotto[:]
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


print(info, f"{n}개의 로또 번호 추첨이 완료되었습니다. 일등하세요!")
while True: time.sleep(0.1)
