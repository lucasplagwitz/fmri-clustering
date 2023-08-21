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
