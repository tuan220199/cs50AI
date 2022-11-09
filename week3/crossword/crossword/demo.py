dict_value = {}

        value = self.domains[var]
        neighbors = self.crossword.neighbors(var)
        for i in value:
            if i in assignment:
                continue
            else:
                count = 0
                for j in neighbors:
                    if i in self.domains[j]:
                        count += 1
                dict_value[i] = count
        dict_value = sorted(dict_value, key= lambda k: dict_value[k])
        
        return dict_value