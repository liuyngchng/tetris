def no_return(a):
    a["a"] = "test"

 

if __name__ == "__main__":
    a = {"a":123}
    print(a)
    no_return(a)
    print(a)

