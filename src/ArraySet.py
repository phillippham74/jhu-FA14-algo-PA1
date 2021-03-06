import shutil, subprocess
import os,logging, sys, math
log = logging.getLogger("PA1")

class ArraySet():
    """ This class is an implementation of a Set using two arrays, as suggested
    for Programming Assignment #1 """
    
    def __init__(self,trace=False):
        """
        :param config_vars: configuration variables from the config file
        :type config_vars: dict
        :returns: None
        
        """
        
        self.trace = trace      # If trace is on, make sure to log all activity
        
        self.long_array = []      # THis is the longer array used for the set
        self.short_array = [None]     # This is the shorter array used for the set
    
    def merge(self):
        """ This function merges the short and long array together """
        log.info("Merging short and long arrays together")
        
        self.long_array
        self.short_array
        
        element_count = 0
        temp_array = []          # Temporary array to hold merged values
        while len(self.long_array) > 0 and len(self.short_array)>0:
            element_count += 1
            log.info("Adding element #{0} to new merged array".format(element_count))
            if self.short_array[0] < self.long_array[0]:
                temp_array.append(self.short_array.pop(0))
            else:
                temp_array.append(self.long_array.pop(0))
            
        
        for remaining_elem in self.long_array + self.short_array:
            element_count += 1
            log.info("Adding element #{0} to new merged array".format(element_count))
            temp_array.append(remaining_elem)   # Add remaining values from lsits
        
        self.long_array = temp_array        # Replace long array
        
        self.short_array = [None for x in xrange(int(math.sqrt(len(self.long_array))))]
    
    def insert_into_array(self,element,array_to_insert_into,needLog=True):
        """ This function merges the short and long array and
        reallocates them into the longer array """
        """
        null_index = array_to_insert_into.index(None)
        array_to_insert_into[null_index] = element
        self.insertion_sort(array_to_insert_into)
        """
        
        x = 0
        while x < len(array_to_insert_into):
            orig_element = array_to_insert_into[x]
            if needLog:
                log.info("Checking element in index: {0} from short array with length {1}, and total items across both lists: {2}".format(x, 
                         len([item for item in self.short_array]),
                         len([item for item in self.short_array + self.long_array if item != None])))
            if orig_element == None:          # If None is found, then insert and break!
                array_to_insert_into[x] = element
                break
            elif element >= orig_element:
                x +=1
                continue
            else:
                array_to_insert_into[x] = element
                y = x+1
                if y == len(array_to_insert_into):
                    break
                
                while y < len(array_to_insert_into) and (array_to_insert_into[y] < orig_element or array_to_insert_into[y] == None):
                    if array_to_insert_into[y] == None:
                        array_to_insert_into[y] = orig_element
                        break
                    
                    next_element = array_to_insert_into[y]
                    
                    array_to_insert_into[y] = orig_element
                    orig_element = next_element
                    y += 1
                break
        
        if None not in array_to_insert_into:    # If None doesn't exist, then there is no more room in the array
            self.merge()
    
    def insert(self,element):
        """ This function will insert the element into the ArraySet. It will
        call insert_into_array to actually insert it into the array.
        
        :param element - type str - element to insert into the ArraySet
        :returns None
        """
        log.info("Inserting element: {0}".format(element))
        
        self.insert_into_array(element,self.short_array)
        
        """
        log.info("New short list: {0}".format(self.short_array))
        log.info("New long list: {0}".format(self.long_array))
        """
    
    def search(self,element):
        """ This function will search for an element in the ArraySet
        
        :param element - type str - element to insert into the ArraySet
        :returns bool - True if the element is found in the Arrayset, or False
        if it doesn't exist
        """
        
        found = False
        for search_list in [self.short_array,self.long_array]:
            found = self.exists(element, search_list)
            if found:
                break
        return found
    
    def exists(self,element,list_to_search):
        """ This function implements the binary search to check whether or not an element exists
        in the list
        
        :param element - type str - element to search for
        :param list_to_search - type list - list to check whether an element exists
        """
        beg = 0
        end = len(list_to_search) - 1
        while True:
            if end < beg:
                return False
            
            mid = (beg + end) / 2
            
            log.info("Checking if result element {0} is equal to search element {1}, total length of list: {2}".format(list_to_search[mid],element,len(list_to_search)))
            if list_to_search[mid] == None:
                return False
            elif list_to_search[mid] < element:
                beg = mid + 1
            elif list_to_search[mid] > element:
                end = mid - 1
            else:
                return True
        return False
    


class ArraySetRunner():
    """ This class will run the program for Programming Assignment #1 """
    
    def __init__(self,inputfile):
        """ Constructor takes an input file with elements to insert and search
        for in the ArraySet
        
        :param inputfile - type str - inputfile on the local disk to use
        for inserting and searching
        """
        self.elements = []      # List of elements to insert/search for
        
        self.array_set = ArraySet()
        
        self.read_input_file(inputfile)
    
    def read_input_file(self,filename):
        
        if os.path.exists(filename):
            log.info("Reading input file for elements: {0}".format(filename))
            infile = open(filename)
            self.elements = infile.read().split()
            infile.close()
            log.info("Found {0} elements in input file".format(len(self.elements)))
        
        else:
            log.error("Input file does not exist: {0}".format(filename))
    
    
    def execute(self,options):
        """ This function will run Programming Assignment #1 and will output
        various information based on the type of the run given as input"""
        
        self.build_database()
        self.query_element(options.query_element)
    
    def query_element(self,element):
        log.info("Querying for element {0}".format(element))
        found = self.array_set.search(element)
        log.info("Element exists? {1}".format(element,found))
        print "Element '{0}' exists? {1}".format(element,found)
    
    def build_database(self):
        log.info("Building the ArraySet")
        for element in self.elements:
            self.array_set.insert(element)
            """
            print "\n\nSHORT ARRAY: ", self.array_set.short_array
            print "LONG ARRAY: ", self.array_set.long_array
            """
    
if __name__ == "__main__":
    import optparse
    
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-l', dest="log",default=False,action="store_true",
                      help="Turn on logging (trace)")
    parser.add_option("-i","--input", dest="inputfile", default=False,
                      help="Input file with the elements to add to the ArraySet")
    parser.add_option("-q","--query",dest="query_element",
                      help = "Element to query for from the ArraySet")
    (options, args) = parser.parse_args()
    
    
    if not options.inputfile:
        parser.error("Must provide an input file with elements to insert into the ArraySet")
    
    if not options.query_element:
        parser.error("Must provide an element to query for in the ArraySet")
    
    fmt = logging.Formatter(fmt="%(asctime)s:%(levelname)-8s:%(filename)-20s:%(message)s")
    hdl = logging.StreamHandler(sys.stdout)
    hdl.setFormatter(fmt)
    log.addHandler(hdl)
    if options.log:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.CRITICAL)
    
    runner = ArraySetRunner(options.inputfile)
    runner.execute(options)