from threshold_crypto.threshold_crypto import *

# load curve_params and thresh_params from storage
curve_params = CurveParameters()
thresh_params = ThresholdParameters(t=3, n=5)

# generate pub_key and key_shares, store them
pub_key, key_shares = create_public_key_and_shares_centralized(curve_params, thresh_params)