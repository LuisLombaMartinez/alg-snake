from collections import deque
from ai.algorithm import PathAlgorithm


class BFS(PathAlgorithm):
    def find_path(self, start, goal, blocked, grid_size, max_steps=None, prev=None):
        width, height = grid_size
        queue = deque([start])
        came_from = {start: None}
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        steps = 0

        while queue:
            if max_steps is not None and steps >= max_steps:
                break
            steps += 1

            cur = queue.popleft()
            if cur == goal:
                break
            for dx, dy in dirs:
                nxt = (cur[0] + dx, cur[1] + dy)
                if (
                    0 <= nxt[0] < width
                    and 0 <= nxt[1] < height
                    and nxt not in came_from
                    and nxt not in blocked
                ):
                    queue.append(nxt)
                    came_from[nxt] = cur

        if goal not in came_from or steps >= max_steps:
            return [self.get_random_move(start)], steps

        path = []
        cur = goal
        while cur != start:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        return path, steps  # Return path and number of steps taken
