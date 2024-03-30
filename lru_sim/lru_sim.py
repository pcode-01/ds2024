class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache = [-1] * cache_slots  # 초기 캐시는 -1로 채워진 배열        
        self.cache_hit = 0
        self.tot_cnt = 1
    
    def do_sim(self, page):
        self.tot_cnt += 1
        
        # 캐시에 페이지가 있는지 확인
        if page in self.cache:
            self.cache.remove(page)  # 페이지를 캐시에서 제거하여 가장 최근으로 만듦
            self.cache.append(page)  # 페이지를 다시 캐시에 추가하여 가장 최신으로 만듦
            self.cache_hit += 1  # 캐시 히트
        else:
            # 캐시에 페이지가 없는 경우
            if self.cache[-1] != -1:
                self.cache.pop(0)  # 캐시가 가득 차면 가장 오래된 페이지를 제거
            self.cache.append(page)  # 새로운 페이지 추가
        
    def print_stats(self):
        hit_ratio = "{:.5f}".format(self.cache_hit / self.tot_cnt)
        print("cache_slot =", self.cache_slots, "cache_hit =", self.cache_hit, "hit ratio =", hit_ratio)

if __name__ == "__main__":
    data_file = open("./lru_sim/linkbench.trc")
    lines = data_file.readlines()
    for cache_slots in range(100, 1001, 100):
        cache_sim = CacheSimulator(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)
        
        cache_sim.print_stats()
