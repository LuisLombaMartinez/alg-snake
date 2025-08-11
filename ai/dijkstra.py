import heapq
from ai.algorithm import PathAlgorithm


class Dijkstra(PathAlgorithm):
    def find_path(self, start, goal, blocked, grid_size, max_steps=None, prev=None):
        width, height = grid_size
        heap = [(0, start)]
        came_from = {start: None}
        cost = {start: 0}
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        steps = 0

        while heap:
            if max_steps is not None and steps >= max_steps:
                break
            steps += 1

            cur_cost, cur = heapq.heappop(heap)
            if cur == goal:
                break
            for dx, dy in dirs:
                nxt = (cur[0] + dx, cur[1] + dy)
                if not (0 <= nxt[0] < width and 0 <= nxt[1] < height):
                    continue
                if nxt in blocked:
                    continue
                new_cost = cur_cost + 1
                if nxt not in cost or new_cost < cost[nxt]:
                    cost[nxt] = new_cost
                    heapq.heappush(heap, (new_cost, nxt))
                    came_from[nxt] = cur

        if goal not in came_from or steps >= max_steps:
            return [self.get_random_move(start, prev=prev)], steps

        path = []
        cur = goal
        while cur != start:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()

        return path, steps  # Return path and number of steps taken
