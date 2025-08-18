class MoveLoader:
    VALID_DIRECTIONS = {"up", "down", "left", "right"}

    @staticmethod
    def load_from_file(file_path: str) -> list[str]:
        """
        Load moves from a file. Each line should contain a single move direction.
        Valid directions are: up, down, left, right.
        """
        moves = []
        try:
            with open(file_path, "r") as file:
                for line in file:
                    move = line.strip().lower()
                    if move in MoveLoader.VALID_DIRECTIONS:
                        moves.append(move)
                    else:
                        raise ValueError(f"Invalid move direction: {move}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Error reading file {file_path}: {e}")
        if not moves:
            raise ValueError("No valid moves found in the file.")
        return moves
