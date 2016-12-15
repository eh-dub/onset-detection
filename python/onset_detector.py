from aubio import onset

def onset_detector(rate=44100
                   ,window_size=4096
                   ,hop_size=1024
                   ,method="default"
                   ,tolerance=0.7
                   ):
    return onset(method, window_size, hop_size, rate);
