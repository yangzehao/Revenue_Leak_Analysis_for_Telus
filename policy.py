# This is the TELUS Credit Policy Function. It should be noted
# that the max credit coefficients are used to calculate the
# max policy credit return. If the real credit, issued by TELUS representative,
# is larger than the max policy credit, revenue leakage can be generated.
def credit_Policy(x):
    if x<1000:
        credit=0.5
    elif x>=1000 and x<=5000:
        credit=0.5
    else:
        credit=0.8
    return x*credit
