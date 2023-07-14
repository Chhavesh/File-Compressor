import heapq
import os

# implementing a binary tree
#this binary tree has in 4 parameter, the value, frequency of the value(key), 
# left child and right child 
class BinaryTree :
    def __init__(self, value, freq) -> None:
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None
        

class Huffman :
    def __init__(self,path) -> None:
        #path to the file
        self.path = path
        #the iterable for stroing the heap
        self.__heap = []
        # a dictionary to store the code from the binary tree nodes
        self.__code = {}
    
    #overloading the less than operator
    def __lt__(self, other) :
        return self.freq < other.freq # as used in the binary tree class

    #overloading the equal to operator
    def __et__(self, other) :
        return self.freq == other.freq
    
    #this functions takes every character in a file, and then maps its frequency of occurence
    def __frequency_from_text(self, text) :
        freq_dic = {}
        for  i in text :
            if i not in freq_dic :
                freq_dic[i] = 0
            
            freq_dic[i] +=1
            return freq_dic
    
    # to push all the elements into the heap
    def __build_heap(self, freq_dict) :
        #we first extract the key value pair in our frequency dictionary
        #then convert the pair into a node of binary tree
        # then push the node into the heap
        for key in freq_dict :
            frequency = freq_dict[key]
            node = BinaryTree(key,frequency)
            #pushing this node onto the heap
            heapq.heappush(self.__heap, node)
        
    # to make the binary tree out of all the nodes present in the min-heap
    # we will take the two most minimum elements and then add the two values
    # then push a new node with key = "" and freq = the sum we calcuated
    # and we repeated this until we have only one elemet in the heap
    def __build_BinaryTree(self) :
        while len(self.__heap) >= 2 :
            node_1 = heapq.heappop(self.__heap)
            node_2 = heapq.heappop(self.__heap)
            
            freq_sum = node_1.freq + node_2.freq
            
            newNode = BinaryTree(None, freq_sum)
            newNode.left = node_1
            newNode.right = node_2 
            heapq.heappush(self.__heap, newNode)  
        return
    
    # this is a helper function for the _encode_Tree for the purpose of recursion
    def __encode_Tree_helper(self, root, curr_bits) :
        if root is None :
            return
        
        # now we want to only go to the leaf nodes, and those are the only nodes that have a value
        # because in all the rest thee value is None
        
        if root.value is not None :
            self.__code[root.value] = curr_bits
        
        self.__encode_Tree_helper(root.left, curr_bits+'0')
        self.__encode_Tree_helper(root.right, curr_bits+'1')
    
    def __encode_Tree(self) :
        # first we have to get the root of the binary tree
        # it is the only element left in the heap
        root = heapq.heappop(self.__heap)
        
        # so what we are trying to do is to move down till the leaf nodes
        # if we move left, we add 0 to our ans, for right we add 1
        # we will use recursion for this
        
        self.__encode_Tree_helper(root, "")
    
    # we are just gonna iterate over the input text and then for each character 
    # we shall look up the corresponding code in our dictionary and then add it into a resultant string    
    def __encodeText(self, text):
        encoded_text = ""
        for elem in text :
            encoded_text += self.__code[elem]
        
        return encoded_text
    
    def __padText(self, encoded_text) :
        # we have a formula for how much we should pad
        # padding = 8 - lengh of text%8
        # for example , if lenght of encoded text is 13, padding = 8-13%8 = 3
        
        padding_value = 8 - len(encoded_text)%8
        
        for i in range(padding_value) :
            encoded_text += '0'
        
        # we also store 8 bit info about how much encoding we did
        padding_info = "{0:08b}".format(padding_value)
        # this takes the 0 index arg, converts it into 8 bit and b if for binaary encoding
        
        padded_text = padding_info + encoded_text
        return padded_text      
    
    #divide in 8 bits
    # convert into integer
    # push into a byte array
    def __make_byte_array(self, padded_text) :
        byte_array = []
        for i in range(0, len(padded_text), 8) :
            byte = padded_text[i:i+8]
            byte_array.append(int(byte, 2))
        
        return byte_array        
        
    
    def compression(self) :
        
        #to access the file and extract text from the file
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + '.bin'
        
        with open(self.path, 'r+') as file, open(output_path, 'wb') as output :
            text = file.read()
            text = text.rstrip()
        
            # create frequency of each element and store it in a freq_dic
            freq_dic = self.__frequency_from_text(text)
            
            # Make a min heap fro    two minimun frequency
            min_heap = self.__build_heap(freq_dic)
            
            # contruct a binary tree from the heap
            self.__build_BinaryTree()
            
            # construct code from the binary tree and store it in a dictionary
            self.__encode_Tree()
            
            # construct encoded text
            encoded_text = self.__encodeText(text)
            
            # now we have to pad the enocded text 
            padded_text = self.__padText(encoded_text)
            
            # now we have to duvuded the padded text into parts of 8bits each (1byte)
            bytes_array = self.__make_byte_array(padded_text)
            
            final_bytes = bytes(bytes_array)
            
            output.write(final_bytes)
            
        print("completed encoding")
        return output_path


path = input("Path :")
obj = Huffman(path)
obj.compression()