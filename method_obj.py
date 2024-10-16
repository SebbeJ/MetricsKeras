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

    def inc_comments(self, inc = 1):
        self.comments += inc
    
    def get_comments(self):
        return self.comments

    def inc_docstring(self, inc=1):
        self.docstrings += inc
    
    def get_docstring(self):
        return self.docstrings

class file():
    def __init__(self, name, type, path):
        self.name = name
        self.type = type
        self.abs_path = path.replace("\\", "/")

        self.children = []
        self.len = 0

        self.weight = 0
        
        self.line_size = 0
        self.average_line_size = 0

        self.mean_comments = 0
        self.mean_docstring = 0
        self.mean_comment_docstring = 0
        self.max_lines = 0
        self.min_lines = -1
        self.mean_method_size = 0


    
    def add_child(self, child):
        self.children.append(child)

    def calc_mean(self):
        
        if self.type == "file":
            methods = count_method_lines(self.abs_path)
            
            self.mean_method_size, self.weight, self.max_lines, self.min_lines, self.mean_comments, self.mean_docstring, self.mean_comment_docstring = compile_method_data(methods)

        elif self.type == "folder":
            print(self.abs_path)
            line_total = 0
            comment_total = 0
            docstring_total = 0
            comment_docstring_total = 0

            if len(self.children) == 0:
                return

            for child in self.children:
                child_weight = child.get_weight()
                self.weight += child_weight
                line_total += child.get_mean_method_size() * child_weight
                comment_total += child.get_comment_mean() *child_weight
                docstring_total += child.get_docstring_mean() * child_weight
                comment_docstring_total += child.get_mean_comment_docstring() * child_weight

                if child.get_max() > self.max_lines:
                    self.max_lines = child.get_max()
                if (child.get_min() < self.min_lines or self.min_lines == -1) and child.get_min() != -1:
                    self.min_lines = child.get_min()
            
            if self.weight == 0:
                self.min_lines = -1
                return

            self.mean_method_size = line_total/self.weight
            self.mean_comments = comment_total/self.weight
            self.mean_docstring = docstring_total/self.weight
            self.mean_comment_docstring = comment_docstring_total/self.weight
    
    def get_mean_method_size(self):
        return self.mean_method_size

    def get_comment_mean(self):
        return self.mean_comments
    
    def get_docstring_mean(self):
        return self.mean_docstring
    
    def get_mean_comment_docstring(self):
        return self.mean_comment_docstring
    
    def get_weight(self):
        return self.weight
    
    def get_max(self):
        return self.max_lines
    
    def get_min(self):
        return self.min_lines
    
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
        

    def print_structure(self, level=0, max_level = None, mean_method= True, max=True, min=True, mean_comments=False, mean_docstring=False, mean_docstring_comment = False):
        """Helper method to print the structure of the tree."""
        indent = " " * (level * 4)
        string_to_print = f"{indent}{self.name} (Type: {self.type}"
        
        if mean_method:
            string_to_print += f", mean method size: {self.mean_method_size}"
        if max:
            string_to_print += f", size of biggest method: {self.max_lines}"
        if min:
            string_to_print += f", size of smallest method: {self.min_lines}"
        if mean_comments:
            string_to_print += f", mean ammount of comments per method: {self.mean_comments}"
        if mean_docstring:
            string_to_print += f", mean ammount of docstrings per method: {self.mean_docstring}"
        if mean_docstring_comment:
            string_to_print += f", mean ammount of both docstring and comment per method: {self.mean_comment_docstring}"
        string_to_print += ")"

        print(string_to_print)
        if max_level:
            if level == max_level:
                return

        for child in self.children:
            child.print_structure(level + 1, max_level, mean_method, max, min, mean_comments, mean_docstring, mean_docstring_comment)
        
    

def find_end(line):
    string_without_spaces = line.replace(" ", "").replace("\n", "").replace("\t", "")
    
    for i in string_without_spaces:
        if i == ":":
            return True
        previous = i
    return False

