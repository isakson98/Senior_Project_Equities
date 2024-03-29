import os
import datetime as dt
import pandas as pd


'''
This class is solely responsible for dealing with files in my database.
Each database has 4 essential functions:
- add
- update
- remove
- retrieve

In essense, this class deals exactly with that. Specify the directory you want
to work in at the start or change it if you have to, and all you have to do then


The beauty of this approach is that it is very flexible. You can rearrange/add
folders if you find this necessary without any additional changes to the code
in this class. This works because the burden of identifying which folder you 
want to work with lies on you. That's fine, because this project is built as
a researcher playground, and as a researcher using these classes you have 
common sense to supply info in a correct fashion. There are several exceptions,
and if statements that protect user in some ways from messing up

PS. can think of this as a wrapper for the os module
'''
class DataFlatDB:
    
    # need to go one dir up to get access to database, since we are in a folder
    # root_data_dir = os.path.dirname(__file__)
    # root_data_dir = os.path.dirname(root_data_dir)

    # new directory with data files
    root_data_dir = r'C:\Users\isaks\OneDrive\Desktop\Everything\Personal code\trading\_DATABASE_'
    dir_operated_on = None
    suffix = None

    '''
    params:
        dir_list_to_operate_in -> list of top-down directories that lead to the one you want to work on

    it is intended to use an object of this class to operate on one directory
    at a time. Use two of these objects if you have simultenous directories you are working on. 
    '''
    def __init__(self, dir_list_to_operate_in : list):
        self.change_dir(dir_list_to_operate_in)

    ###################
    # Private Methods #
    ###################

    '''
    params
        file_path -> path to file to be renamed

    description:
        this function is used when a new version of data is available,
        but the old one is decided to be saved as well. Use this function
        to add date to the outdated file, so as to show that it is an old file

    returns:
        new_path_old_file -> new path of the old file, the one renamed
    '''
    def __add_date_to_file_name(self, file_path : str) -> str:
        directory, file_name =  os.path.split(file_path)
        _, str_date = self.__get_todays_date(file_path)
        new_file_name = str_date + "_" + file_name 
        new_path_old_file = os.path.join(directory, new_file_name)
        
        if os.path.exists(new_path_old_file) == False:
            os.rename(file_path, new_path_old_file)

        return new_path_old_file

    '''
    params:
        file_name -> name of the file to have an operation on

    description:
        helper function that creates the suffix of the file, based on 
        where the file is located. Builds two 

        if price/1_day/file_name, file_name must have price_1_day as suffix of the name

    returns:
        bool

    '''
    def __create_file_suffix(self, ext=".csv", depth=2):

        suffix_parts = list()
        rest = self.dir_operated_on
        for count in range(depth):
            rest, current_dir = os.path.split(rest)
            # we want to stop before adding data to sufix
            if current_dir == "data":
                break
            suffix_parts.append(current_dir)

        suffix_parts.reverse()
        suffix = "_".join(suffix_parts)
        suffix = "_" + suffix + ext
        self.suffix = suffix

        return True

    '''
    params:
        none

    description:
        helper function that fetches the creation date of the file

    returns 
        creation_date -> datetime object of the date
        string_v -> string version of the date for adding to file name
    '''
    def __get_todays_date(self) -> list:

        today_date = dt.date.today()
        string_v = today_date.strftime("%d-%b-%Y")
        return [today_date, string_v]

    '''
    params:
        list_dir -> list of directories in top-down order for concatenation

    description:
        helper function used in all functions available to the user of this class
        this function concatonates the given elements in the list 

    returns:
        string_path -> the full path given 
    '''
    def __merge_path_content(self, list_dir : list) -> str:
        # asterisk before list expands list into number of elements it has
        string_path = os.path.join(self.root_data_dir, *list_dir)

        return string_path

    ##################
    # Public Methods #
    ##################

    '''
    params:
        string_path -> the path given to verify

    description:
        this function is used before operating on existing files
        to verify that the file actually exists

    returns:
        boolean -> True if file exists / False otherwise
    '''
    def verify_path_existence(self, string_path : str):

        if not os.path.exists(string_path):
            client_use = os.path.join(self.dir_operated_on, string_path)
            if os.path.exists(client_use):
                return True
            return False
        return True

    '''
    params:
        root_name_file -> name of the file to be added
        content_to_add -> content of this new file

    description:
        one of core functions of this class. use this function to create new files

    returns:
        True/False -> True if write was successful
    '''
    def add_data(self, root_name_file : str, content_to_add : pd.DataFrame, default_suffix=True):
        full_name = root_name_file + self.suffix
        full_path = self.__merge_path_content([self.dir_operated_on, full_name])
        exists = self.verify_path_existence(full_path)
        if exists:
            print(f"New data not added because file exists {full_name}")
            return False
        content_to_add.to_csv(full_path, index=False)
        return True

    '''
    params:
        full_file_name -> name of the file to be added
        content_to_add -> full content of this new file
        keep_old -> boolean, if yes, existing old data will be kept but renamed, with date added

    description:
        With entire df as parameter, update_data() saves to file name given.
        Unlike adding, this function also has a feature of keeping the old content of the file
        by renaming it, adding the date the file was originally created (useful for watchlists)

    returns:
        True/False -> True if write was successful
    '''
    def update_data(self, full_file_name, content_to_add, keep_old):
        full_path = self.__merge_path_content([self.dir_operated_on, full_file_name])
        exists = self.verify_path_existence(full_path)
        if not exists:
            print(f"{full_file_name} could not be updated because it doesn't exist")
            return False

        if keep_old:
            # "frees up" space for new data to take up this file name
            self.__add_date_to_file_name(full_path)

        content_to_add.to_csv(full_path, index=False)

        return True

    '''
    params:
        full_file_name -> root name of file you want data of + suffix will be appended

    description:
        if no files is given, you return everything containing in that folder

    returns:
        dict -> path ->full path to file, data
    '''
    def retrieve_data(self, full_file_name) -> pd.DataFrame():
        full_path = self.__merge_path_content([self.dir_operated_on, full_file_name])
        df = pd.DataFrame()
        try : 
            df = pd.read_csv(full_path)
        except:
            print(f"{full_file_name} could not be read")
        return df
        
    '''
    params:
        none

    description:
        you returns everything containing in that folder
    
    return
        big_list list of dataframes in the folder
    '''
    def retrieve_all_file_names(self) -> list():
        return os.listdir(self.dir_operated_on)

    '''
    params:
        file_name -> name of file with 

    description:
        parses out the ticker out of the file name

    returns:
        returns the ticker portion of the file name
    '''
    def __retrieve_ticker_name_helper(self, file_name):
        split_list = file_name.split("_")
        return split_list[0]

    '''
    params:
        none
    
    description:
        you returns every ticker symbol containing in that folder
        using map() that enacts that function on every element of the iterable

    return
        all_ticker_names 
    '''
    def retrieve_all_ticker_names(self) -> list():
        all_dir_files = self.retrieve_all_file_names()
        # convert back to the list object 
        all_ticker_names = list(map(self.__retrieve_ticker_name_helper, all_dir_files))
        return all_ticker_names


    '''
    params:
        full_file_name -> name of file you want data of

    description:
        this function deletes a file (if that ever becomes necessary)

    return:
        bool
    '''
    def remove(self, full_file_name):
        full_path = self.__merge_path_content([self.dir_operated_on, full_file_name])
        os.remove(full_path)
        return True

    '''
    params:
        dir_list_to_operate_in -> list of top-down directories that lead to the one you want to work on

    description:
        I am anticipating working a lot with a lot of files just one directory at a time.
        To avoid overhead constantly verifying full file path for every file, 
        I decided to allow to specify it just once. This way it's not done redundantly.
        If you decide to change the directory, you can do it using this function.
        It will change the member variable that is used in all main functions,
        that stores the full path to the directory 

    returns:
        str_dir -> full path given as a list as a param turned into a string
    '''
    def change_dir(self, dir_list_to_operate_in : list):
        str_dir = self.__merge_path_content(dir_list_to_operate_in)
        if not self.verify_path_existence(str_dir):
            raise ValueError(f'{str_dir} does not exist! Reexamine the path')
        self.dir_operated_on = str_dir
        self.__create_file_suffix()
        return str_dir

