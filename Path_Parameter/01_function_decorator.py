# def fence(func): #with our func we can perform things before and after it 
#     def wrapper():
#         print("+" * 10)
#         func()
#         print("+" * 10)
#     return wrapper


# @fence  #when python interpreater will see this statement it goes ahead and take log() func declaration, provide it to fence, and in fence we go ahead and recieve it as argument
# def log():
#     print("decorated !")



# log()



#------------------------------------------------------------------------------------------------
# CUSTOM FENCE/ CUSTOM ARGUMENT IN DECORATOR FUNCTION


def custom_fence(fence: str = '+'):

    def add_func(func):

        def wrapper(text: str):
            print(fence * len(text))
            func(text)
            print(fence * len(text))
            
        return wrapper

    return add_func


@custom_fence("-")
def log(text: str):
    print(text)


log("ballon")



#output >>

# ------
# ballon
# ------