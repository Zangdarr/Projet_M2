class Fifo:
   liste = []
   size  = 0
   is_empty = True
   cursor = 0
   nbr_elements = 0

   def __init__(self, size):
      self.liste = [[] for i in range(size)]
      self.size = size
      self.is_empty = True
      self.cursor = 0
      self.nbr_elements = 0

   def push_in(self, element):
       self.liste[self.cursor] = element
       self.cursor = (self.cursor + 1) % self.size
       if(self.nbr_elements != self.size):
           self.nbr_elements += 1
       if(not self.is_empty):
           self.is_empty = True

   def get(self):
       return self.liste[0:self.nbr_elements]

   def get_nbr_elements(self):
       return self.nbr_elements
