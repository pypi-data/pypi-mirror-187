from pathlib import Path

from printbuddies import ProgBar, clear, print_in_place


class TreeGenerator:
    """Generates a nested dictionary of arbitrary depth
    representing the subdirectories of a given directory."""

    def __init__(self, starting_directory: str | Path):
        self.starting_dir = Path(starting_directory)
        self.paths = [self.starting_dir]
        self._pipe = "|"
        self._tee = "|-"
        self._elbow = "|_"
        self.generate()

    def generate(self):
        self.paths.extend(self._crawl(self.starting_dir))
        clear()
        self._drop_parents()
        self._generate_tree()
        self._generate_tree_string()

    def _drop_parents(self):
        self.paths = [
            Path(str(path)[str(path).find(self.starting_dir.stem) :])
            for path in self.paths
        ]

    def __str__(self):
        return f"{self.tree_string}"

    def _crawl(self, start_dir: Path) -> list[Path]:
        """Generate recursive list of paths by crawling
        down every branch from the starting_dir."""
        paths = []
        print_in_place(f"Crawling {start_dir}...")
        for item in start_dir.iterdir():
            if item.is_file():
                paths.append(item)
            elif item.is_dir():
                paths.extend(self._crawl(item))
                print_in_place(f"Crawling {start_dir}...")
        return paths

    def _generate_tree(self):
        """Generate nested dictionary of subdirectories."""
        self.tree = {}
        prog_bar = ProgBar(len(self.paths))
        prog_bar.display()
        for path in sorted(self.paths):
            if path.parts[0] not in self.tree:
                self.tree[path.parts[0]] = {}
            current_layer = self.tree[path.parts[0]]
            branches = path.parts[1:]
            for branch in branches:
                if branch not in current_layer:
                    current_layer[branch] = {}
                current_layer = current_layer[branch]
            prog_bar.display()

    def _format_branch_name(self, branch_name: str, index: int) -> str:
        if index == 0:
            return f"{branch_name}\n"
        elif index == 1:
            return f'{self._pipe}{"  "*index}{self._tee}{branch_name}\n'
        else:
            return (
                f'{self._pipe}{("  "+self._pipe)*(index-1)}  {self._tee}{branch_name}\n'
            )

    def _convert_branch_to_string(
        self, branch: dict, branch_name: str, index: int
    ) -> str:
        """Iterates through a nested dictionary and returns a string representation."""
        output = self._format_branch_name(branch_name, index)
        for i, leaf in enumerate(branch.keys()):
            if branch[leaf] == {}:
                output += f'{self._pipe}{("  "+self._pipe)*index}  '
                if i == len(branch.keys()) - 1:
                    output += f"{self._elbow}{leaf}\n"
                    output += f'{self._pipe}{("  "+self._pipe)*index}\n'
                else:
                    output += f"{self._tee}{leaf}\n"
            else:
                output += self._convert_branch_to_string(branch[leaf], leaf, index + 1)
        return output

    def _trim_tree(self):
        tree = self.tree_string.splitlines()
        self.tree_string = ""
        for i, line in enumerate(tree[:-1]):
            if (
                all(ch in f"{self._pipe} " for ch in line)
                and i < len(tree) - 2
                and self._tee in tree[i + 1]
            ):
                self.tree_string += f"{line[:tree[i+1].find(self._tee)+1]}\n"
            else:
                self.tree_string += f"{line}\n"

    def _generate_tree_string(self):
        """Generates formatted string representation of
        the directory tree."""
        self.tree_string = ""
        for root in self.tree.keys():
            self.tree_string += self._convert_branch_to_string(self.tree[root], root, 0)
        self._trim_tree()


class UrlTreeGenerator(TreeGenerator):
    """Generates a tree representation of a given list of urls."""

    def __init__(self, urls: list[str]):
        self.paths = [Path(url) for url in urls]
        self._pipe = "|"
        self._tee = "|-"
        self._elbow = "|_"

    def generate(self):
        self._generate_tree()
        self._generate_tree_string()
