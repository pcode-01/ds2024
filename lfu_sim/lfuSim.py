# 캐시 아이템을 표현하는 클래스
class CacheItem:
    def __init__(self, lpn, tot_cnt, freq=1):
        self.lpn = lpn  # 로직 페이지 번호, 식별자 역할을 하는 속성
        self.tot_cnt = tot_cnt  # 해당 아이템이 처리된 전체 횟수
        self.freq = freq  # 아이템이 접근된 빈도수

    def __lt__(self, other):
        # 다른 아이템과 비교하여 우선 순위를 결정하는 메소드, 비교 기준은 빈도
        return self.freq < other.freq

    def __gt__(self, other):
        # 다른 아이템과 비교하여 우선 순위를 결정하는 메소드, 비교 기준은 빈도
        return self.freq > other.freq

    def __repr__(self):
        # 객체의 문자열 표현을 반환하는 메소드, 디버깅 용도
        return f"CacheItem(lpn={self.lpn}, freq={self.freq}, tot_cnt={self.tot_cnt})"


# LFU(Least Frequently Used) 캐싱 알고리즘을 구현한 최소 힙 클래스
class LFUCache:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots  # 캐시 슬롯의 최대 크기
        self.heap = []  # 힙 구조를 사용하여 아이템을 저장하는 리스트
        self.lpn_to_freq = {}  # 각 LPN의 빈도수를 저장하는 딕셔너리
        self.tot_cnt = 0  # 전체 요청 처리 횟수
        self.cache_hit = 0  # 캐시 히트 횟수

    def __str__(self):
        # 캐시의 현재 상태를 문자열로 반환하는 메소드, 디버깅 용도
        heap_str = "\nHeap : "
        for item in self.heap:
            heap_str += f"{item.lpn}(f: {item.freq} t: {item.tot_cnt}) "
        return heap_str

    def is_empty(self):
        # 힙이 비었는지 확인하는 메소드
        return len(self.heap) == 0

    def get(self, key):
        # 주어진 키에 해당하는 캐시 아이템을 검색하는 메소드
        for item in self.heap:
            if item.lpn == key:
                return item
        return None

    def get_index(self, key):
        # 주어진 키의 인덱스를 반환하는 메소드
        for i, item in enumerate(self.heap):
            if item.lpn == key:
                return i
        return None

    def percolate_up(self, index):
        # 부모 노드의 인덱스를 계산하는 공식
        parent = (index - 1) // 2

        # 만약 현재 노드가 루트 노드가 아니고, 현재 노드가 부모 노드보다 작다면 위치를 교환
        if index > 0 and self.heap[index] < self.heap[parent]:
            # 현재 노드와 부모 노드의 위치를 교환
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            # 위치 교환 후, 재귀적으로 부모 노드에서도 동일한 과정을 반복하여 힙 속성 유지
            self.percolate_up(parent)

    def percolate_down(self, index):
        # 현재 인덱스의 왼쪽 자식 노드 인덱스 계산
        left_index = 2 * index + 1
        # 현재 인덱스의 오른쪽 자식 노드 인덱스 계산
        right_index = 2 * index + 2

        # 왼쪽 자식 인덱스가 힙의 크기 내에 있는지 확인
        if left_index <= len(self.heap) - 1:
            # 오른쪽 자식도 힙의 크기 내에 있고, 오른쪽 자식이 왼쪽 자식보다 작은 경우
            if (right_index <= len(self.heap) - 1) and (
                self.heap[left_index] > self.heap[right_index]
            ):
                # 왼쪽 자식 대신 오른쪽 자식과 비교/교환하기 위해 인덱스 변경
                left_index = right_index

            # 현재 노드가 선택된 자식 노드보다 큰 경우 위치 교환
            if self.heap[index] > self.heap[left_index]:
                # 현재 노드와 자식 노드의 위치를 교환
                self.heap[index], self.heap[left_index] = (
                    self.heap[left_index],
                    self.heap[index],
                )
                # 위치 교환 후, 재귀적으로 해당 자식 노드에서도 동일한 과정을 반복하여 힙 속성 유지
                self.percolate_down(left_index)

    def extract_min(self):
        # 힙이 비어 있는지 확인
        if self.is_empty():
            return None  # 힙이 비어있다면 None 반환

        # 힙의 첫 번째 요소(최소값)를 min_item에 저장
        min_item = self.heap[0]

        # 힙의 마지막 요소를 힙의 첫 번째 위치로 이동
        self.heap[0] = self.heap.pop()

        # 새로운 루트 요소에 대해 힙 속성을 유지하도록 아래로 이동시키기
        self.percolate_down(0)

        # 최소값을 반환
        return min_item

    def insert(self, key):
        # print(self)  # For debugging
        # 총 요청 카운트를 1 증가
        self.tot_cnt += 1

        # 주어진 키에 해당하는 노드 검색
        node = self.get(key)
        # 노드의 인덱스
        index = self.get_index(key)

        # 캐시 히트인 경우: 해당 키가 이미 캐시에 있을 때
        if node:
            # 노드의 사용 빈도수 증가
            node.freq += 1
            # 키에 대응하는 빈도수 사전 업데이트
            self.lpn_to_freq[key] += 1

            # 해당 노드의 위치를 힙에서 상위로 조정
            self.percolate_up(len(self.heap) - 1)
            # 해당 노드 아래를 힙 속성을 유지하도록 조정
            self.percolate_down(index)

            # print("HIT  : ", node.lpn)  # For debugging

            # 캐시 히트 수 증가
            self.cache_hit += 1
        else:
            # 캐시 슬롯이 가득 찼을 경우, 최소 노드를 제거
            if len(self.heap) >= self.cache_slots:
                extracted_node = self.extract_min()

                # print("EVICT: ", extracted_node.lpn)  # For debugging

            # 새 노드의 빈도를 설정
            new_freq = 1
            # 키가 이미 빈도 사전에 있으면, 빈도 증가 후 딕셔너리 업데이트
            if key in self.lpn_to_freq:
                new_freq += self.lpn_to_freq[key]
                self.lpn_to_freq[key] += 1
            else:
                # 키가 새로 삽입되는 경우, new_freq(==1)로 설정
                self.lpn_to_freq[key] = new_freq

            # 새 캐시 아이템을 힙에 추가
            new_node = CacheItem(key, self.tot_cnt, new_freq)
            self.heap.append(new_node)
            # 새로 추가된 노드의 위치를 힙에서 상위로 조정
            self.percolate_up(len(self.heap) - 1)

            # print("MISS : ", key)  # For debugging


def lfu_sim(cache_slots):
    cache_hit = 0
    tot_cnt = 0
    data_file = open("linkbench.trc")

    cache = LFUCache(cache_slots)
    for line in data_file.readlines():
        lpn = line.split()[0]

        # Program here
        cache.insert(lpn)

    cache_hit = cache.cache_hit
    tot_cnt = cache.tot_cnt
    print(
        "cache_slot = ",
        cache_slots,
        "cache_hit = ",
        cache_hit,
        "tot_cnt = ",
        tot_cnt,
        "hit ratio = ",
        cache_hit / tot_cnt,
    )

    data_file.close()


if __name__ == "__main__":
    for cache_slots in range(100, 1000, 100):
        lfu_sim(cache_slots)
    # lfu_sim(100)