def find_parent(method, indent):
    parent = None
    method_to_compare = method
    while method_to_compare != None:
        if method_to_compare.get_indent() < indent:
            parent = method_to_compare
            break
        method_to_compare = method_to_compare.get_parent()
    return parent

def simple_inc(method, line, inside_docstring):
    if line.strip().startswith("#"):  # Check if the entire string is a comment
        # print("Finds it as only comment")
        method.inc_comments()
    elif inside_docstring or (line.strip().startswith('\'\'\'') and line.strip().endswith('\'\'\'')) or (line.strip().startswith('\"\"\"') and line.strip().endswith('\"\"\"')):
        method.inc_docstring()
        # print("Finds it as docstring")
    else:  # Check if the string contains a comment
        method.inc_line_count()  
        # print("Finds it as normal line")
        if '#' in line:
            method.inc_comments()
            # print("Finds it as comment too!")

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
        # print(f"Current file: {file_path}")
        for line in file:

            stripped_line = line.strip()
            expanded_line = line.replace('\t', ' ' * 4)

            # skipa tomma rader och simpla hashtag kommentarer
            comment_check = comment_regex.match(line)

            if not stripped_line:
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


            if match != None and not inside_parameters and not inside_docstring:
                
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
                    methods[current_method.get_name()] = current_method

                if current_method: 
                    if current_method.get_parent():
                        lines_counted = current_method.get_line_count()
                        comments_counted = current_method.get_comments()
                        docstrings_counted = current_method.get_docstring()

                        parent.inc_line_count(lines_counted)
                        parent.inc_comments(comments_counted)
                        parent.inc_docstring(docstrings_counted)

               
                parent = find_parent(current_method, indent_level)
                    
                # Checkar ifall en inre metod påbörjas
                
                # print(f'Name: {match.group(1)}, parent: {parent}, indent level: {indent_level}')
                current_method = method(match.group(1), parent, indent_level)
                if '#' in line:
                    current_method.inc_comments()

            elif match == None and method_indent >= indent_level and not end_was_not_found and not inside_parameters:
                # print("1111")
                lines_counted = current_method.get_line_count()
                comments_counted = current_method.get_comments()
                docstrings_counted = current_method.get_docstring()

                if current_method:
                    methods[current_method.get_name()] = current_method
                parent = find_parent(current_method, indent_level)
                if parent:
                    parent.inc_line_count(lines_counted)
                    parent.inc_comments(comments_counted)
                    parent.inc_docstring(docstrings_counted)

                
                current_method = parent
                if current_method:
                    simple_inc(current_method, line, inside_docstring)

            elif current_method is not None and not inside_parameters:
                # print("22222")
                simple_inc(current_method, line, inside_docstring)
            if inside_parameters:
                end_params_check = find_end(line)
            if end_params_check:
                inside_parameters = False

            if inside_parameters: end_was_not_found = True
            else: end_was_not_found = False

        if current_method is not None:
            methods[current_method.get_name()] = current_method
    
    return methods


def compile_method_data(method_dict):
    methods = list(method_dict.values())
    if len(methods) == 0:
        return 0, 0, 0, -1, 0, 0, 0
    
    line_values = []
    comment_values = []
    docstring_values = []
    for m in methods:
        line_values.append(m.get_line_count())
        comment_values.append(m.get_comments())
        docstring_values.append(m.get_docstring())
        if m.get_line_count() == 0:
            print(f"{m.get_name()} har inga lines")


    
    weight = len(line_values)
    line_mean = sum(line_values)/weight
    mean_comments = sum(comment_values)/weight
    mean_docstring = sum(docstring_values)/weight
    mean_comment_docstring = (sum(docstring_values) + sum(comment_values))/weight
    return line_mean, len(line_values), max(line_values), min(line_values), mean_comments, mean_docstring, mean_comment_docstring
