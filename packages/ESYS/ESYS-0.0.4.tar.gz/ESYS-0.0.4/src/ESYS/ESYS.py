def error(ErrorName,Errorvalue):
    if ErrorName=="NameError":
        raise NameError(Errorvalue)
    elif ErrorName=="SyntaxError":
        raise SyntaxError(Errorvalue)
    elif ErrorName=="IndentationError":
        raise IndentationError(Errorvalue)
    elif ErrorName=="SystemError":
        raise SystemError(Errorvalue)
    elif ErrorName=="ValueError":
        raise ValueError(Errorvalue)
    elif ErrorName=="TypeError":
        raise TypeError(Errorvalue)
    elif ErrorName=="ZeroDivisionError":
        raise ZeroDivisionError(Errorvalue)
    elif ErrorName=="RuntimeError":
        raise RuntimeError(Errorvalue)
    elif ErrorName=="Exception":
        raise Exception(Errorvalue)
    elif ErrorName=="BaseException":
        raise BaseException(Errorvalue)
    elif ErrorName=="KeyboardInterrupt":
        raise KeyboardInterrupt(Errorvalue)
    elif ErrorName=="OSError":
        raise OSError(Errorvalue)
    elif ErrorName=="SystemExit":
        raise SystemExit(Errorvalue)
    elif ErrorName=="FileNotFoundError":
        raise FileNotFoundError(Errorvalue)
    elif ErrorName=="ConnectionError":
        raise ConnectionError(Errorvalue)
    elif ErrorName=="TabError":
        raise TabError(Errorvalue)
    elif ErrorName=="EOFError":
        raise EOFError(Errorvalue)
    elif ErrorName=="AssertionError":
        raise AssertionError(Errorvalue)
    elif ErrorName=="AttributeError":
        raise AttributeError(Errorvalue)
    elif ErrorName=="FloatingPointError":
        raise FloatingPointError(Errorvalue)
    elif ErrorName=="Error":
        raise ImportError(Errorvalue)
    elif ErrorName=="GeneratorExit":
        raise GeneratorExit(Errorvalue)
    elif ErrorName=="ModuleNotFoundError":
        raise ModuleNotFoundError(Errorvalue)
    else:
        raise Exception("Unsupported Error. Please try again with another Error.")
def GetTwo(Form,Space):
    if Form=="int":
        a,b=map(int,input("").split(Space))
    elif Form=="float":
        a,b=map(float,input("").split(Space))
    elif Form=="str":
        a,b=map(str,input("").split(Space))
    else:
        raise ValueError(f"Didn't Put the right form. Please input int or float or str, and not {Form}")
def add_one(a):
    b=a+1
    return b
