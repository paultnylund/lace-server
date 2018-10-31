class Stack:
    '''Create and initialise a Stack 

    This class creates and initialises a Stack datastructure. The class
    includes various functions to either modify or check values on the stack.

    Attributes:
        items: An ordered python list to initialise the stack
    '''
    def __init__(self, items):
        '''Initialise the stack with the items from args or an empty list

        Args:
            items: An ordered python list to initialise the stack
        '''
        self.items = items or []
    
    def isEmpty(self):
        '''Check if the stack is empty

        Returns:
            (bool): True if the array is empty, else False
        '''
        return self.items == []
    
    def push(self, item):
        '''Push an item onto the stack

        Args:
            item: The item to push on the stack
        '''
        self.items.append(item)

    
    def pop(self):
        '''Pop and return the first item on the stack
        
        Returns:
            Returns the item that was popped off the stack
        '''
        return self.items.pop()
    
    def peek(self):
        '''Find the first item on the stack

        Returns:
            Returns the first item on the stack
        '''
        return self.items[len(self.items) - 1]
    
    def next_peek(self):
        return self.items[len(self.items) - 2]
    
    def reset(self, items):
        self.items = items
    
    def size(self):
        '''Find the number of items in the stack

        Returns:
            (int): Returns the number of items in the stack
        '''
        return len(self.items)