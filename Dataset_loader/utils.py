import os
import pandas as pd
class File():
    def __init__(self):
        self.request = None
        self.content = None
        self.file = None
        self.specs  =   {
                        'Mode' : None,
                        'Output' : None
                        }
    
    def __validation(self, request):
        '''This function validates the file name and extension'''
        
        assert len(request) == 2,'Too many arguments, must be 2'
        
        if '\\' or '/' in list(request.items())[0][1] == False:
            extension = '.'+list(request.items())[0][1].split('.')[-1]
        elif '\\' or '/' in list(request.items())[1][1] == False:
            extension = '.'+list(request.items())[1][1].split('.')[-1]
        else:
            raise Exception('File name not found on request')
        
        return extension
    
    def Saveto(self, request, content):
        '''This function saves the content to a file, checks the file format and extension
        and checks if the content is a dataframe or a dictionary'''
        
        self.request = request
        self.content = content
        self.specs['Mode'] = 'w'
        self.specs['Output'] = False
        
        with File.Handler(**self.specs, **self.request) as self.file:
            
            extension = self.__validation(self.request)
            
            if isinstance(self.content, pd.DataFrame):
                if extension == '.csv':
                    self.content.to_csv(self.file, index=False)
                elif extension == '.tsv':
                    self.content.to_csv(self.file, sep='\t', index=False)
                elif extension == '.json':
                    self.content.to_json(self.file)
                elif extension == '.xlsx' or '.xls':
                    self.content.to_excel(self.file, index=False)
                elif extension == 'pkl':
                    self.content.to_pickle(self.file)
                else:
                    raise Exception('File extension not supported')
            elif isinstance(self.content, dict):
                if extension == '.csv':
                    pd.DataFrame(self.content).to_csv(self.file, index=False)
                elif extension == '.tsv':
                    pd.DataFrame(self.content).to_csv(self.file, sep='\t', index=False)
                elif extension == '.json':
                    pd.DataFrame(self.content).to_json(self.file)
                elif extension == '.xlsx' or '.xls':
                    pd.DataFrame(self.content).to_excel(self.file, index=False)
                elif extension == 'pkl':
                    pd.DataFrame(self.content).to_pickle(self.file)
                else:
                    raise Exception('File extension not supported')
            elif isinstance(self.content, str):
                self.file.write(self.content)
            else:
                raise Exception('Content must be a dictionary or pandas dataframe')
            
    def Loadfrom(self, request, format_ = 'dataframe'):
        '''This function loads the content from a file and 
        checks if the loading file format is a dataframe or a dictionary'''
        
        self.request = request        
        self.specs['Mode'] = 'r'        
        self.specs['Output'] = 'variable'
        
        with File.Handler(**self.specs, **self.request) as file:
            
            extension = self.__validation(self.request)
            if format_ == 'dataframe':
                if extension == '.csv':
                    self.file = pd.read_csv(file)
                elif extension == '.tsv':
                    self.file = pd.read_csv(file, sep='\t')
                elif extension == '.json':
                    self.file = pd.read_json(file)
                elif extension == '.xlsx' or '.xls':
                    self.file = pd.read_excel(file)
                elif extension == 'pkl':
                    self.file = pd.read_pickle(file)
                else:
                    raise Exception('File extension must be .csv, .tsv, .json, .xlsx, .xls or .pkl')
            elif format_ == 'dictionary':
                if extension == '.csv':
                    self.file = pd.read_csv(file).to_dict()
                elif extension == '.tsv':
                    self.file = pd.read_csv(file, sep='\t').to_dict()
                elif extension == '.json':
                    self.file = pd.read_json(file).to_dict()
                elif extension == '.xlsx' or '.xls':
                    self.file = pd.read_excel(file).to_dict()
                elif extension == 'pkl':
                    self.file = pd.read_pickle(file).to_dict()
                else:
                    raise Exception('File extension must be .csv, .tsv, .json, .xlsx, .xls or .pkl')
            elif format_ == 'text':
                self.file = file.read().splitlines()
                
            else:
                raise Exception('Format must be dataframe, dictionary or string')
            
        return self.file
            
    class Handler():
        def __init__(self, Mode, Output, File_name, Path):
            #Change to the directory where this script is located
            os.chdir(os.path.join(os.path.dirname(os.path.realpath('__file__'))))
            
            #Check if the path provided contains the name of the file, if yes, remove it
            if File_name in Path:
                Path = Path.replace(File_name,'')
                
            self.mode = Mode
            self.filename = File_name
            self.folder = os.path.basename(Path).title()
            self.path = os.path.join(Path, File_name)
            self.file = None
            self.output = Output
            
        def __enter__(self):
            self.file = open(self.path, self.mode)
            
            return self.file
            
        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.file.close()
            
            if self.output == 'variable' and self.mode == 'r':
                print(f"File(Name: {self.filename}, Folder: {self.folder}) loaded")
            elif self.mode == 'w':
                print(f"File(Name: {self.filename}, Folder: {self.folder}) saved!")