from colorama import Fore


class EasyPy():
    ErrorFedback = True

    def validate_pin(pin, lenght,ErrorFedback):

        if ErrorFedback == True:
            # return true or false
            if len(pin) == lenght:
                if pin.isdigit():
                    print(True)
                    return True
                else:
                    print(Fore.GREEN,"EasyPy:",Fore.RED,f"False Pin with lenght of {lenght}. Actual Lenght:{len(pin)}, The pin is {pin}",)
                    print(Fore.GREEN, "EasyPy:", Fore.RED,f"Perhaps the pin is not a Int, The pin is {pin}")
                    return False

            else:
                print(Fore.GREEN,"EasyPy:",Fore.RED,f"False Pin with lenght of {lenght}. Actual Lenght:{len(pin)}, The pin is {pin}",)
                return False
        else:
            if len(pin) == lenght:
                if pin.isdigit():
                    return True
                else:
                    return False

            else:
                return False
    def getAscii(Item,ErrorFedback):
        if ErrorFedback == True:
            try:
                print(ord(Item))
                return ord(Item)
            except:
                print(Fore.GREEN,"EasyPy:", Fore.RED, "Unknown Error")
        else:
            return ord(Item)
