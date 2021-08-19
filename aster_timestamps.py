import glob
import pandas as pd

def aster_timestamps(directory, ext='hdf'):

    '''Given a directory of ASTER files, read the timestamps of ASTER observations (in UTC) from their filenames.
       Option to search for HDF of TIF files.
       
       Returns timestamp and filepath for each file found.'''
    
    assert (ext == 'hdf') or (ext == 'tif') , "File extension must be either hdf or tif"
    
    # Find all our ASTER files
    search_path = '{directory}/**/*.{ext}'.format(directory=directory, ext=ext)
    aster_files = glob.glob(search_path, recursive=True)
    
    # Create empty list to hold timestamps as we step through all files in the list
    aster_timestamps_UTC = []
    
    # for each filepath in the list of ASTER files
    for fpath in aster_files:
        # Parse the date and time from ASTER filename
        fn = fpath.split('/')[-1]
        MM = fn.split('_')[2][3:5]
        DD = fn.split('_')[2][5:7]
        YYYY = fn.split('_')[2][7:11]
        hh = fn.split('_')[2][11:13]
        mm = fn.split('_')[2][13:15]
        ss = fn.split('_')[2][15:17]
        # create pandas timestamp and append to the list
        aster_timestamps_UTC.append(pd.Timestamp('{}-{}-{} {}:{}:{}'.format(YYYY, MM, DD, hh, mm, ss),tz='UTC'))
    
    # Create pandas dataframe, sort, and reset index
    aster_df = pd.DataFrame({'timestampUTC': aster_timestamps_UTC, 'filepath': aster_files})
    aster_df.sort_values('timestampUTC',inplace=True)
    aster_df.reset_index(inplace=True, drop=True)
    
    return aster_df