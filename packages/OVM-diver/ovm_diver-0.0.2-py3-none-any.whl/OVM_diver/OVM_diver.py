
def topoff():
    '''
    Calculate the resulting trimix after topping up
    '''
    O2_start = int(input("Enter the O2 part of the starting mix: "))  
    He_start = int(input("Enter the Helium part of the starting mix: "))  
    P_start = int(input("Enter the starting fill pressure: "))  
    O2_fill = int(input("Enter the O2 part of the topoff mix: "))  
    He_fill = int(input("Enter the Helium part of the topoff mix (default = 0): ") or 0 )  
    P_result = int(input("Enter the final pressure: "))  
    
    O2_result = ( (P_start * O2_start) + ((P_result - P_start) * O2_fill )) / P_result
    O2_result = round((O2_result),1)

    He_result = ( (P_start * He_start) + ((P_result - P_start) * He_fill )) / P_result 
    He_result = round((He_result),1)

    end_mix = "Tx " + str(O2_result) + "/" + str(He_result)

    print(" ")
    print("Final mix:")
    print("----------")
    print("O2: " + str(O2_result) + " %")
    print("He: " + str(He_result) + " %")
    print(" ")
    print("ANALYSE BEFORE DIVING")

    input("Press ENTER to close")


def fill():
    '''
    Calculate the resulting trimix after topping up
    '''
    v_donor = int(input("Enter tanksize of the donor tank in liters: "))
    p_donor = int(input("Enter pressure of the donor tank in bar: "))  
    v_target = int(input("Enter tanksize of the target tank in liters: "))  
    p_target = int(input("Enter starting pressure of the donor tank in bar: ") or 1 )  

    result = ((v_donor * p_donor) + (v_target * p_target)) / (v_donor + v_target)

    print(result)

    input("Press ENTER to close")


def blend():
    '''
    Calculate the gasses needed for desired mix
    '''


