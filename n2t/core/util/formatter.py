class TabDepth:
    @classmethod
    def with_depth(cls, string: str, depth: int) -> str:
        return "\t" * depth + string
