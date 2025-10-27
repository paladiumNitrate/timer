import numpy as np



class LifeCycle():
    
    
    def __init__(self, life_spans, num_of_ancestors, tot_popul, max_lifetime):
        
        self.life_spans = life_spans           # python list        
        self.num_of_ancestors = num_of_ancestors
        self.fertile_window = np.array([0.3, 0.8])
        self.max_lifetime = max_lifetime
        self.tot_popul = tot_popul
        
        
    def life_matrix(self):
        
        life_bins = np.zeros([self.num_of_ancestors, self.max_lifetime])
        life_bins[:, 0] = self.tot_popul
        
        return life_bins
        
    def death_matrix(self):
        
        life_limit = np.ones([self.num_of_ancestors, self.max_lifetime])
        
        for i, l_s in enumerate(self.life_spans):
            life_limit[i, int(l_s) - 1] = 0
            
        return life_limit
        
    def fertility_matrix(self):
        
        fertile_matrix = np.zeros([self.num_of_ancestors, self.max_lifetime])
        for i, l_s in enumerate(self.life_spans):
            fertile_index = np.ceil(l_s * self.fertile_window).astype(int)
            fertile_matrix[i, fertile_index[0]: fertile_index[1]] = 1
            
        return fertile_matrix
