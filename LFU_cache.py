"""
// Time Complexity 
get - O(1)
put - O(1)
// Space Complexity : O(n)
// Did this code successfully run on Leetcode : Yes
// Any problem you faced while coding this : No
// Your code here along with comments explaining your approach
Algorithm explanation
We leveraged the use of OrderedDict to keep track of least recently
used elements and most recently used items
Initial configuration - 
a) keyToCount map - dictionary mapping the key to count of occurence
b) countToLRU - dictionary mapping the count to ordered dict of key,val

- get
    General idea is 
        - increment the count of the key to 1 in the keytocount map
        - Update the countToLRU map because of change in count
        - Keep track of min count
        - return the val for the key
- put
    General idea is
        - if the key is already present
            - call get operation
            - update the value for the key in the count to LRU map
        - if the size of the cache reaches the capacity
            - remove the least freq element using min_count from the LRU map
            - remove the corresponding key from freq map
            - add the new key with val
        - else (new entry)
            - add the fresh entry of key with count 1
            - reset the min count to 1
            - add the new key with val in LRU map
"""

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        #stores the key to frequency mapping
        self.keyToCount = {}
        #the map that stores the (key,value) pair per count of key
        self.countToLRU = defaultdict(OrderedDict)
        self.min_count = 1

    def get(self, key: int) -> int:
        cnt = self.keyToCount.get(key)
        if not cnt:
            return -1
        #self.keyToCount.move_to_end(key)
        #prev_cnt = self.keyToCount[key][1]
        
        #incrementing the count
        self.keyToCount[key] += 1
        
        #popping the key in the LRU map for the current count
        val = self.countToLRU[cnt].pop(key)
        
        #checking if the count LRU map is empty
        if not self.countToLRU.get(cnt):
            #delete the entry from the map for the count
            del self.countToLRU[cnt]
            
            #regulating the min count to keep it updated based on shuffling
            if cnt == self.min_count:
                self.min_count+=1
        
        #Add the new cnt entry with (key,val) in the LRU map
        self.countToLRU[cnt+1][key] = val
        
        return val

    def put(self, key: int, val: int) -> None:
        
        def add_new_entry():
            #add the new entry with count 1 for the key and update the corresponding count in the LRU map
            self.keyToCount[key] = 1
            
            #reset the min count
            self.min_count = 1
            
            #update the count to LRU map
            self.countToLRU[1][key] = val
        
        # print('put', key, value, self.keyToCount)
        if not self.capacity:
            return
        frequency = 1
        
        #check if key is already present in the count map
        if key in self.keyToCount:
            
            #repeat the process done in get operation
            self.get(key)
            
            #update the LRU with the updated val for the current count
            self.countToLRU[self.keyToCount[key]][key] = val
            
            #self.keyToCount.move_to_end(key)
            #frequency = self.keyToCount[key][1] + 1
        elif len(self.keyToCount) ==  self.capacity:
            #remove the least frequently used element(freq-> min_count), always removes from the start
            key_to_be_removed,_ = self.countToLRU[self.min_count].popitem(last=False)
            #delete the count entry from the keytocount map
            del self.keyToCount[key_to_be_removed]
            add_new_entry()
        else:
            add_new_entry()

# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)