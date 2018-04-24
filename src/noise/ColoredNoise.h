#include "WhiteNoise.h"
#include "NoiseFilter.h"
#include <fftw3.h>
#include <iostream>

class ColoredNoise
{
  public:
    ColoredNoise(double mean, double stddev, double alpha, unsigned seed=0, unsigned samplesize=1024, int fft_flags=FFTW_ESTIMATE);
    ~ColoredNoise();
    double operator()();
  private:
    fftw_complex* _sample;
    double _mean;
    double _stddev;
    double _alpha;
    unsigned _seed;
    unsigned _samplesize;
    unsigned _sampleit;
    int _fft_flags;
    WhiteNoise* _wngenerator;
    NoiseFilter* _thefilter;
    void _generateSample();
};
