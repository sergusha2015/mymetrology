# -*- coding: utf-8 -*-
import re

def removeInCode(list_of_objects, code):
    list_of_delete_elements = []
    for item in list_of_objects:
        index_input = item.span()[0]
        index_output =item.span()[1]
        list_of_delete_elements.append(code[index_input: index_output])
    for item in list_of_delete_elements:
        code = code.replace(item, '')

def findEnd(list_elements, _elements):
    brackets_left_front = 0
    brackets_right_front = 0
    while brackets_left_front != brackets_right_front:
        if '}' in list_elements[_elements]:
            brackets_right_front += 1
            if brackets_right_front == brackets_left_front:
                break
        if '{' in list_elements[_elements]:
            brackets_left_front += 1
        _elements += 1
        if _elements == len(list_elements) - 1:
            break
    return _elements

def deleteComments(code):
    list = re.finditer(r'\'[^\']*\'', code)
    removeInCode(list, code)
    list = re.finditer(r'\"[^\"]*\"', code)
    removeInCode(list, code)
    list = re.finditer(r'/\*[\s*\S*]*\*/', code)
    removeInCode(list, code)
    list = re.finditer(r'\([^\)\(]*\)', code)
    removeInCode(list, code)
    list = re.finditer(r'//[^\n]*\n', code)
    removeInCode(list, code)
    list = re.finditer(r'var[^\;]*;', code)
    removeInCode(list, code)
    return code

def searchFunctions(code):
    list_of_functions = []
    list_search = re.finditer(r'\s*function[\s*\n*]*[a-zA-Z_0-9]+\s*[\s*\n*]*\{', code)
    for function in list_search:
        brackets_ltft_front = 1
        brackets_right_front = 0
        index_brackets_in_code = function.span()[1]
        while brackets_ltft_front != brackets_right_front:
            if code[index_brackets_in_code] == '{':
                brackets_ltft_front += 1
            elif code[index_brackets_in_code] == '}':
                brackets_right_front += 1
            index_brackets_in_code += 1
        list_of_functions.append(code[function.span()[0]:index_brackets_in_code])
    for function in list_of_functions:
        code = code.replace(function, '')
    return list_of_functions, code

def getFunctionsDictionary(list_of_functions):
    dictionary_of_functions={}
    for element in list_of_functions:
        function_code = element
        function_list = re.finditer(r'\s*function[\s*\n*]*[a-zA-Z_]',element)
        for function in function_list:
            delete_function_list = element[:function.span()[1]-1]
            element = element.replace(delete_function_list,'')
        function_list = re.finditer(r'[a-zA-Z_0-9]*\s*\{',element)
        for function in function_list:
            element = element[:function.span()[1]-1]
            index_element = function_code.index('{')
            dictionary_of_functions[element] = function_code[index_element + 1: len(function_code)-1]
    return dictionary_of_functions

def getMakkeybNumber(code):
    result = 1
    list = re.findall(r'\s*if[\s+\n*]*',code)
    list += re.findall(r'\s*for[\s+\n*]*',code)
    list += re.findall(r'\s*while[\s+\n*]*',code)
    result += len(list)
    return result

def main():
    source_data = open('source1.js', 'r')
    code_text = source_data.read()
    code_text = deleteComments(code_text)
    functions_listik, code_text = searchFunctions(code_text)
    functions_dictionary = getFunctionsDictionary(functions_listik)
    for key in functions_dictionary.keys():
        code_text = code_text.replace(key,'\n'+functions_dictionary[key]+'\n')
    print('\nNumber of Makkeyb:', getMakkeybNumber(code_text))

main()






















