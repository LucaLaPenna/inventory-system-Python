import datetime
import json
import pickle

"""
ADD REFERENCING 
"""


class Batch:
    def __init__(self, B_id, B_type, B_fit, B_nc, B_date, B_component, location):
        self.B_id = B_id
        self.B_type = B_type
        self.B_fit = B_fit
        self.B_nc = B_nc
        self.B_date = B_date
        self.B_component = B_component
        self.location = location

    def __str__(self):
        return "Batch details for: {0}\n" \
               "Components' type: {1}\n" \
               "Components' fit {2}\n" \
               "Number of components: {3}\n" \
               "Manufacture date:{4} \n ".format(self.B_id, self.B_type, self.B_fit, self.B_nc, self.B_date)


class Component:

    def __init__(self, C_id, C_status):
        self.C_id = C_id
        self.C_status = C_status

    def __str__(self):
        return "Component ID: {0} status: {1}\n".format(self.C_id, self.C_status)


def Validation(user_input, desired_output):
    while user_input not in desired_output:
        user_input = input("Error: invalid option; please input a valid option > ")
    return user_input


def next_batch_number(existing_batches):
    if len(existing_batches) == 0:
        previous_batch = "000000000000"
    else:
        previous_batch = max(existing_batches)
    today = str(datetime.date.today())  # 2019-03-02
    today = today.replace("-", "")  # 20190302
    if today == previous_batch[:8]:
        next_batch = today + str(int(previous_batch[8:]) + 1).zfill(4)  # The last 4 character of the string get turned
        # into a number and then incremented by 1 to then be turned back into a 4 character string using zfill
        return next_batch
    else:
        return today + "0001"


def get_batch_type():
    print("Please select the product type from the options below:")
    print("1. Winglet Strut, 2. Door Handle, 3. Rudder Pin")
    option = input("Please enter a component type number > ")
    option = Validation(option, ["1", "2", "3"])

    if option == "1":
        the_type = "Wingless Strut"

    elif option == "2":
        the_type = "Door Handle"

    elif option == "3":
        the_type = "Rubber Pin"
    return the_type


def get_batch_type_fit(the_type):
    """
    :param the_type:
    :return:
    """
    the_type_fit = ""
    if the_type == "Wingless Strut":

        print("1. A320 Series, 2. A380 Series")
        option = Validation(input("Please enter a fitment type number > "), ["1", "2"])
        if option == "1":
            the_type_fit = "A320 Series"
        elif option == "2":
            the_type_fit = "A380 Series"

    if the_type == "Rubber Pin":
        print("1. 10mm x 75mm, 2. 12mm x 100mm, 3. 16mm x 150mm")
        option = Validation(input("Please enter a fitment type number > "), ["1", "2", "3"])
        if option == "1":
            the_type_fit = "10mm x 75mm"
        elif option == "2":
            the_type_fit = "12mm x 100mm"

        elif option == "3":
            the_type_fit = "16mm x 150mm"

    if the_type == "Door Handle":
        the_type_fit = "No Fit Type"
    return the_type_fit


def nc_generator():
    def test(numberComponent):
        while type(numberComponent) != int:
            try:
                numberComponent = int(numberComponent)
                while numberComponent < 1 or numberComponent > 9999:
                    numberComponent = test(input("Error: invalid input; please enter a number between 1 and 9999 > "))
                return numberComponent
            except ValueError:
                numberComponent = test(input("Error: invalid input; please input a number > "))
        return numberComponent

    numberComponent = test(input("Please enter the number of components you would like to create (1-9999)"))
    return numberComponent


def verification(current_batch):
    print("The batch " + current_batch.B_id + " contains " + str(current_batch.B_nc) + " " + current_batch.B_fit +
          " " + current_batch.B_type + "(s) componenets")  #
    choice = Validation(input("Is the information above correct?(Y/N)"), ["Y", "y", "N", "n"])
    if choice == "Y" or choice == "y":
        return "Y"
    else:
        return "N"


def component_generator(current_batch):
    nc = int(current_batch.B_nc)
    for n in range(nc):
        C_id = str(current_batch.B_id) + "-" + str(n + 1).zfill(4)
        C_status = "MANUFACTURED-UNFINISHED"
        current_batch.B_component[C_id] = Component(C_id, C_status)
        save_component(current_batch.B_component[C_id])
    return current_batch.B_component


def printdetails(current_batch):
    print(current_batch)
    for keys in current_batch.B_component:
        print(current_batch.B_component[keys])


# Data
def update_list(existing_batches):
    with open("..\Data\BatchIndex.json", "w") as f:
        json.dump(existing_batches, f)
    print("Saved")


# Data
def readbatches():
    with open("..\Data\BatchIndex.json") as f:
        r_batches = json.load(f)
    return r_batches


# Data
def save_batch(batch):
    f = open("..\Data\\" + batch.B_id + ".pck", "wb")
    pickle.dump(batch, f)
    f.close()


# Data
def save_component(component):
    f = open("..\Data\\" + component.C_id + ".pck", "wb")
    pickle.dump(component, f)
    f.close()


# Data
def read_batch(batch_name):
    f = open("..\Data\\" + batch_name + ".pck", "rb")
    batch = pickle.load(f)
    f.close()
    return batch


def read_component(component_name):
    f = open("..\Data\\" + component_name + ".pck", "rb")
    component = pickle.load(f)
    f.close()
    return component


