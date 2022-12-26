# Module to read and write to TLP config files


def WriteToFile(attribute, value, status):
    # function to read and write to config file

    FILE = "/etc/tlp.d/00-test.conf"

    with open(FILE, "r") as fileObj:
        contents = fileObj.readlines()

        for x in contents:
            index = contents.index(x)
            x = x.strip()

            if attribute in x:
                if status:
                    # if status true, uncomment the attribute
                    contents[index] = f"{attribute}={value}\n"
                else:
                    # if status false, comment the attribute
                    contents[index] = f"#{attribute}={value}\n"

        # write the upated values to config file
        with open(FILE, "w") as file:
            for x in contents:
                file.write(x)
