import re

'''
To do:
    Bättre kod: 
    ***Gör automatiska test cases
    -Dela upp i mindre metoder
    *Skriv ordentliga kommentarer

    Utökad funktionalitet:
    *Implementera weight till genomsnitt
    -Ge filer och metoder mer data
        *Kommentarer/docstrings
        -Längd i rader (filer)
        *Average längd
    *Ignorera tomma folders/filer för genomsnittet
    -Gör om till console commands

    Presenteation:
    *Implementera depth
    -Implementera visualisering
'''

class method: 
    '''A class to save information about methods, mostly setter and getters'''
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
    '''Says file but is covers folders as well, it is here the magic happens'''
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

    def calc_mean(self, include_inside_method = True):
        '''Calculates all relevant information, started of as only counting the means so that's why the name is like that'''
        if self.type == "file": #In case it is a file 
            methods = count_method_lines(self.abs_path, include_inside_method) #Creates a structure of methods with relevant information
            
            self.mean_method_size, self.weight, self.max_lines, self.min_lines, self.mean_comments, self.mean_docstring, self.mean_comment_docstring = compile_method_data(methods) #collects all the data, yeah it is too much

        elif self.type == "folder": #in case it is a folder
            line_total = 0
            comment_total = 0
            docstring_total = 0
            comment_docstring_total = 0

            if len(self.children) == 0: #No use in doing it if it is an empty folder
                return

            for child in self.children: #goes through all everything in the folder and compiles the information
                child_weight = child.get_weight()
                self.weight += child_weight #The wheight is the ammount of methods in each file/folder, very important to calculate the mean
                line_total += child.get_mean_method_size() * child_weight 
                comment_total += child.get_comment_mean() *child_weight
                docstring_total += child.get_docstring_mean() * child_weight
                comment_docstring_total += child.get_mean_comment_docstring() * child_weight

                if child.get_max() > self.max_lines:
                    self.max_lines = child.get_max()
                if (child.get_min() < self.min_lines or self.min_lines == -1) and child.get_min() != -1: #Had to make sure that empty folders doesnt count
                    self.min_lines = child.get_min() 
            
            if self.weight == 0: #Deals with the case when the folders doesn't have children
                self.min_lines = -1 #-1 indicates that the folder had no methods
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
        '''Compiles the data into a string, only used for testing'''
        if name != "":
            abs_name = name + "/" + self.name
        else:
            abs_name = self.name

        saved_data[abs_name] = {"Type": self.type, "mean method size": round(self.mean_method_size, 2), "weight": self.weight, "level": level}
        for child in self.children:
            child.retrieve_data(saved_data, abs_name, level +1)
        

    def print_structure(self, level=0, max_level = None, mean_method= True, max=True, min=True, mean_comments=False, mean_comment_per_line = False, mean_docstring=False, mean_docstring_comment = False):
        '''Prints the entire structure of the tree'''
        indent = " " * (level * 4)
        string_to_print = f"{indent}{self.name} (Type: {self.type}"
        
        #Prints all the values requested
        if mean_method:
            string_to_print += f", mean method size: {self.mean_method_size}"
        if max:
            string_to_print += f", size of biggest method: {self.max_lines}"
        if min:
            string_to_print += f", size of smallest method: {self.min_lines}"
        if mean_comments:
            string_to_print += f", mean ammount of comments per method: {self.mean_comments}"
        if mean_comment_per_line:
            print_value = 0
            if self.mean_method_size != 0:
                print_value = self.mean_comments/self.mean_method_size
            else:
                print_value = "-"
            string_to_print += f", mean ammount of comments per line in method: {print_value}"
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
            child.print_structure(level + 1, max_level, mean_method, max, min, mean_comments, mean_comment_per_line, mean_docstring, mean_docstring_comment)
        
    

def find_end(line):
    '''Used to see if method definition has ended, regex failed me on this point so I made my own function'''
    string_without_spaces = line.replace(" ", "").replace("\n", "").replace("\t", "")
    
    for i in string_without_spaces:
        if i == ":":
            return True
        previous = i
    return False

def find_parent(method, indent):
    '''
    Finds the parent function of the function
    Mostly wouldn't be needed if not for weird edge-cases
    '''
    parent = None
    method_to_compare = method
    while method_to_compare != None:
        if method_to_compare.get_indent() < indent:
            parent = method_to_compare
            break
        method_to_compare = method_to_compare.get_parent()
    return parent

def simple_inc(method, line, inside_docstring):
    '''Deals counts the line correctly depending on if it is a docstring, comment or normal line
    doesn't handle the case where a docstring is written after a normal line and some other weird cases
    that we actually couldnt find after looking at the code
    '''
    if line.strip().startswith("#"):  # Check if the entire string is a comment
        method.inc_comments()
    elif inside_docstring or (line.strip().startswith('\'\'\'') and line.strip().endswith('\'\'\'')) or (line.strip().startswith('\"\"\"') and line.strip().endswith('\"\"\"')): #Checks if the string is a docstring
        method.inc_docstring()
    else: #In case it actually a normal line of code
        method.inc_line_count()  
        if '#' in line: # Check if the string contains a comment
            method.inc_comments()

