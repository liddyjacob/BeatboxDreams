"""recognize.py
Sound recognition tools
"""

def avgFreq(array):
    """ get the average frequency
    (Number of times array crosses 0)

    """
    # Calculate the number of crosses of the axis to get frequency.
    num_crosses = 0

    if array[0] == 0:
        sign = 0
    else:
        sign = array[0] / abs(array[0])

    for value in array:
        # Do nothing if sign is zero.
        if sign != 0:
            # Sign change
            if value * sign < 0:
                num_crosses += 1

        if value == 0:
            sign = 0
        else:
            sign = value / abs(value)
        continue
        # If the sign is positive

    return len(array) / num_crosses;

def dissipation(array, measurements = 16):
    """ Calculate the dissipation of a frequency.
    The return value is a fration K with the property:
    |max(f)| * K^(j / len(array)) > |f(xj)|
    """
    abs_array = [abs(x) for x in array]
    f_max = max(abs_array)

    sum_k = 0;
    for i in range(1, measurements + 1):
        j = int((len(array) - 1) * i / measurements)
        k = (abs_array[j] / f_max) ** (measurements / i)

        sum_k += k

    return sum_k / measurements

