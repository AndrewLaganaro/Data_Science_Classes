from pandas import DataFrame as df
import pandas as pd
from os import chdir, makedirs
from os.path import join, dirname, realpath, basename, exists
import json
#TODO remove definitely "folders" and use dirgroup. make last reviews. mostly everything is done here.
#TODO make tests with each function

class File():
    def __init__(self, configdir = None):
        #TODO Change configdir to configfile
        #FIXIT test
        #NOTE lalalal
        #BUG test 2
        #ADDHERE function to add a new folder to the config file
        #Change to the directory where this script is located
        chdir(join(dirname(realpath('__file__')))) #todo won't be necessary anymore
        self.currentdir = dirname(realpath('__file__'))  
        print(self.currentdir)
        self.request = None
        self._internalrequest = None
        self.content = None
        self.file = None
        self.specs  =   {
                        'Mode' : None,
                        'Output' : None
                        }
        if configdir:
            self.configdir = configdir
        else:
            self.configdir = '..\\..\\Env\\Config.json'
        self._internal = False

    def Help(self):
        '''This function shows the available folders on the project context'''
        Folders = self.__ConfigEdit(gethelp = True)
        folderlist = [] 
        fileslist = []
        configdict = {}
        for group in Folders:
            folderlist.append(group)
            fileslist.append(list(Folders[group].keys()))
            configdict.update(zip(folderlist, fileslist))

        folderdf = df.transpose(df.from_dict(configdict, orient = 'index'))
        #folderdf = folderdf.T
        folderdf = folderdf[sorted(folderdf.columns)]
        folderdf.replace(to_replace = [None], value ='---', inplace = True)
        display(folderdf)
        
    def __ConfigEdit(self, saveopen = False, edit = False, add = False, delete = False, save = False, 
                    getdir = False, gethelp = False, dirgroup = 'Folders', newconfig = None):
        '''This function loads the config file
        will return Folders dirgroup if not stated otherwise'''
        
        self.specs['Mode'] = 'r'
        self.specs['Output'] = None
        
        internalrequest  =  {
                            'File_name': basename(self.configdir),
                            'Path': join(self.currentdir, self.configdir)
                            }
        #Send an internal request to the Open function to open the config file
        #It will deactivate the internal request right after the file is sent
        self._internal = True
        Config = self.Open(internalrequest, format_ = 'dictionary')
        
        if (add or delete or edit or saveopen or gethelp) == True:
            return Config
        elif save:
            self._internal = True
            Config = self.Save(internalrequest, newconfig)
        elif getdir:
            Config = Config[dirgroup] #"folders"
            return Config
        
    def __Validation(self, request, saveopen = False, edit = False, add = False, delete = False, 
                    getdir = False, gethelp = False):
        '''This function validates the file name and extension to the whole class'''
        
        def ispath(element):
            pathsymbols = ['\\', '/']
            path_exists = any(item in element for item in pathsymbols)
            return path_exists
        
        if isinstance(request, dict):
            validate = list(request.items())
            
            if len(request) == 1:
                firstkey, firstvalue = validate[0][0], validate[0][1]
                firstelem, secondelem = ispath(firstkey), ispath(firstvalue)
            elif len(request) == 2:
                firstkey, firstvalue = validate[0][0], validate[0][1]
                secondkey, secondvalue = validate[1][0], validate[1][1]
                
                firstelem, secondelem = ispath(firstkey), ispath(firstvalue)
                thirdelem, fourthelem = ispath(secondkey), ispath(secondvalue)
        elif isinstance(request, str):
            firstelem = ispath(request)
            
        if add:
            assert len(request) == 1,'Too many keys, must be 1'
            # {'folder_name':'folder_path'}
            if firstelem == False and secondelem == True:
                newfolder = firstkey
                newpath = firstvalue
            # {'folder_path':'folder_name'}
            elif firstelem == True and secondelem == False:
                newfolder = firstvalue
                newpath = firstkey
            else:
                raise Exception('Please provide a folder name and a path in a dictionary')
            #change to list
            return {newfolder : newpath}
            
        elif delete:
            assert isinstance(request, str), 'Please provide a folder name in text'
            if firstelem == False:
                return request
            else:
                raise Exception('Please provide a folder name, not a path')
        elif edit:
            assert len(request) == 1,'Too many keys, must be 1'
            if edit == 'name':
                # {'old_folder_name':'new_folder_name'}
                if firstelem == False and secondelem == False:
                    oldfolder = firstkey
                    newfolder = firstvalue
                return {oldfolder : newfolder}
            elif edit == 'path':
                # {'current_folder_name':'new_folder_path'}
                if firstelem == False and secondelem == True:
                    foldername = firstkey
                    folderpath = firstvalue
                # {'folder_path':'folder_name'}
                elif firstelem == True and secondelem == False:
                    foldername = firstvalue
                    folderpath = firstkey
                else:
                    raise Exception('Please provide a folder name and a path in a dictionary')
                return {foldername, folderpath}
        elif saveopen:
            assert len(request) == 2,'Too many keys, must be 2'
            # {'folder_name':'name', 'folder_path':'path'}
            if firstelem == False and secondelem == False:
                if thirdelem == False and fourthelem == True:
                    filename = firstvalue
                    filefolder = secondvalue
            # {'folder_path':'path', 'folder_name':'name'}
            elif firstelem == False and secondelem == True:
                if thirdelem == False and fourthelem == False:
                    filename = secondvalue
                    filefolder = firstvalue
            else:
                raise Exception('Please provide a folder name and a path in a dictionary')
            extension = '.' + filename.split('.')[-1]
            internalrequest =   {
                                'File_name' : filename,
                                'Path' : filefolder
                                }
            return internalrequest, extension
        
        elif getdir: # folder -> string to get, being the name of the folder; to retrieve the path from
            assert isinstance(request, str), 'Please provide a folder name in text'
            if firstelem == False:
                return request
            else:
                raise Exception('Please provide a folder name, not a path')
        elif gethelp:
            assert isinstance(request, str), 'Please provide a folder group in text'
            if firstelem == False:
                return request
            else:
                raise Exception('Please provide a folder group name, not a path')
            
        else:
            raise Exception('Please provide a valid request')
        
    def AddDir(self, createfolder, dirgroup = None):
        '''This function adds a directory to the config file'''
        
        self.specs['Mode'] = 'r+'
        self.specs['Output'] = None
        verified = 0
        switchkey = False
        
        Config = self.__ConfigEdit(dirgroup, add = True)
        newfolder = self.__Validation(createfolder, add = True)
        newfoldername = list(newfolder.keys())[0].lower().strip()
        
        for key in Config['Folders']:
            verified += 1
            if newfoldername == key.lower().strip():
                switchkey = True
                if verified == len(Config['Folders']) and switchkey == True: 
                    raise Exception('Folder name already exists in the config file')
                
            elif verified == len (Config['Folders']) and switchkey == False:
                Config['Folders'].update(newfolder)
                self.__ConfigEdit(save = True, newconfig = Config)
                break
            
    def DelDir(self, delfolder, dirgroup = None):
        '''This function removes a directory from the config file'''
        # Modify Config['Folders'] to include dirgroups
        
        self.specs['Mode'] = 'r+'
        self.specs['Output'] = None
        verified = 0
        
        Config = self.__ConfigEdit(dirgroup, delete = True)
        removefolder = self.__Validation(delfolder, delete = True).lower().strip()
        
        for key in Config['Folders']:
            if removefolder == key.lower().strip():
                del Config['Folders'][key]
                self.__ConfigEdit(save = True, newconfig = Config)
                break
            elif verified == len(Config['Folders']): 
                raise Exception('Folder name not found in the config file')
            verified += 1 
            
    def EditDir(self, editdir, edit = None, dirgroup = None): 
        '''This function edits a directory in the config file'''
        # Modify Config['Folders'] to include dirgroups
        
        self.specs['Mode'] = 'r+'
        self.specs['Output'] = None
        verified = 0
        
        Config = self.__ConfigEdit(dirgroup, edit = True)
        
        editfolder = self.__Validation(editdir, edit)
        searchkey = list(editfolder.keys())[0].lower().strip()
        newvalue = list(editfolder.values())[0].lower().strip()
        
        for currentkey in Config['Folders']:
            if edit == 'name':
                if searchkey == currentkey.lower().strip():
                    Config['Folders'][newvalue] = Config['Folders'][currentkey]
                    del Config['Folders'][currentkey]
                    break
                elif verified == len(Config['Folders']): 
                    raise Exception('Folder name not found in the config file')
                verified += 1
            elif edit == 'folder':
                if searchkey == currentkey.lower().strip():
                    Config['Folders'][currentkey] = newvalue
                    break
                elif verified == len(Config['Folders']): 
                    raise Exception('Folder name not found in the config file')
                verified += 1
            else:
                raise Exception('Edit type must be either "name" or "path"')
            
        self.__ConfigEdit(save = True, newconfig = Config)
        
    def Folder(self, folder = None, dirgroup = None):
        '''This function pulls the folder path of a .json file'''
        
        self.specs['Mode'] = 'r'        
        self.specs['Output'] = None
        verified = 0
        request = self.__Validation(folder, getdir = True)
        folders = self.__ConfigEdit(dirgroup, getdir = True)
        request = request.lower().strip()
        
        for key in folders.keys(): #throw lower().strip() in here, test if it works 
            if request == key.lower().strip():
                request = key
                folderpath = join(dirname(realpath('__file__')), folders[str(request)])
                break
            elif verified == len(folders): 
                raise Exception('Folder name not according to the config file'+
                                '\n'+'Please refer to the Help() function for more information')
            verified += 1
                
        return folderpath
    
    def Save(self, request, content):
        '''This function saves the content to a file, checks the file format and extension
        and checks if the content is a dataframe or a dictionary'''
        
        self.content = content
        self.specs['Mode'] = 'w'
        self.specs['Output'] = 'save'
        self._internalrequest, extension = self.__Validation(request, saveopen = True)
        
        with File.Handler(**self.specs, **self._internalrequest) as self.file:
            
            if self._internal == True:
                self._internal = False
                self.file.truncate(0)  
                self.file.seek(0)
                json.dump(self.content, self.file, indent = 4, sort_keys = True)
                #This verification could be done with forXexec but the gain in lines would not hold up this time
                
            elif self._internal == False:
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
                    print('HERE:' + extension)
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
                
    def Open(self, request, format_ = 'dataframe'):
        '''This function loads the content from a file and 
        checks if the loading file format is a dataframe or a dictionary'''
        
        self.specs['Mode'] = 'r'
        
        if self._internal == True:
            self.specs['Output'] = None
            self._internal = False
        else:
            self.specs['Output'] = 'load'
        
        self._internalrequest, extension = self.__Validation(request, saveopen = True)
        
        with File.Handler(**self.specs, **self._internalrequest) as file:
            
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