def inc_parent(method):
    '''Adds the childs values to the parents, only used if we count the child method as 
    part of the parent
    '''
    parent = method.get_parent()
    if parent:
        lines_counted = method.get_line_count()
        comments_counted = method.get_comments()
        docstrings_counted = method.get_docstring()

        parent.inc_line_count(lines_counted)
        parent.inc_comments(comments_counted)
        parent.inc_docstring(docstrings_counted)

def count_method_lines(file_path, include_inside_method = True):
    '''
    Goes through a file and gathers information about all methods present
    avert your eyes, the horror begins
    '''

    #Bunch of regex that will be used later on
    method_regex = re.compile(r'^\s*def\s+(\w+)\s*\(')  
    decorator_regex = re.compile(r'^\s*@')  
    decorator_unended_regex = re.compile(r'^\s*@\w+.*\(\s*$|^\s*@\w+.*\(\s*#')
    comment_regex = re.compile(r'^\s*#(.)*')
    docstring_regex = re.compile(r'(\'\'\'|\"\"\")')

    #specific cases if the parameters for a function stretch multiple lines
    end_parant_regex = re.compile(r'\)')
    start_parant_regex = re.compile(r'\(')
    parant_count = 0

    #method dict that will be returned
    methods = {}  

    #some really ugly booleans to keep track of things
    current_method = None
    inside_docstring = False
    inside_docstring = False
    docstring_type = None
    inside_parameters = False
    end_was_not_found = False
    end_params_check = False
    ongoing_decorator = False
    parant_end_check = None
    parant_start_check = None

    with open(file_path, 'r', errors="ignore") as file:
        for line in file: #goes through the file line by line

            stripped_line = line.strip()
            expanded_line = line.replace('\t', ' ' * 4)#Used to keep track of indent


            if not stripped_line: #Ignores empty lines
                continue

            docstring_check = docstring_regex.findall(line)

            if docstring_check: #Checks if we find docstring
                if not inside_docstring: #Begins docstring
                    inside_docstring = True
                    docstring_type = docstring_check[0]  # ''' or """

                    if len(docstring_check) == 2: #Means that the docstring starts and ends on the same line
                        inside_docstring = False
                        docstring_type = None
                else: #Ends docstring
                    if docstring_check[0] == docstring_type:
                        inside_docstring = False
                        docstring_type = None

            indent_level = len(expanded_line) - len(expanded_line.lstrip()) #Compares the length of line without whitespace and with, aka aquires the indent
        


            if ongoing_decorator: #Deals with decorators, the work of the devil 
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

            #Aquires the expected indent of the method to later compare with the actual indent
            if current_method != None:
                method_indent = current_method.get_indent()
            else:
                method_indent = -1
            
            match = method_regex.match(line) #Checks if there is a method
            if match != None and not inside_parameters and not inside_docstring: #There was a method!
                
                if find_end(line): #Checks if the parameters ends on the same line as the method
                    inside_parameters = False
                else:
                    inside_parameters = True
                

                if current_method is not None: #If we were currently counting a method, we add it to the methods dict
                    methods[current_method.get_name()] = current_method

                    if include_inside_method: #adds it's data to the parent as well if we count it as part of the parent
                        inc_parent(current_method)

               
                parent = find_parent(current_method, indent_level) #find parent if there was one
                    
                
                current_method = method(match.group(1), parent, indent_level) #Creates the new method we found

                if '#' in line: #can be a comment on the line so made sure to count it to the new method
                    current_method.inc_comments()

            elif match == None and method_indent >= indent_level and not end_was_not_found and not inside_parameters: #the case when a method ends without a new one

                if current_method:
                    methods[current_method.get_name()] = current_method #Saves the method
                if include_inside_method:
                    inc_parent(current_method) 

                parent = find_parent(current_method, indent_level)
                current_method = parent #Goes back one step, to either parent method or the "baseline"
                if current_method:
                    simple_inc(current_method, line, inside_docstring) #increments line count if relevant

            elif current_method is not None and not inside_parameters: #normal line without method
                simple_inc(current_method, line, inside_docstring)
            
            if inside_parameters: #checks if the parameter has ended
                end_params_check = find_end(line)
            if end_params_check:
                inside_parameters = False

            if inside_parameters: end_was_not_found = True #yeah idk
            else: end_was_not_found = False

        if current_method is not None: #in case we get to the end of the file while inside a method
            if include_inside_method:
                inc_parent(current_method)
            methods[current_method.get_name()] = current_method
    
    return methods


def compile_method_data(method_dict):
    '''Compiles all data about the methods in a file'''
    methods = list(method_dict.values())
    if len(methods) == 0:
        return 0, 0, 0, -1, 0, 0, 0 #in case there was no methods in the file
    
    line_values = []
    comment_values = []
    docstring_values = []
    for m in methods:
        line_values.append(m.get_line_count())
        comment_values.append(m.get_comments())
        docstring_values.append(m.get_docstring())


    
    weight = len(line_values)
    line_mean = sum(line_values)/weight
    mean_comments = sum(comment_values)/weight #count comment per line
    mean_docstring = sum(docstring_values)/weight #but docstring per method
    mean_comment_docstring = (sum(docstring_values) + sum(comment_values))/weight #tracks them both, not used in the report
    return line_mean, len(line_values), max(line_values), min(line_values), mean_comments, mean_docstring, mean_comment_docstring
