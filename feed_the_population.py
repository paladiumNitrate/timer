import numpy as np
import pandas as pd
from animal_specs import AnimalSpecies
from plant_specs import PlantSpecies

class FoodShare():
    
    def __init__(self, populations):
        
        animals = AnimalSpecies()        
        self.species, self.specs, self.spec_matrix = animals.get_matrix()        
        
        self.mass = self.spec_matrix[:, self.specs.index('mass')]
        self.foraging_power = self.spec_matrix[:, self.specs.index('foraging_power')]
        self.diet_type = self.spec_matrix[:, self.specs.index('diet_type')]
        
        self.populations = np.ravel(populations).astype(float)
        n = len(self.species)
        if self.populations.shape[0] != n:
            raise ValueError(f"Population length {self.populations.shape[0]} != number of species {n}")
        
    def predation_summary(self):
        
        eaters = self.who_eats_me()
        
        prey_idx, pred_idx = np.where(eaters)
        preys = self.species[prey_idx]
        preds = self.species[pred_idx]
        
        df = pd.DataFrame({"prey": preys, "predator": preds})        
        prey_groups = df.groupby("prey")["predator"].apply(list)
        pred_groups = df.groupby("predator")["prey"].apply(list)
        
        return df, prey_groups, pred_groups           
        
    def available_food(self):
        
        f_matrix = self.forage_matrix()
        
        food_deliver = self.mass * self.populations * 0.75
        share_for_each = food_deliver[:, None] * f_matrix
        tot_share_for_each = np.sum(share_for_each, axis = 0)
        
        return tot_share_for_each
        
    def forage_matrix(self):
        
        eaters = self.who_eats_me()
        weights = (self.foraging_power[None, :] * eaters).astype(float)
        row_sums = np.sum(weights, axis=1, keepdims = True)
        row_sums[row_sums == 0] = 1    # prevent 0 sums
        norm_f_matrix = weights / row_sums
                
        return norm_f_matrix       
        
    def who_eats_me(self):
        
        n = len(self.species)
        eaters = np.zeros((n, n), dtype = bool)
                
        predator_mask = (self.diet_type == 2) | (self.diet_type == 3)       
        for i in range(n):            
                       
            mass_logic = (self.mass <= (self.mass[i] * 10)) & predator_mask
            forage_logic = (self.foraging_power >= (self.foraging_power[i] * 1.25)) & predator_mask
            eaters[i, :] = mass_logic & forage_logic
                
        return eaters
        
