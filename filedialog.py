from pathlib import Path
from typing import Type, Any



class Text_FileDialog:
    def __init__(self, root: str | Path | list[str] | tuple[str], canOpenFiles: bool = False):
        self.__root = ''
        if isinstance(root, (list, tuple)):
            for r in root: self.__root = Path(self.__root, r)
        self.__root = str(root)
        if not Path(self.__root).exists(): self.__Root404Error()
        self.__canRunDialog = True
        self.__canOpenFiles = canOpenFiles
    
    def __Root404Error(self):
        print(f"path '{self.__root}' does not exist")
        raise SystemExit()
    
    def __getLastInPath(self, path: str | Path): return str(path).rsplit('/', 1)[-1]
    
    def run(self):
        self.__help()
        while self.__canRunDialog:
            inp = input(f"{self.__getLastInPath(self.__root)}/ > ").strip().split(' ', 1)
            if len(inp) > 1: output = self.__getcommand(inp[0], inp[1])
            else: output = self.__getcommand(inp[0], None)
            if output: return output

    def __command404(self, command: str): print(f"unknown command '{command}'")

    def __getcommand(self, command: str, input: str | Path | None):
        match command.casefold():
            case 'help': self.__help()
            case 'cd': self.__cd(input)
            case 'ls': self.__ls(input)
            case 'cat': self.__cat(input)
            case 'open' | 'file':
                opened = self.__openfile(input)
                if opened: return opened
            case x: self.__command404(command)

    def close(self): self.__canRunDialog = False

    def __help(self):
        messages = [
            "'exit': exits the file dialog"
            "'help': shows this message",
            "'cd' [directory]: moves into the given directory, use '..' to move into the previous directory",
            "'ls': shows the contents of the current folder",
            "'cat' [file]: shows the contents of the given file"
        ]
        for m in messages: print(m)
        if self.__canOpenFiles: print("'open' [file]: open a file(if supported)")
    
    def exit(self): self.__canRunDialog = False
    
    def __cd(self, directory: str | Path | None) -> bool:
        if directory == None: return False
        if directory == '..':
            self.__root = str(Path('../', self.__root))
            return True
        newroot = Path(self.__root, directory)
        if not newroot.exists(): print(f"directory '{directory}' does not exist"); return False
        self.__root = newroot
        return True
    
    def __ls(self, directory: str | Path = None) -> bool:
        print(f"from current folder '{self.__getLastInPath(self.__root)}'")
        if directory != None:
            if not Path(directory).exists(): print(f"path '{directory}' does not exist"); return False
        path = Path(self.__root, directory) if directory != None else Path(self.__root)
        for d in path.iterdir(): print(self.__getLastInPath(d))
        return True
    
    def __cat(self, file: str | Path | None) -> bool:
        if file == None: return False
        if not Path(self.__root, file).exists(): print(f"file '{file}' does not exist"); return False
        with open(Path(self.__root, file), 'rt') as f: print(f.read())
        return True
    
    def __openfile(self, file: str | Path | None):
        if not self.__canOpenFiles: return
        if not Path(self.__root, file).exists(): print(f"file '{file}' does not exist"); return
        return str(Path(self.__root, file))