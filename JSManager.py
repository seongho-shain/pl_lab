begin = '(function(ext) {\n\tvar device = null;\n\n\tvar levels = {\n\t\tHIGH:1,\n\t\tLOW:0\n\t};\n\n\text.resetAll = function(){};\n\n\text.runArduino = function(){\n	\n\t};\n\text.digitalWrite = function(pin,level) {\n\t\t\t\tdevice.send([pin, levels[level]])\n\t};\n\tvar _level = 0;\n'
end = '\n\tfunction processData(bytes) {\n\t\ttrace(bytes);\n\t}\n\t// Extension API interactions\n\tvar potentialDevices = [];\n\text._deviceConnected = function(dev) {\n\t\tpotentialDevices.push(dev);\n\n\t\tif (!device) {\n\t\t\ttryNextDevice();\n\t\t}\n\t}\n\n\tfunction tryNextDevice() {\n\t\t// If potentialDevices is empty, device will be undefined.\n\t\t// That will get us back here next time a device is connected.\n\t\tdevice = potentialDevices.shift();\n\t\tif (device) {\n\t\t\tdevice.open({ stopBits: 0, bitRate: 115200, ctsFlowControl: 0 }, deviceOpened);\n\t\t}\n\t}\n\n\tfunction deviceOpened(dev) {\n\t\tif (!dev) {\n\t\t\t// Opening the port failed.\n\t\t\ttryNextDevice();\n\t\t\treturn;\n\t\t}\n\t\tdevice.set_receive_handler(\'demo\',function(data) {\n\t\t\tprocessData(data);\n\t\t});\t};\n\n\text._deviceRemoved = function(dev) {\n\t\tif(device != dev) return;\n\t\t\tdevice = null;    };\n\n\text._shutdown = function() {\n\t\tif(device) device.close();\n\t\tdevice = null;\n\t};\n\n\text._getStatus = function() {\n\t\tif(!device) return {status: 1, msg: \'LCD1602 disconnected\'};\n\t\treturn {status: 2, msg: \'LCD1602 connected\'};\n\t}\n\n\tvar descriptor = {};\n\tScratchExtensions.register(\'LCD1602\', descriptor, ext, {type: \'serial\'});\n})({});'

class JSManager:
    functions = []
    def saveJS(self, path):
        with open(path, 'w') as outfile:
            outfile.write(begin)
            for function in self.functions:
               outfile.write(function)
            outfile.write(end)

    def addFunction(self, name, params):
        functionCode = '\text.' + name + ' = function('

        #파라미터 이름이 없는 경우 noName + emptyNameCount로 매김
        emptyNameCount = 0
        for param in params:
            print("param!! : ",param)
            if 'const' in param:
                param.remove("const")
            if len(param) < 2:
                name = "noName" + str(emptyNameCount)
            else:
                name = param[1]

            # 포인터 삭제, js파일에 변수명에 그대로 들어가면 문제가 됨
            name = name.replace("*", "")

            functionCode += name + ','
            emptyNameCount += 1

        if len(params) > 0:
            functionCode = functionCode[:-1]

        functionCode += ') {\n'

        if len(params) > 0:
            functionCode += '\t\tdevice.send(['

        emptyNameCount = 0
        for param in params:
            if 'const' in param:
                param.remove("const")
            if len(param) < 2:
                name = "noName" + str(emptyNameCount)
            else:
                name = param[1]

            # 포인터 삭제, js파일에 변수명에 그대로 들어가면 문제가 됨
            name = name.replace("*", "")

            functionCode += name + ','
            emptyNameCount += 1

        if len(params) > 0:
            functionCode = functionCode[:-1]
            functionCode += ']);\n'

        functionCode += '\t};\n'

        self.functions.append(functionCode)


# jsManager = JSManager()
# jsManager.saveJS("C:\sample.js")