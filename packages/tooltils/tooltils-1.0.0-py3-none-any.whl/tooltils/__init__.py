# Copyright(c) 2023 ebots
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""# tooltils | v1.0.0
A lightweight python utility library built on standard modules
"""

class baseMD:
    from os import removedirs, rename, remove, system
    from urllib.request import urlopen
    from urllib.error import URLError
    from os.path import exists
    from shutil import rmtree
    from json import dumps
    import time as ctime


class errors:
    class ConnectionError(Exception):
        """Unable to connect to server"""
        def __init__(self, message=None, *args):
            self.message = message

        def __str__(self):
            if self.message:
                return self.message
            return 'Unable to connect'

    class ParsingError(Exception):
        """Unable to parse given data"""
        def __init__(self, message=None, *args):
            self.message = message

        def __str__(self):
            if self.message:
                return self.message
            return 'Unable to parse'

    class CompileError(Exception):
        """Unable to compile data"""
        def __init__(self, message=None, *args):
            self.message = message

        def __str__(self):
            if self.message:
                return self.message
            return 'Unable to compile'



class requests:
    """URL post and get methods"""
    def get(self, url:str, params: dict={}):
        """Call a URL and return JSON data"""
        try:
            if params != {}:
                if url[-1] == '?':
                    http = url
                else:
                    http = f'{url}?'
                for i in range(len(params)):
                    key = eval(str(params.keys())[10:-1])[i]
                    item = key + '=' + params[key]
                    if key + '=' in http:
                        continue
                    http += item + '&'
                data = baseMD.urlopen(http[0:-1])
            else:
                data = baseMD.urlopen(url)
        except baseMD.URLError:
            raise errors.ConnectionError('Nodename nor servername provided')

        try:
            parsed_json = eval((str(data.read()).replace('true', 'True').replace('false', 'False'))[2:-1])
        except:
            raise errors.ParsingError('Unable to parse JSON data from given url({0})'.format(url))

        class response:
            code = data.getcode()
            json = parsed_json
            pretty = baseMD.dumps(json, indent=4)
            text = data.read()
        return response

class json:
    """General JSON file interactions"""
    def load(file: str) -> str:
        """Load data from a JSON file as a dictionary"""
        inc = 0
        appljson = []
        with open(str(file)[25:-28].replace('\'', ''), 'r') as rfile:
            tempdata = rfile.readlines()
        tempdata.pop(0)
        tempdata.pop(-1)
        for i in tempdata:
            for x in i:
                if x != ' ':
                    break
                inc += 1
            reduc = 3
            if i == tempdata[-1]:
                reduc = 2
            evalstr = ('{' + i[inc + 1:-reduc].replace('\'', '') + '}').replace('true', 'True').replace('false', 'False')
            appljson.append(eval(evalstr))
            inc = 0
        return appljson

    def set(file: str, setting: str, value: str) -> None:
        """Set a value in a JSON file"""
        jdata = load(file)
        names = []
        inc = 0
        appljson = ['[\n']

        for i in jdata:
            names.append(str(i.keys())[12:-3])

        for i in names:
            if i == setting:
                eof = ''
                if type(value) is str:
                    value = f'"{value}"'
                elif type(value) is bool:
                    value = str(value).lower()
                tempjson = '    {"' + setting + '": ' + value + '}'
                if i == names[-1]:
                    eof = '\n]'
                else:
                    eof = ',\n'
                appljson.append(f'{tempjson}{eof}')
            else:
                tempvalue = jdata[inc][f'{names[inc]}']
                if type(tempvalue) is str:
                    tempvalue = f'"{tempvalue}"'
                elif type(tempvalue) is bool:
                    tempvalue = str(tempvalue).lower()
                eof = ''
                tempjson = '    {"' + names[inc] + '": ' + tempvalue + '}'
                if i == names[-1]:
                    eof = '\n]'
                else:
                    eof = ',\n'
                appljson.append(f'{tempjson}{eof}')
            inc += 1

        with open(str(file)[25:-28].replace('\'', ''), 'r+') as writefile:
            writefile.truncate(0)
            for i in appljson:
                writefile.write(i)

    def dump(file: str, data: dict) -> None:
        """Dump JSON data into a file"""
        filename = str(file)[25:-28].replace('\'', '')
        with open(filename, 'r') as wfile:
            wdata = wfile.readlines()
        wdata.pop(-1)
        wdata[-1] = wdata[-1][0:-1] + ','
        for i in data:
            elem = str(i).replace('\'', '"').replace(
                'False', 'false').replace('True', 'true')
            wdata.append(f'\n    {elem},')
        wdata[-1] = wdata[-1][0:-1] + '\n'
        wdata.append(']')
        with open(filename, 'r+') as wfile:
            wfile.writelines(wdata)

    def decode(data: dict) -> list:
        """Convert dictionary data(JSON data) to a list in value pairs"""
        templist = []
        for i in data:
            tempvalue = data.get(i)
            templist.append([i, tempvalue])
        return templist

    def encode(data: list) -> dict:
        """Convert list data to a dictionary(JSON data)"""
        tempdict = {}
        for i in data:
            tempdict.update({i[0]: i[1]})
        return tempdict

class time:
    """Functions relating to the system time and hardware"""
    def epoch() -> float:
        """Return epoch based off system clock (If applicable)"""
        return baseMD.ctime.time()

    def getdate(format: int=0, timestamp: float=baseMD.ctime.time()) -> str:
        """Convert time.time() -> readable date"""

        date = baseMD.ctime.localtime(timestamp)
        month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                 'August', 'September', 'October', 'November', 'December'][date.tm_mon - 1]
        day_end = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th',
                   'th'][int(str(date.tm_mday)[-1])] if str(date.tm_mday) not in ['11', '12', '13'] else 'th'
        hour = date.tm_hour % 12 if date.tm_hour % 12 != 0 else 12
        min = str(date.tm_min) if len(str(date.tm_min)) != 1 else f'0{date.tm_min}'
        sec = str(date.tm_sec + 1) if len(str(date.tm_sec + 1)
                                        ) != 1 else f'0{date.tm_sec + 1}'
        formats = ['{0}-{1}-{2} {3}:{4}:{5}'.format(date.tm_year, date.tm_mon if len(str(date.tm_mon)) != 1 else f'0{date.tm_mon}',
                                                    date.tm_mday, date.tm_hour if len(str(date.tm_hour)) != 1 else f'0{date.tm_hour}', min, sec),
                   '{0}:{1} {2} on the {3}{4} of {5}, {6}'.format(hour, min, 'PM' if date.tm_hour >= 12 else 'AM',
                                                                  date.tm_mday, day_end, month, date.tm_year)]
        return formats[format]

    def sleep(ms: float) -> None:
        """Delay execution for x amount of milliseconds"""
        baseMD.ctime.sleep(ms / 1000)

class logging:
    """General logging functions and ANSI escape sequence colour codes"""
    colours = ['pink', 'green', 'blue', 'yellow',
               'red', 'white', 'cyan', 'gray', '']
    cvalues = ['35', '32', '34', '33',
              '31', '38', '36', '30', '0']

    def ctext(text: str='', colour: str='', bold: bool=False) -> str:
        """Returns text in specified colour"""
        try:
            cvalue = logging.cvalues[logging.colours.index(colour)]
        except ValueError:
            cvalue = colour

        baseMD.system('')
        return '\u001b[{0}{1}{2}\u001b[0m'.format(cvalue, ';1m' if bold else 'm', text)

    def log(type: int, header: str, details: str) -> None:
        """Log text to the terminal as an info, warning or error type"""
        try:
            data = [[logging.ctext('INFO', 'blue', True), '     '],
                    [logging.ctext('WARNING', 'yellow', True), '  '],
                    [logging.ctext('ERROR', 'red', True), '    ']][type - 1]
        except IndexError:
            raise IndexError('Unknown type ({0})'.format(type))

        baseMD.system('')
        print('{0} {1}{2}{3} {4}'.format(logging.ctext(time.getdate(), 'gray', True), data[0], data[1],
                                         logging.ctext(header, 'pink'), details))

class miniCompiler():
    """MiniCompiler creator class"""
    def __init__(self, file, runFile: bool=True, name: str='@_compiled', suffix: bool=True):
        self.suffix = suffix
        self.file = file
        self.runFile = runFile
        self.name = name.replace('@', ''.join((file.split('.')[0:-1])))
        if not baseMD.exists(self.file):
            return None
        elif self.file.split('.')[-1] == 'py':
            self.type = 'py'
        elif self.file.split('.')[-1] == 'cpp':
            self.type = 'c++'
        else:
            self.type = 'c'

    def __repr__(self):
        return f'<Compiler object [{self.file}]>'

    def main(self) -> str:
        """Execute all functions at once"""
        self.compile()
        if self.runFile:
            self.execute()
            self.end()
        return f'<Compiler object [{self.file}]>'

    def compile(self) -> str:
        """Compile the file"""
        if self.type[0] == 'c':
            cname = 'gcc' if self.type == 'c' else 'g++'
            error = baseMD.system(cname + f' {self.file} -o {self.name}')
            if error != 0:
                raise errors.CompileError('Failed to compile c file')
        else:
            cname = 'python3' if self.suffix else 'python'
            cmd = f'{cname} -m PyInstaller {self.file} -F'
            error = baseMD.system(cmd)
            if error != 0:
                raise errors.CompileError('Failed to compile python file')
            baseMD.remove(self.name.split('_')[0] + '.spec')
            baseMD.rmtree('build/', ignore_errors=True)
            baseMD.system('mv "dist/' + self.name.split('_')[0] + '" ./')
            baseMD.removedirs('dist/')
            baseMD.rename(self.name.split('_')[0], self.name)
        return f'<Compiler object [{self.file}]>'

    def execute(self) -> str:
        """Execute the compiled file if applicable"""
        baseMD.system(f'./{self.name}')
        return f'<Compiler object [{self.file}]>'

    def end(self) -> str:
        """Delete the compiled file if applicable"""
        try:
            baseMD.remove(self.name)
        except FileNotFoundError:
            raise FileNotFoundError('Compiled file was not found')
        return f'<Compiler object [{self.file}]>'

class interpereter:
    """Custom python interpereter to parse different features"""
    def __init__(self, file: None, name: str = '@_interpereted'):
        self.file = file
        self.name = name.replace('@', ''.join(file.split('.')[0:-1])) + '.py'
        self.interpereted = []
        try:
            with open(self.file, 'r') as rfile:
                self.lines = rfile.readlines()
        except (FileNotFoundError, IsADirectoryError):
            raise FileNotFoundError('Could not locate file')

    def __repr__(self):
        return '<Interpereter object ({0})>'.format(self.file)

    def indent(self, line):
        indent = ''
        for i in range(len(line) - len(line.lstrip())):
            indent += ' '
        return indent

    def condition(self, line):
        declaration = line.split('=')
        try:
            if line.lstrip()[0] != '#' and line.lstrip()[0:2] != '//' and len(declaration) != 1 and len(declaration[1].split('?')) != 1:
                statement = declaration[1].split('?')[0][1:-1]
                values = declaration[1].split('?')[1].split(':')
                return f'{declaration[0][0:-1]} = {values[0][1]} if {statement} else {values[1][1]}\n'
        except IndexError:
            pass

    def comment(self, line):
        if line.lstrip()[0:2] == '//':
            return self.indent(line) + '#' + line.lstrip()[2:-1] + line[-1]

    def interperet(self) -> str:
        """Interperet file specified"""
        for line in self.lines:
            checked = False
            clines = [self.condition(line), self.comment(line)]
            for i in clines:
                if i == None:
                    if checked:
                        self.interpereted.append(line)
                        checked = False
                    else:
                        checked = True
                else:
                    self.interpereted.append(i)

        with open(self.name, 'a+') as wfile:
            wfile.truncate(0)
            wfile.writelines(self.interpereted)

        return '<Interpereter object ({0})>'.format(self.file)
