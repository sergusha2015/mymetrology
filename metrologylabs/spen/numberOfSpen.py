# -*- coding: utf-8 -*-
import re


def delComments(code):

    dellist = []
    listiter = re.finditer(r'/\*[\s*\S*\n*]*\*/', code)
    for iter in listiter:
        dellist.append(code[iter.span()[0]:iter.span()[1]])
    for item in dellist:
        code = code.replace(item, '')

    dellist = []
    listiter = re.finditer(r'\'[^\']*\'', code)
    for iter in listiter:
        dellist.append(code[iter.span()[0]:iter.span()[1]])
    for item in dellist:
        code = code.replace(item, '')

    dellist = []
    listiter = re.finditer(r'\"[^\"]*\"', code)
    for iter in listiter:
        dellist.append(code[iter.span()[0]:iter.span()[1]])
    for item in dellist:
        code = code.replace(item, '')

    dellist = []
    listiter = re.finditer(r'//[^\n]*\n', code)
    for iter in listiter:
        dellist.append(code[iter.span()[0]:iter.span()[1]])
    for item in dellist:
        code = code.replace(item, '')

    return code


def searchFunctions(code):
    functionslist = []
    listiter = re.finditer(r'\s*function[\s*\n*]*[a-zA-Z_0-9]+\s*\([^\)]*\)[\s*\n*]*\{', code)
    for iter in listiter:
        left = 1
        right = 0
        index = iter.span()[1]
        while left != right:
            if code[index] == '{':
                left += 1
            elif code[index] == '}':
                right += 1
            index += 1
        functionslist.append(code[iter.span()[0]:index])

    for item in functionslist:
        code = code.replace(item, '')

    return functionslist, code


def countVars(code):
    returnvarslist = []
    varlist = re.findall(r'var[^;]*;',code)
    dellist = []
    for item in varlist:
        item = item[4:]
        dellist = re.findall(r'=[^\,\;]*', item)
        for iter in dellist:
            item = item.replace(iter, '')
        returnvarslist += re.findall(r'[[a-zA-Z_]+[0-9]*]*(?=\s*,*=*\s*;*)', item)
    return returnvarslist


def getLocalVarsList(globalvarsdictionary, function):
    global resultfile
    parametrs = function[function.find('(')+1:function.find(')')]
    localvarslist = countVars(function)
    localvarslist += re.findall(r'[[a-zA-Z_]+[0-9]*]*(?=\s*,*=*\s*;*)', parametrs)
    functionname = function[:function.find('(')]
    varsdictionary = {}
    global spen
    for var in localvarslist:
        varsdictionary[var] = len(re.findall(r'[^a-z0-9A-Z_]{1}%s[^0-9a-zA-Z_]{1}' % var, function)) - 1
        spen += varsdictionary[var]
    for var in globalvarsdictionary:
        if var not in localvarslist:
            globalvarsdictionary[var] += len(re.findall(r'[^a-z0-9A-Z_]{1}%s[^0-9a-zA-Z_]{1}' % var, function))
    print(functionname)
    print(varsdictionary)
    resultfile.writelines(str(functionname)+'\n')
    resultfile.writelines(str(varsdictionary)+'\n')

def main():
    global resultfile
    sourcefile = open('source.js', 'r')
    code = sourcefile.read()
    code = delComments(code)
    functionslist, code = searchFunctions(code)
    globalvarslist = countVars(code)
    globalvarsdictionary = {}
    global spen
    for var in globalvarslist:
        globalvarsdictionary[var] = len(re.findall(r'[^a-z0-9A-Z_]{1}%s[^0-9a-zA-Z_]{1}' % var, code)) - 1
    for function in functionslist:
        getLocalVarsList(globalvarsdictionary, function)
    for var in globalvarsdictionary:
        spen += globalvarsdictionary[var]
    resultfile.writelines('\nГлобальные переменные'+'\n')
    print('\nГлобальные переменные')
    resultfile.writelines(str(globalvarsdictionary)+'\n')
    print(globalvarsdictionary)
    print('\nРезультирующий спен: ', spen)
    resultfile.writelines('\nРезультирующий спен: '+str(spen)+'\n')
spen = 0

resultfile = open('result.txt','w')

main()
