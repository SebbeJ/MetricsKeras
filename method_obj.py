import re
import unittest

'''
To do:
    Bättre kod: 
    ***Gör automatiska test cases
    -Dela upp i mindre metoder
    -Skriv ordentliga kommentarer

    Utökad funktionalitet:
    *Implementera weight till genomsnitt
    -Ge filer och metoder mer data
        -Kommentarer/docstrings
        -Längd i rader (filer)
        -Average längd
    -Ignorera tomma folders/filer för genomsnittet
    -Gör om till console commands

    Presenteation:
    -Implementera depth
    -Implementera visualisering
'''

class method:
    def __init__(self, name, parent, indent):
        self.name = name
        self.parent = parent
        self.indent = indent
        self.line_count = 0
        self.comments = 0
        self.docstrings = 0
    
    def inc_line_count(self, inc = 1):
        self.line_count += inc

    def get_name(self):
        return self.name
    
    def get_line_count(self):
        return self.line_count
    
    def get_indent(self):
        return self.indent

    def get_parent(self):
        return self.parent
    
class file():
    def __init__(self, name, type, path):
        self.name = name
        self.type = type
        self.abs_path = path.replace("\\", "/")

        self.children = []
        self.len = 0
        self.mean_method_size = 0
        self.weight = 0
        self.no_of_comments = 0
        self.no_of_docstring = 0
        self.line_size = 0
        self.average_line_size = 0
    
    def add_child(self, child):
        self.children.append(child)

    def calc_mean(self):
        total = 0
        if self.type == "file":
            methods = count_method_lines(self.abs_path)
            
            self.mean_method_size, self.weight = compile_method_data(methods)

            return self.mean_method_size
        elif self.type == "folder":
            print(self.abs_path)

            for child in self.children:
                child_weight = child.get_weight()
                self.weight += child_weight
                total += child.get_mean_method_size() * child_weight

            if self.weight == 0: return 0

            self.mean_method_size = total/self.weight
            return self.mean_method_size
    
    def get_mean_method_size(self):
        return self.mean_method_size
    
    def get_weight(self):
        return self.weight
    
    def get_children(self):
        return self.children
    
    def retrieve_data(self, saved_data, name ="", level=0):
        if name != "":
            abs_name = name + "/" + self.name
        else:
            abs_name = self.name

        
        # print(f"name type: {self.name}, mean type: {type(self.mean_method_size)}, weight type: {type(self.weight)}")
        saved_data[abs_name] = {"Type": self.type, "mean method size": round(self.mean_method_size, 2), "weight": self.weight, "level": level}
        for child in self.children:
            child.retrieve_data(saved_data, abs_name, level +1)
        

    def print_structure(self, level=0):
        """Helper method to print the structure of the tree."""
        indent = " " * (level * 4)
        print(f"{indent}{self.name} (Type: {self.type}, mean method size: {self.mean_method_size})")
        for child in self.children:
            child.print_structure(level + 1)
        
    

def find_end(line):
    string_without_spaces = line.replace(" ", "").replace("\n", "").replace("\t", "")
    previous = ""
    for i in string_without_spaces:
        if i == ":" and previous == ")":
            return True
        previous = i
    return False



