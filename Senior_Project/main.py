'''

if new type of data arrives -> manually create a folder or reorganize stuff
then give the location to DataReceiveExtractor class

need some kind of structure that verifies the data directories


THIS OF THIS AS A CLIENT SPACE.
This is the researcher ground.
This is where you are going to request and write stuff and ask for analysis
Do not delegate everything to library classes, as this overfits stuff (no hard coding)


'''
# popular scripts, combination of all modules features above
from CommonScripts import CommonScripts
# from DataBase.popular_paths import popular_paths

# default python
import time


if __name__ == '__main__':
    start = time.time()
    ###################################################################
    # PLACE SCRIPT BETWEEN THE TWO LINES (any of the methods from CommonScript class)
    # You can define your own function or change parameters of existing ones
    ###################################################################
    comm_obj = CommonScripts()
    comm_obj.draw_descending_trendline_on_bullish_stock("AAPL")
    ##################################################################
    end = time.time()
    print(str(end-start) + " seconds")