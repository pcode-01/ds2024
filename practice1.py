# find_max.py

# 재귀 버전 함수
def find_max_recursive(data):
    # 기저 사례: 리스트에 하나의 요소만 남았을 때
    if len(data) == 1:
        return data[0]
    
    # 리스트를 두 부분으로 나누고 각 부분의 최대값을 재귀적으로 찾음
    mid = len(data) // 2
    left_max = find_max_recursive(data[:mid])
    right_max = find_max_recursive(data[mid:])
    
    # 두 부분의 최대값 중 큰 값을 반환
    return max(left_max, right_max)

# 반복 버전 함수
def find_max_iterative(data):
    # 데이터가 비어있을 경우
    if not data:
        return None
    
    # 최대값을 임시로 설정
    max_value = data[0]
    
    # 데이터를 반복하면서 최대값을 업데이트
    for num in data:
        if num > max_value:
            max_value = num
    
    return max_value

if __name__ == "__main__":
    # 사용자로부터 10개의 데이터 입력받기
    data = []
    for i in range(10):
        num = float(input(f"Enter number {i+1}: "))
        data.append(num)
    
    # 재귀 버전으로 최대값 찾기
    max_recursive = find_max_recursive(data)
    print("Maximum value (recursive):", max_recursive)
    
    # 반복 버전으로 최대값 찾기
    max_iterative = find_max_iterative(data)
    print("Maximum value (iterative):", max_iterative)
