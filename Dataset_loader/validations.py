def __Validation(self, request, add = False, delete = False, edit = None, getdir = False , saveopen = False):
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
                
        if add: # add -> dict to add (1 key 1 value)
            assert len(request) == 1,'Too many keys, must be 1'
            # add request format is: {'folder_name':'folder_path'}
            if firstelem == False and secondelem == True:
                newfolder = firstkey
                newpath = firstvalue
            # if inverted, {'folder_path':'folder_name'}
            elif firstelem == True and secondelem == False:
                newfolder = firstvalue
                newpath = firstkey
            # if request is wrong formated
            else:
                raise Exception('Please provide a folder name and a path in a dictionary')
            #change to list
            return {newfolder : newpath}
            
        elif delete: # delete -> string to remove
            assert isinstance(request, str), 'Please provide a folder name in text'
            if firstelem == False:
                return request
            else:
                raise Exception('Please provide a folder name, not a path')
        elif edit:  # edit -> 2 options: either by name or by path
            assert len(request) == 1,'Too many keys, must be 1'
            if edit == 'name':# edit -> by name: dict to edit (1 key 1 value, previous name new name)
                # edit request name format is: {'old_folder_name':'new_folder_name'}
                
                if firstelem == False and secondelem == False:
                    oldfolder = firstkey
                    newfolder = firstvalue
                    
                return {oldfolder : newfolder}
                
            elif edit == 'path':# edit -> by path: dict to edit (1 key 1 value, current name new path)
                # edit request path format is: {'current_folder_name':'new_folder_path'}
                
                if firstelem == False and secondelem == True:
                    foldername = firstkey
                    folderpath = firstvalue
                # if inverted, {'folder_path':'folder_name'}
                elif firstelem == True and secondelem == False:
                    foldername = firstvalue
                    folderpath = firstkey
                # if request is wrong formated
                else:
                    raise Exception('Please provide a folder name and a path in a dictionary')
                
                return {foldername, folderpath}
            
        elif saveopen:
            # saveopen request format is: {'folder_name':'name', 'folder_path':'path'}
            #{'folder_path':'path', 'folder_name':'name'}
            assert len(request) == 2,'Too many keys, must be 2'
            
            if firstelem == False and secondelem == False:
                if thirdelem == False and fourthelem == True:
                    filename = firstvalue
                    filefolder = secondvalue
                    
            elif firstelem == False and secondelem == True:
                if thirdelem == False and fourthelem == False:
                    
                    filename = secondvalue
                    filefolder = firstvalue
            else:
                raise Exception('Please provide a folder name and a path in a dictionary')
            
            extension = '.'+filefolder.split('.')[-1]
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
            
        else:
            raise Exception('Please provide a valid request')