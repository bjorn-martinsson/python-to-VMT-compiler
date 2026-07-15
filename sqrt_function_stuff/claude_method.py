# This is a newly developed method to compute square root accurately
# for all strictly positive float32 values.
# It uses only the basic arithmetic operations available in VMT.
# The relative error of the output is 2.6084596704833984e-09, 
# which far smaller than the precision of a float32. 

# The base algorithm was developed by Claude after being
# tasked to improve a previous attempt of mine.
# It is an unusual twist on a newton raphson,
# that does not require a good initial guess.
# Neither me, nor the AI, knows if this algorithm
# has been discovered before.

# Credit: Adamant helping a ton with prompting the AI.
#         Without his help, this would likely never been found.


def sqrt_claude(x):
    guess = (1.0   + x      ) * 4.3e-12
    guess = (guess + x/guess) * 2.1e-06
    guess = (guess + x/guess) * 0.0014
    guess = (guess + x/guess) * 0.037
    guess = (guess + x/guess) * 0.19
    guess = (guess + x/guess) * 0.41
    guess = (guess + x/guess) * 0.495
    guess = (guess + x/guess) * 0.5
    guess = (guess + x/guess) * 0.5

    return guess



#Here is an explanation of the maths behind it
#
#Define the "relative error" of a guess to be (guess/sqrt(x)). When this is 1, the guess is equal to sqrt(x). 
#
#Assume initially that the relative error is in [exp(-m), exp(m)] for some non-negative real number m. This means the guess is in [sqrt(x)*exp(-m), sqrt(x)*exp(m)].
#
#After an iteration of guess = 0.5 * (guess + x/guess),
#analysis shows that the new relative error lies in [1.0, cosh(m)], where it is 1 if guess was exactly sqrt(x), and cosh(m) if the guess was either of the extremes,sqrt(x)*exp(-m) or sqrt(x)*exp(m).
#
#Since this is an over estimation, claude's idea is to divide the guess by sqrt(cosh(m)). This puts the new guess in [1/sqrt(cosh(m)), sqrt(cosh(m))]. Now we are back where we started, but with m -> ln(sqrt(cosh(m))).
#
#My idea to get nicer constants is to divide by something close to sqrt(cosh(m)) instead of exactly sqrt(cosh(m)). Turns out that this works pretty well if you keep just 2 digits (with some few exceptions).


import math

def round_to_sig_digits(number, n=3):
    if number == 0:
        return 0
    # Calculate the number of decimal places needed
    decimals = n - math.ceil(math.log10(abs(number)))
    return round(number, decimals)

import math
def constants(u_lo, u_hi, eps=1.2e-7):
    m = max(-u_lo, u_hi)
    cs = []
    while math.cosh(m) - 1 > eps:
        c = 1/(2*math.sqrt(math.cosh(m)))

        c = round_to_sig_digits(c, 2 if c < 0.49 else 3)
        #if c >= 0.49:
        #    c = 0.5

        cs.append(("c", c))
        x = max(2*c * math.cosh(m), 1/(2 * c))
        m = math.log(x)
            
    return cs + [("c", 0.5)], math.cosh(m) - 1   # constants, guaranteed rel. error

# Constants that work for x in [-2**64, 2**64]
print(constants(math.log(2**-32), math.log(2**32)))

# Constants that work for all strictly positive float32 values
print(constants(math.log(2**-149)/2, math.log(2**149)/2))
