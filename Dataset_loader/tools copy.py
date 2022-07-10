from textwrap import indent
import pandas as pd
from os import chdir, makedirs
from os.path import join, dirname, realpath, basename, exists
import json

class File():
    def __init__(self):
        
        #Change to the directory where this script is located
        chdir(join(dirname(realpath('__file__'))))
        self.currentdir = dirname(realpath('__file__'))  
        self.request = None
        self.content = None
        self.file = None
        self.specs  =   {
                        'Mode' : None,
                        'Output' : None
                        }
        self.configfile = '..\\..\\Env\\Config.json' 
        self._help = False
        self.edit = False
        
    def Help(self):
        '''This function shows the available folders on the project context'''
        self._help = True
        Folders = self.Folder()
        folderlist = [] 
        
        for folder in Folders.keys():
            folderlist.append(folder)
        folderdf = pd.DataFrame({'Folders in this project': folderlist})
        display(folderdf)
        self._help = False
    
    def __ConfigEdit(self, dirgroup = None, edit = False, save = False, newconfig = None):
        '''This function loads the config file'''
        
        self.specs['Mode'] = 'r'
        self.specs['Output'] = None
        
        internalrequest =   {
                            'File_name': basename(self.configfile),
                            'Path': join(dirname(realpath('__file__')), self.configfile)
                            }
        # saveto = self.__Validation(internalrequest, internal=True)
        Config = self.Loadfrom(internalrequest, format_ = 'dictionary', internal= True)
        
        if edit == True:
            return Config
        elif save == True:
            self.edit = True 
            Config = self.Saveto(internalrequest, newconfig)  
        else: 
            Config = Config['Folders']
            return Config
    
    def __Validation(self, request, edit = False, remove = False, internal = False):
        '''This function validates the file name and extension'''
        if remove == True:
            
            assert isinstance(request, str), 'Please provide a folder name in text'  
            
            return request
        
        else:
            if edit == False:
                assert len(request) == 2,'Too many arguments, must be 2'
            if edit == True:
                assert len(request) == 1,'Too many arguments, must be 1'
                
            if '\\' or '/' in list(request.items())[0][1] == False:
                
                if edit == True:
                    folderpath = list(request.items())[0][1]
                    foldername = list(request.items())[0][0]
                else:
                    filename = list(request.items())[0][1]
                    extension = '.'+list(request.items())[0][1].split('.')[-1]
                    
            elif '\\' or '/' in list(request.items())[1][1] == False:                
                
                if edit == True:
                    folderpath = list(request.items())[1][1]
                    foldername = list(request.items())[1][0]
                else:
                    filename = list(request.items())[1][1]
                    extension = '.'+list(request.items())[1][1].split('.')[-1]
            else:
                if edit == True:
                    raise Exception('Folder name or Path not found on request')
                else:
                    raise Exception('File name or Path not found on request')
            
            if edit == True:
                return {foldername : folderpath}
            #elif internal == True:
            #    return filename, path
            elif edit == False and internal == False:
                return extension 
            #fazer retornar o request inteiro para o Loadfrom usar
            
    def AddDirectory(self, createfolder, dirgroup = None):
        '''This function adds a directory to the config file'''
        
        self.specs['Mode'] = 'r+'
        self.specs['Output'] = None
        verified = 0
        switchkey = False
        
        Config = self.__ConfigEdit(dirgroup, edit = True)
        newfolder = self.__Validation(createfolder, edit = True)   
        
        for key in Config['Folders']:
            verified += 1
            if list(newfolder.keys())[0].lower().strip() == key.lower().strip():
                switchkey = True
                if verified == len(Config['Folders']) and switchkey == True: 
                    raise Exception('Folder name already exists in the config file')
                
            elif verified == len (Config['Folders']) and switchkey == False:
                Config['Folders'].update(newfolder)
                self.__ConfigEdit(save = True, newconfig = Config)
                break
            
    def RemoveDirectory(self, delfolder, dirgroup = None):
        '''This function removes a directory from the config file'''
        
        self.specs['Mode'] = 'r+'
        self.specs['Output'] = None
        verified = 0
        Config = self.__ConfigEdit(dirgroup, edit = True)
        removefolder = self.__Validation(delfolder, edit=True, remove = True)
        
        for key in Config['Folders']:
            if removefolder.lower().strip() == key.lower().strip():
                del Config['Folders'][key]
                break
            elif verified == len(Config['Folders']): 
                raise Exception('Folder name not found in the config file')
            verified += 1 
            self.__ConfigEdit(save = True, newconfig = Config)
            
    def EditDirectory(self, editfolder, dirgroup = None, kind = None): 
        '''This function edits a directory in the config file'''
        
        #TODO - Modify Config['Folders'] to include dirgroups instead of just folders, 
        # allowing for multiple folder groups to be edited and used
        
        self.specs['Mode'] = 'r+'
        self.specs['Output'] = None
        verified = 0
        Config = self.__ConfigEdit(dirgroup, edit = True)
        
        editfolder = self.__Validation(editfolder, edit = True)
        
        searchkey = list(editfolder.keys())[0].lower().strip()
        newvalue = list(editfolder.values())[0].lower().strip()
        
        for currentkey in Config['Folders']:
            if kind == 'name':
                if searchkey == currentkey.lower().strip():
                    
                    Config['Folders'][newvalue] = Config['Folders'][currentkey]
                    del Config['Folders'][currentkey]
                    break
                elif verified == len(Config['Folders']): 
                    raise Exception('Folder name not found in the config file')
                verified += 1
                
            elif kind == 'folder':
                if searchkey == currentkey.lower().strip():
                    Config['Folders'][currentkey] = newvalue
                    break
                elif verified == len(Config['Folders']): 
                    raise Exception('Folder name not found in the config file')
                verified += 1
                
            else:
                raise Exception('Kind must be either "name" or "path"')
            
        self.__ConfigEdit(save = True, newconfig = Config)
        
    def Folder(self, folder = None, dirgroup = None):
        '''This function pulls the folder path from a .json file 
        using the OS module and also the folder names in order for it to be used as a string
        during other function calls. The main goal of this function is to make the main usage
        of this class as easy as possiblewithout needing to type each and every folder path every time'''
        
        self.specs['Mode'] = 'r'        
        self.specs['Output'] = None
        verified = 0
        
        Folders = self.__ConfigEdit(dirgroup)
        
        if self._help == True:
            return Folders
        else:
            request = folder.lower()
            
            for key in Folders.keys():
                if request.lower().strip() == key.lower().strip():
                    request = key
                    folderpath = join(dirname(realpath('__file__')), Folders[str(request)])
                    break
                elif verified == len(Folders): 
                    raise Exception('Folder name not accoridng to the config file'+
                                    '\n'+'Please refer to the Help() function for more information')
                verified += 1
                    
            return folderpath
    
    def Saveto(self, request, content):
        '''This function saves the content to a file, checks the file format and extension
        and checks if the content is a dataframe or a dictionary'''
        
        self.request = request
        self.content = content
        self.specs['Mode'] = 'w'
        self.specs['Output'] = 'save'
        # self.request = self.__Validation(self.request)
        with File.Handler(**self.specs, **self.request) as self.file:
            
            extension = self.__Validation(self.request)
            if self.edit == True:
                
                self.file.truncate(0)  
                self.file.seek(0)
                json.dump(self.content, self.file, indent = 4, sort_keys = True)
                
            elif self.edit == False:
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
                    
                elif isinstance(self.content, dict) and self.edit == False:
                    if extension == '.csv':
                        pd.DataFrame(self.content).to_csv(self.file, index=False)
                    elif extension == '.tsv':
                        pd.DataFrame(self.content).to_csv(self.file, sep='\t', index=False)
                    elif extension == '.json':
                        pd.DataFrame(self.content).to_json(self.file, indent = 4)
                    elif extension == '.xlsx' or '.xls':
                        pd.DataFrame(self.content).to_excel(self.file, index=False)
                    elif extension == 'pkl':
                        pd.DataFrame(self.content).to_pickle(self.file)
                    else:
                        raise Exception('File extension not supported')
                else:
                    raise Exception('Content must be a dictionary or pandas dataframe')
            self.edit = False
            
    def Loadfrom(self, request, format_ = 'dataframe', internal = False):
        '''This function loads the content from a file and 
        checks if the loading file format is a dataframe or a dictionary'''
        #TODO - covert internal to attribute
        self.request = request        
        self.specs['Mode'] = 'r'
        if internal == True:
            self.specs['Output'] = None
        else:
            self.specs['Output'] = 'load'        
            
        with File.Handler(**self.specs, **self.request) as file:
            
            extension = self.__Validation(self.request)
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
                    self.file = json.load(file)
                elif extension == '.xlsx' or '.xls':
                    self.file = pd.read_excel(file).to_dict()
                elif extension == 'pkl':
                    self.file = pd.read_pickle(file).to_dict()
                else:
                    raise Exception('File extension must be .csv, .tsv, .json, .xlsx, .xls or .pkl')
            else:
                raise Exception('Format must be dataframe or dictionary')
            
        return self.file
    class Handler():
        def __init__(self, Mode, Output, File_name, Path):
            #TODO - Enable the __Validation function to check File_name and Path independently of their names
            #outside of a dictionary
            
            #Check if the path provided contains the name of the file, if yes, remove it
            if File_name in Path:
                Path = Path.replace(File_name,'')
                
            self.mode = Mode
            self.filename = File_name
            self.folder = basename(Path).title()
            self.path = join(Path, File_name)
            self.file = None
            self.output = Output
            
        def __enter__(self):
            
            self.file = open(self.path, self.mode)
            
            return self.file
            
        def __exit__(self, exc_type, exc_value, exc_traceback):
            self.file.close()
            
            if self.output == 'load' and self.mode == 'r':
                print(f"File(Name: {self.filename}, Folder: {self.folder}) loaded")
            elif self.output == 'save' and self.mode == 'w':
                print(f"File(Name: {self.filename}, Folder: {self.folder}) saved!") 