def create_batch():
    previous_batches = readbatches()
    print(previous_batches)
    batch_id = next_batch_number(previous_batches)
    date = datetime.date.today()
    the_type = get_batch_type()
    the_type_fit = get_batch_type_fit(the_type)
    nc = nc_generator()  # nc stands for number of components
    location = "Factory Floor – Warehouse Not Allocated"
    current_batch = Batch(batch_id, the_type, the_type_fit, nc, date, {}, location)
    choice = verification(current_batch)
    if choice == "Y":
        B_component = component_generator(current_batch)
        current_batch = Batch(batch_id, the_type, the_type_fit, nc, date, B_component, location)
        save_batch(current_batch)
        printdetails(current_batch)
        previous_batches.append(batch_id)
        update_list(previous_batches)


    else:
        pass


def display_all():    # list all batches

    batches = readbatches()
    if len(batches) == 0:
        print("There are no batches to display.")
    else:
        number_of_batches = len(batches)
        print("Batch \t\t Type \t\t\t Size/Fit \t\t Quantity made \t Location")
        for y in range(number_of_batches):
            batch = read_batch(batches[y])
            print(batch.B_id + " " + batch.B_type + "\t " + batch.B_fit + "\t " + str(batch.B_nc) + "\t\t\t\t "
                  + batch.location)
        print()
        print("~There are no more batches to display~")


def display_batch(batch_number):
    if batch_number not in readbatches():
        print("Batch does not exist")
    else:
        batch = read_batch(batch_number)
        print("Manufacture date: \t\t\t\t" + str(batch.B_date))
        print("Component type: \t\t\t\t" + batch.B_type)
        print("Component size/fitment type: \t" + batch.B_fit)
        print("Number of components in batch:  " + str(batch.B_nc))
        print("location \t\t\t\t\t\t" + batch.location)
        for keys in batch.B_component:
            print("Component id: \t\t\t\t\t" + batch.B_component[keys].C_id)
            print("Component status: \t\t\t\t" + batch.B_component[keys].C_status)


def display_component(component_number):
    batch_number = component_number[:12]
    if batch_number not in readbatches():
        print("Batch does not exist")
    else:
        batch = read_batch(batch_number)
        components = []
        for keys in batch.B_component:
            components.append(keys)
        if component_number not in components:
            print("component does not exist in batch")
        else:
            component = batch.B_component[component_number]
            print("Component id: \t\t\t\t\t " + component.C_id)
            print("Component status: \t\t\t\t " + component.C_status)
            print("Component type: \t\t\t\t " + batch.B_type)
            print("Component size/fitment type: \t " + batch.B_fit)
            print("Manufacture date: \t\t\t\t " + str(batch.B_date))


def allocation(batch_number):
    if batch_number not in readbatches():
        print("Batch does not exist")
    else:
        batch = read_batch(batch_number)
        if batch.location == "Factory Floor – Warehouse Not Allocated":
            choice = Validation(input("Select warehouse (1.Paisley, 2.Dubai) >"), ["1", "2"])
            if choice == "1":
                batch.location = "Paisley"
                print("This batch is now allocated and will be shipped to Paisley")
            elif choice == "2":
                batch.location = "Dubai"
                print("This batch is now allocated and will be shipped to Dubai")
            save_batch(batch)
        else:
            print("This batch has been already allocated")


def search():
    desired_batches = {}
    type = get_batch_type()
    fit = get_batch_type_fit(type)
    choice = Validation(input("You selected: " + fit + " " + type + ", is this information correct? (Y/N)"),
                        ["Y", "y", "N", "n"])
    if choice == "Y" or choice == "y":
        for batch in readbatches():
            batch = read_batch(batch)
            if batch.B_fit == fit:
                desired_batches[batch.B_id] = batch
        if len(desired_batches) == 0:
            print("there was no " + fit + " " + type + " available in stock  ")
        else:
            for batch in desired_batches:
                print(desired_batches[batch])
                for component in desired_batches[batch].B_component:
                    print(desired_batches[batch].B_component[component])
    else:
        pass


def finish(component_number):
    batch_number = component_number[:12]
    if batch_number not in readbatches():
        print("Batch does not exist")
    else:
        batch = read_batch(batch_number)
        components = []
        for keys in batch.B_component:
            components.append(keys)
        if component_number not in components:
            print("component does not exist in batch")
        else:
            component = read_component(component_number)
            if component.C_status == "MANUFACTURED-UNFINISHED":
                choice = Validation(input("Select finish (1.Polished, 2.Painted) >"), ["1", "2"])
                if choice == "1":
                    component.C_status = "Polished"
                    batch.B_component[component_number].C_status = "Polished"
                    print("This component has been finished with polish")
                elif choice == "2":
                    component.C_status = "Painted"
                    batch.B_component[component_number].C_status = "Painted"
                    print("This component has been finished with painted")
                save_component(component)
                save_batch(batch)
                save_batch(batch)
                print("finished")
            else:
                print("This component has been already finished")


def main():
    while True:
        print("Please choose an option:")
        print("1 Create a new batch")
        print("2 List all batches")
        print("3 View details of a batch")
        print("4 View details of a component")
        print("5 Allocate manufactured stock")
        print("6 Search by product type")
        print("7 Finish a component")
        print("8 Exit")
        option = Validation(input("> "), ["1", "2", "3", "4", "5", "6", "7", "8"])
        if option == "1":
            create_batch()
        elif option == "2":
            display_all()
        elif option == "3":
            display_batch(input("Enter batch number: "))
        elif option == "4":
            display_component(input("Enter component number"))
        elif option == "5":
            allocation(input("Enter batch number"))
        elif option == "6":
            search()
        elif option == "7":
            finish(input("Enter component number"))
        elif option == "8":
            check = Validation(input("Are you sure? Y for yes and N for no"), ["Y", "y", "N", "n"])
            if check == "Y" or check == "y":
                print("Thank you, bye")
                break  # Ends the program
            else:
                print("")


if __name__ == '__main__':
    main()
