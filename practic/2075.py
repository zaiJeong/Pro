import heapq

heap = []
N = int(input())
for i in range(N):
    num_list = list(map(int, input().split()))
    for j in num_list:
        if len(heap) < N:
            heapq.heappush(heap, j)
        else :
            if heap[0] < j:
                heapq.heappop(heap)
                heapq.heappush(heap, j)

print(heap[0])
print("hi")