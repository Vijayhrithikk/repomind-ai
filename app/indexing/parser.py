from pathlib import Path

from tree_sitter import Language
from tree_sitter import Parser

import tree_sitter_go

GO_LANGUAGE = Language(tree_sitter_go.language())

parser = Parser(GO_LANGUAGE)

class FunctionChunk:
    def __init__(self, file_path:str,function_name: str,content: str):
        self.file_path=file_path 
        self.function_name=function_name
        self.content=content 

    def extract_functions(file_path:str):
        source=Path(file_path).read_text(encoding="utf-8",errors="ignore")

        tree=parser.parse(source.encode())

        root=tree.root_node

        chunks=[]

        for node in root.children:
            if node.type!="function_declaration":
                continue 
            name_node = node.child_by_field_name("name")

            if not name_node:
                continue 
            function_name=source[name_node.start_byte:name_node.end_byte]

            content=source[node.start_byte:node.end_byte]
            chunks.append(FunctionChunk(file_path=file_path,function_name=function_name,content=content))
        return chunks


def extract_functions(file_path:str):
        source=Path(file_path).read_text(encoding="utf-8",errors="ignore")

        tree=parser.parse(source.encode())

        root=tree.root_node

        chunks=[]

        for node in root.children:
            if node.type!="function_declaration":
                continue 
            name_node = node.child_by_field_name("name")

            if not name_node:
                continue 
            function_name=source[name_node.start_byte:name_node.end_byte]

            content=source[node.start_byte:node.end_byte]
            chunks.append(FunctionChunk(file_path=file_path,function_name=function_name,content=content))
        return chunks