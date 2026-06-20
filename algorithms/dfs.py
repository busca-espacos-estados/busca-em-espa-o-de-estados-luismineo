from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        stats = {'expanded': 0, 'generated': 1, 'max_frontier': 0}

        def _dfs(state, path_tiles):
            stats['expanded'] += 1
            if state.is_goal:
                return state
            if state.cost >= self.depth_limit:
                return None
            neighbors = [n for n in state.neighbors() if n.tiles not in path_tiles]
            stats['generated'] += len(neighbors)
            if len(neighbors) > stats['max_frontier']:
                stats['max_frontier'] = len(neighbors)
            for neighbor in neighbors:
                path_tiles.add(neighbor.tiles)
                found = _dfs(neighbor, path_tiles)
                if found is not None:
                    return found
                path_tiles.discard(neighbor.tiles)
            return None

        solution = _dfs(initial, {initial.tiles})
        return SearchResult(
            solution=solution,
            nodes_expanded=stats['expanded'],
            nodes_generated=stats['generated'],
            max_frontier_size=stats['max_frontier'],
            depth=solution.cost if solution else 0,
        )
