import json

class Persistency:
    
    def __init__(self, ratio,herbivor_quantity, carnivor_entity, food_quantity, time, file_path):
                
        dictionary = {
          "Time": time,
          "Herbivor_Quantity": herbivor_quantity,
          "Carnivor_Quantity": carnivor_entity,
          "Food_Quantity": food_quantity,
          "Herbivor/Carnivor-Ratio": ratio
     }

        with open(file_path, "r") as outfile:
            data = json.load(outfile)
            data.append(dictionary)
            outfile.close        
        
        
        with open(file_path, "w") as outfile:
            json_object = json.dumps(data, ensure_ascii=False, indent=5)
            outfile.write(json_object)
            outfile.close        

    def add_initial_information(ratio ,qnt_herb, qnt_carn, qnt_food, file_path):
        dictionary = {
          "Initial_Herbivor": qnt_herb,
          "Initial_Carnivor": qnt_carn,
          "Initial_Food": qnt_food,
          "Ratio_Stable": ratio
     }

        with open(file_path, "r") as outfile:
            data = json.load(outfile)
            data.append(dictionary)
            outfile.close        
        
        
        with open(file_path, "w") as outfile:
            json_object = json.dumps(data, ensure_ascii=False, indent=5)
            outfile.write(json_object)
            outfile.close        

def CreateJson(timestamp):
                
        file_path = f"Helpers/Data/Data{timestamp}.json"
        
        with open(file_path, "w") as outfile:
            json.dump([], outfile)
            
        return file_path


#timestamp = datetime.now().strftime("%Y.%m.%d.%H.%M") # Gets current dat and time to create the file for the simulation
#file_path = CreateJson(timestamp)