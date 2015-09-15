from ssimTools import drawH, fuzz
import numpy as np
import random
drad = np.pi/180.0

class iv:
# Class to hold the initial variables (iv)
    H = None
    Hi = 0
    Hl=0
    a = None
    e = None
    inc = None

    fdraw = True
    fsize = None
    rnd = None

def setRand(seed):
    # Allow the seed to be set for repeatability
    iv.rnd = random.Random(seed)


def GiMeObj(fname):
    """
    GiMiObj returns an object with orbital elements and observation characteristics.
    GiMiObj takes in a file of orbital elements (the KRQ q200 file in this case), selects an object, "fuzzes" its orbital parameters
    assigns an H magnitude and a colour and then returns it.

    Inputs:
    fname - a file in this director

    Output:
    a - semimajor axis
    e - eccentricity
    inc - inclination (rad)
    node - longitude of the ascending node (rad)
    peri - argument of pericentre (rad)
    M - mean anomaly (rad)
    h - H magnitude in field of survey
    color - array of colour conversion values (see below)
    gb - opposition surge effect
    ph - phase angle
    period - light curve period
    amp - light curve amplitude
    """
    
    rg = iv.rnd

    # ------------- Determine oribal parameters -----------------------

    # **** Read in a, e, inc from a file ****
    # This is only done once, when fdraw = true. Values are stored in iv class above.
    if iv.fdraw==True:
        # fsize is "wc -l" of the input file
        iv.a, iv.e, iv.inc = np.genfromtxt(fname,usecols=(0,1,2), unpack=True)
        # Read in H distribution parameters plus one other deprecated value ....
        iv.alpha_faint, iv.alpha, iv.hmax, iv.hmin, iv.hbreak, iv.contrast = np.genfromtxt('H_dist_vars.txt', unpack=True)
        iv.fsize = len(iv.a)
        # No need to reload the file
        iv.fdraw = False

    # Randomly pick a, e, inc
    rn = int(iv.fsize*rg.random())    
    a = iv.a[rn]
    e = iv.e[rn]
    inc = iv.inc[rn]

    # Assign the three angles randomly
    node = rg.random()*2*np.pi
    peri = rg.random()*2*np.pi
    M = rg.random()*2*np.pi

    # Draw an H magnitude from a SPL, knee, or divot distribution
    # Uses class values as read in from file (see above)
    h = drawH(iv.alpha, iv.hmax, iv.alpha_faint, iv.contrast, iv.hbreak, iv.hmin)

    
    # ------------------------------------------------------------
    # ------------------------------------------------------------

    # ------------- fuzz oribal parameters -----------------------

    q = a*(1.-e)
    qorig = a*(1.-e)
    a=fuzz(a,0.1) # fuzz a by +- 10%
    eorig = e
    if e<.3:
        e = fuzz(e,0.1) # fuzz e by +- 10%
        q= a*(1.-e)
    else:
        q=fuzz(q,0.1) # fuzz q by +- 10%
        e=1.-q/a
    while e<0: # if e < 0, restart the process
        q = qorig
        e = eorig
        if e<.3:
            e = fuzz(e,0.1)
            q= a*(1.-e)
        else:
            q=fuzz(q,0.1)
            e=1.-q/a
    inc = fuzz(inc,1,type='abs')*drad # fuzz inc by +- 1 degree
    # Change radians to degrees

    # ------------------------------------------------------------
    # ------------------------------------------------------------

    epoch = 2453157.5
    gb = -0.12      # Opposition surge effect
    ph = 0.00       # Initial phase of lightcurve
    period = 0.60   # Period of lightcurve
    amp = 0.00      # Amplitude of lightcurve (peak-to-peak)
    #     color : Array of colors (10*R8)
    #                colors[0] : g-x
    #                colors[1] : r-x
    #                colors[2] : i-x
    #                colors[3] : z-x
    #                colors[4] : u-x
    #                colors[5] : V-x
    #                colors[6] : B-x
    #                colors[7] : R-x
    #                colors[8] : I-x  

    gmr = rg.gauss(0.7, 0.2) # g-r colour sampled from gaussian with mu 0.7 and std 0.2 (from CFEPS data)
    color=[gmr, 0.0, 0.0, 0.0, 0.0, 0.0,  0.0, -0.1, 0.0, 0.0]
    # This color array is set-up for r band (note r-x = 0.0). 
    # There is a required 10th element which currently does not correspond to a colour.
    # It is there for future expansion, or so I'm told.

    return a, e, inc, node, peri, M, epoch, h, color, gb, ph, period, amp

    # The call to SurveySubs.detos1 for reference
    # SurveySubs.detos1(a,e,inc,node,peri,M,epoch,h,color,gb,ph,period,amp,survey_dir,seed)

