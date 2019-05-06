def validate_strictly_positive_integer(N):
    try:
        val = int(N)
    except ValueError as e:
        print(str(e) + "\nError: N must be numerical")
    else:
        if val != N:
            raise ValueError("N must be an integer.")
        if val <= 0:
            raise ValueError("N must be strictly positive.")


def validate_positive_number(N):
    try:
        val = float(N)
    except ValueError as e:
        print(str(e) + "\nError: The argument must be numerical")
    else:
        if val < 0:
            raise ValueError("The argument must be positive.")


