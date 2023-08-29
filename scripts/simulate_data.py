import scipy
import numpy as np


def generate_linescan(n_measurements: int = 4,
                      sampling_rate: int = 10,
                      seconds_per_repeat: int = 30,
                      stimulus_peak: int = 15,
                      max_bold_change: float = 2.,
                      negative_bold_chage: float = -.3,
                      repeats: int = 30,
                      n_pixel: int = 128):
    xt = np.linspace(0, seconds_per_repeat*sampling_rate*repeats)
    X = np.ones((n_measurements, n_pixel, seconds_per_repeat*sampling_rate*repeats))
    xts = np.linspace(- 5, 5, seconds_per_repeat*sampling_rate)
    for meas in range(n_measurements):
        for i in range(50, 70):
            X[meas, i] = (1+np.exp(-((xts+(i/50-1))**2))*max_bold_change*(i/70)).tolist()*repeats

        for i in range(70, 90):
            X[meas, i] = (1 + np.exp(-((xts+(i/50-1)) ** 2)) * max_bold_change*((160-i)/90)).tolist() * repeats

        for i in range(92, 110):
            X[meas, i] = (1+ np.exp(-((xts-1-np.abs(i/100-1))**2)) * negative_bold_chage).tolist() * repeats

    X = np.apply_along_axis(lambda m: np.convolve(m, np.array([1]*10)/10, "same"),
                            arr=X, axis=1)
    X[:, :10] = 1
    X[:, -10:] = 1
    X += np.random.normal(size=X.shape)*.5
    return X


def generate_slice(n_measurements: int = 4,
                   sampling_rate: int = 10,
                   seconds_per_repeat: int = 30,
                   stimulus_peak: int = 15,
                   max_bold_change: float = 2.,
                   negative_bold_chage: float = -.3,
                   repeats: int = 10,
                   x_pixel: int = 80,
                   y_pixel: int = 80,
                   cortical_peak = (30, 30)):
    xts = np.linspace(- 5, 5, seconds_per_repeat * sampling_rate)
    X = np.ones((n_measurements, y_pixel, x_pixel, seconds_per_repeat*sampling_rate*repeats))
    scharr = np.ones((4, 4))/16
    for meas in range(n_measurements):
        for i in range(cortical_peak[0], cortical_peak[0]+5):
            for j in range(cortical_peak[1], cortical_peak[1]+5):
                X[meas, i, j] = (1+np.exp(-((xts+((i+j)/30-2))**4))*
                                                             max_bold_change*(i/70)).tolist()*repeats
                X[meas, +7+i, j] = (1+ np.exp(-((xts-1-np.abs(i/100-1))**2)) *
                                                                negative_bold_chage).tolist() * repeats


        for i in range(X.shape[3]):
            X[meas, :, :, i] = scipy.signal.convolve2d(X[meas, :, :, i], scharr, boundary='symm', mode='same')
    X[:, :10] = 1
    X[:, -10:] = 1
    X[:, :, :10] = 1
    X[:, :, -10:] = 1
    X += np.random.normal(size=X.shape) * .2
    return X
