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

def hillsAndValleys(array):
    """ Calculate the hills and valleys of a curve.
    Divide by length of array to make this
    agnostic to array length.
                   x
    x             x x
     x      x   x  ^
      x   x   x
        x   ^ ^
        ^
    """

    hills = 0
    valleys = 0
    for i in range(2, len(array) - 2):
        if array[i - 1] < array[i] and array[i + 1] < array[i]:
            hills += 1
        if array[i - 1] > array[i] and array[i + 1] > array[i]:
            valleys += 1

    return float((hills + valleys)) / (len(array))


def curvature(array, hz = 22050):
    """ Calculate the average curavture of the curve"""

    k_sum = 0

    for i in range(2, len(array) - 2):
        slope1 = array[i] - array[i - 1]
        slope2 = array[i + 1] - array[i]
        av_slope = (slope1 + slope2) / 2
        concavity = slope2 - slope1

        k = abs(concavity) / ((1 + av_slope ** 2) ** 1.5)
        k_sum += k

    abs_array = [abs(x) for x in array]
    return (k_sum / (len(array) - 2) ) * hz / max(abs_array)


