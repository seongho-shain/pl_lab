#객체가 여러개인 경우 첫 파라미터 빈칸을 추가로 만들어서 조작할 수 있게 해야할 거 같음
#method 선언 객체.xx로 되게 수정

import json

class JsonManager:
    currentFileName = ''
    data = {}
    IDX = 0
    def __init__(self):
        self.data['extensionName'] = ''
        self.data['description'] = 'KODEKOREA'
        self.data['version'] = '1.0'
        self.data['author'] = 'KODEKOREA'
        self.data['homepage'] = 'KODEKOREA'
        self.data['sort'] = 0
        self.data['javascriptURL'] = 'js/sample.js'
        self.data['firmware'] = '1.0'
        self.data['extensionPort'] = 0
        self.data['blockSpecs'] = []
        self.data['menus'] = {}
        self.data['values'] = {}


    def setCurrentFileName(self, name):
        self.currentFileName = name
        self.data['extensionName'] = name

    def setExtensionName(self, name):
        self.data['extensionName'] = name

    def writeInit(self, _type, _filename, _params):
        TYPE = _type #'w'
        self.data['blockSpecs'].append([TYPE])

        NAME = _filename #"FUNC1"

        BLOCKNAME = NAME + '%n'

        # [['int','A'],['float','B'],['char', 'C']]
        PARAMS = _params

        #파라미터 이름이 없는 경우 noName + emptyNameCount로 매김
        emptyNameCount = 0
        for param in PARAMS:
            if 'const' in param:
                param.remove("const")
            if len(param) < 2:
                name = "noName" + str(emptyNameCount)
            else:
                name = param[1]
            emptyNameCount += 1

            if self.isStringParam(param):
                BLOCKNAME += " " + name + ": " + "%s"
            else:
                BLOCKNAME += " " + name + ": " + "%n"

        self.data['blockSpecs'][self.IDX].append(BLOCKNAME)
        self.data['blockSpecs'][self.IDX].append(NAME)

        self.data['blockSpecs'][self.IDX].append("0")
        for param in PARAMS:
            if len(param) > 2:
                if param[2] == "true":
                    self.data['blockSpecs'][self.IDX].append("1")
                elif param[2] == "false":
                    self.data['blockSpecs'][self.IDX].append("0")
                else:
                    self.data['blockSpecs'][self.IDX].append(param[2])
            else:
                self.data['blockSpecs'][self.IDX].append("0")

        ARDUINOCODE = {
            "inc": '',
            "def": '',
            "setup": '',
            "work": '',
            "loop": ''
        }

        FILENAME = _filename #'sample'

        ARDUINOCODE['inc'] = "#include \"" +  FILENAME+'.h' + "\"\n"
        ARDUINOCODE['def'] = FILENAME + " " + NAME + '{0}'

        args = ''
        for cnt in range(len(PARAMS)):
            args += '{' + str(cnt+1) + '}, '

        args = args[:-2]

        ARDUINOCODE['def'] += '(' + args + ')' + ';\n'

        self.data['blockSpecs'][self.IDX].append(ARDUINOCODE)

        self.IDX = self.IDX + 1


    def writeFunc(self, _type, _funcname, _params):
        TYPE = _type #'w'
        self.data['blockSpecs'].append([TYPE])

        NAME = _funcname #"FUNC1"

        BLOCKNAME = self.currentFileName + "%n" + " ." + NAME
        PARAMS = _params #[['int','A'],['float','B'],['char', 'C']]


        print(PARAMS)

        #파라미터 이름이 없는 경우 noName + emptyNameCount로 매김
        emptyNameCount = 0
        for param in PARAMS:
            if 'const' in param:
                param.remove("const")
            if len(param) < 2:
                name = "noName" + str(emptyNameCount)
            else:
                name = param[1]
            emptyNameCount += 1
            #print('param : ', _params)
            if self.isStringParam(param):
                BLOCKNAME += " " + name + ": " + "%s"
            else:
                BLOCKNAME += " " + name + ": " + "%n"

        self.data['blockSpecs'][self.IDX].append(BLOCKNAME)
        self.data['blockSpecs'][self.IDX].append(NAME)

        self.data['blockSpecs'][self.IDX].append("0")
        for param in PARAMS:
            if(len(param) > 2):
                if param[2] == "true":
                    self.data['blockSpecs'][self.IDX].append("1")
                elif param[2] == "false":
                    self.data['blockSpecs'][self.IDX].append("0")
                else:
                    self.data['blockSpecs'][self.IDX].append(param[2])
            else:
                self.data['blockSpecs'][self.IDX].append("0")

        ARDUINOCODE = {
            "inc": '',
            "def": '',
            "setup": '',
            "work": '',
            "loop": ''
        }

        FUNCNAME = _funcname #'sample'

        #ARDUINOCODE['inc'] = FILENAME+'.h'
        ARDUINOCODE['work'] = self.currentFileName+'{0}'+'.'+FUNCNAME

        args = ''
        for cnt in range(len(PARAMS)):
            args += '{' + str(cnt+1) + '}, '

        args = args[:-2]
        if TYPE == 'w':
            ARDUINOCODE['work'] += '(' + args + ')' + ';\n'
        elif TYPE == 'r':
            ARDUINOCODE['work'] += '(' + args + ')'

        self.data['blockSpecs'][self.IDX].append(ARDUINOCODE)

        self.IDX = self.IDX + 1

    def writeDefines(self, defines):
        names = []

        for define in defines:
            names.append(define[0])

        self.data['menus']['#define'] = names

        for define in defines:
            self.data['values'][define[0]] = define[1]

        self.data['blockSpecs'].append(['R'])
        self.data['blockSpecs'][self.IDX].append("%d.#define")
        self.data['blockSpecs'][self.IDX].append("")
        self.data['blockSpecs'][self.IDX].append(defines[0][0])

        ARDUINOCODE = {
            "inc": '',
            "def": '',
            "setup": '',
            "work": '{0}',
            "loop": ''
        }
        self.data['blockSpecs'][self.IDX].append(ARDUINOCODE)

        self.IDX = self.IDX + 1


    def saveJson(self, path):
        with open(path, 'w') as outfile:
            outfile.write(json.dumps(self.data, indent=4, sort_keys=False))

    # %s로 만들 파라미터인지 확인 == string 형태의 파라미터인지 확인
    def isStringParam(self, param):
        print("chk :", param)
        if len(param) < 2:
            name = "noName"
        else:
            name = param[1]

        if '*' in name:
            return True
        elif '*' in param[0]:
            return True
        elif param[0] == 'char[]':
            return True
        elif '[' in name and ']' in name:
            return True
        else:
            return False

    def isBoolParam(self, param):
        return param[0] == "bool"