def count_method_lines(file_path):
    method_regex = re.compile(r'^\s*def\s+(\w+)\s*\(')  
    decorator_regex = re.compile(r'^\s*@')  
    decorator_unended_regex = re.compile(r'^\s*@\w+.*\(\s*$|^\s*@\w+.*\(\s*#')
    comment_regex = re.compile(r'^\s*#(.)*')
    # docstring_regex = re.compile(r'^\s*(\'\'\'|\"\"\")|(\'\'\'|\"\"\")\s*$')
    docstring_regex = re.compile(r'(\'\'\'|\"\"\")')
    fake_docstring_regex = re.compile(r'(\'\'\'|\"\"\")')
    param_end_regex = re.compile(r'\):(#(.)*|\t*|\r*|\s*)*$')

    end_parant_regex = re.compile(r'\)')
    start_parant_regex = re.compile(r'\(')
    parant_count = 0

    methods = {}  
    line_count = 0

    current_method = None
    inside_docstring = False
    doscstring_type = None
    inside_docstring = False
    docstring_type = None
    inside_parameters = False
    end_was_not_found = False
    end_params_check = False
    ongoing_decorator = False
    parant_end_check = None
    parant_start_check = None

    with open(file_path, 'r', errors="ignore") as file:
        print(f"Current file: {file_path}")
        for line in file:

            stripped_line = line.strip()
            expanded_line = line.replace('\t', ' ' * 4)

            # skipa tomma rader och simpla hashtag kommentarer
            comment_check = comment_regex.match(line)


            if not stripped_line or (comment_check != None):
                continue


            docstring_check = docstring_regex.findall(line)

            if docstring_check:

                if not inside_docstring:
                    inside_docstring = True
                    docstring_type = docstring_check[0]  # ''' eller """
                    

                    if len(docstring_check) == 2:
                        inside_docstring = False
                        docstring_type = None
                else:
                    if docstring_check[0] == docstring_type:
                        inside_docstring = False
                        docstring_type = None
                continue

            if inside_docstring:
                continue

            indent_level = len(expanded_line) - len(expanded_line.lstrip())
            # print("-------------------------------------------")
            # print(line)
            # if current_method:
            #     print(f"current method: {current_method.get_name()}")
            #     print(f"Current indent: {indent_level}")
            #     print(f"Method indent: {current_method.get_indent()}")
            #     if current_method.parent:
            #         print(f"Method parent: {current_method.parent.get_name()}")
            #     else:
            #         print("Current method is an orphan")
            # else:
            #     print("Not inside method")
            #     print(f"Current indent: {indent_level}")
            # print(f"End not found: {end_was_not_found}")
            # print(f"Inside params: {inside_parameters}")
            

            match = method_regex.match(line)

            if ongoing_decorator:
                parant_start_check = start_parant_regex.match(line)
                if parant_start_check:
                    for l in parant_start_check:
                        parant_count += 1
                    parant_end_check = end_parant_regex.match(line)
                if parant_end_check:
                    for l in parant_end_check:
                        parant_count -= 1
                if parant_count == 0:
                    ongoing_decorator = False
                else: continue
            
            if decorator_unended_regex.match(line):
                ongoing_decorator = True
                parant_count = 1
                continue
            elif decorator_regex.match(line):
                continue  

            if current_method != None:
                method_indent = current_method.get_indent()
            else:
                method_indent = -1
            
            # print(f"Inside parameter: {inside_parameters}")


            if match != None and not inside_parameters:
                
                # end_params_check = param_end_regex.match(line)
                # print(f'CHECKEN: {end_params_check}')
                # print(f'Checken är {param_end_regex.pattern}')
                
                if find_end(line):
                    # print("Hittar slutet")
                    inside_parameters = False
                else:
                    # print("Hittar inte slutet: i line: " + line)
                    inside_parameters = True
                
                if current_method is not None:
                    methods[current_method.get_name()] = current_method.get_line_count()  

               
                parent = None
                method_to_compare = current_method
                while method_to_compare != None:
                    if method_to_compare.get_indent() < indent_level:
                        parent = method_to_compare
                        break
                    method_to_compare = method_to_compare.get_parent()
                    
                # Checkar ifall en inre metod påbörjas
                
                # print(f'Name: {match.group(1)}, parent: {parent}, indent level: {indent_level}')
                current_method = method(match.group(1), parent, indent_level)

            elif match == None and (method_indent >= indent_level and indent_level != 0 and not end_was_not_found and not inside_parameters):
                # print("000")
                # print(f'Method indent: {method_indent}, Indent level: {indent_level}')
                #Ifall den inre metoden har tagit slut byter vi till föräldra metoden
                lines_counted = current_method.get_line_count()
                methods[current_method.get_name()] = lines_counted
                current_method = current_method.get_parent()
                if parent:
                    current_method.inc_line_count()
                    #Lägger till inre metodens line count till förälderns
                    current_method.inc_line_count(lines_counted)
            elif match == None and (method_indent >= indent_level or indent_level == 0) and not end_was_not_found and not inside_parameters:
                # print("111")
                #Ifall det är kod som inte tillhör någon metod
                if current_method:
                    methods[current_method.get_name()] = current_method.get_line_count()
                current_method = None
            elif current_method is not None and not inside_parameters:
                # print("22222")
                current_method.inc_line_count()  
            if inside_parameters:
                end_params_check = find_end(line)
            if end_params_check:
                inside_parameters = False

            if inside_parameters: end_was_not_found = True
            else: end_was_not_found = False

        if current_method is not None:
            methods[current_method.get_name()] = current_method.get_line_count()
    
    return methods


def compile_method_data(method_dict):
    values = method_dict.values()
    if len(values) == 0:
        return 0, 0
    mean = sum(values)/len(values)
    return mean, len(values)
