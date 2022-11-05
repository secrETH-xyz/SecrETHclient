# generate curve and threshold parameters and save them

import pickle
from threshold_crypto.threshold_crypto import CurveParameters, ThresholdParameters

curve_params = CurveParameters()
pickle.dump(curve_params, open('curve_params', 'wb'))

thresh_params = ThresholdParameters(t=3, n=5)
pickle.dump(thresh_params, open('thresh_params', 'wb'))
