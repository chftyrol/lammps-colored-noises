#include "NoiseFilter.h"
#include "WhiteNoise.h"
#include <fftw3.h>

#ifndef __COLOREDNOISE_H__
#define __COLOREDNOISE_H__

class ColoredNoise
{
  public:
    ColoredNoise(double mean, double stddev, double alpha, unsigned seed=0, unsigned samplesize=1024);
    ~ColoredNoise();
    double operator()();
  private:
    double* _sample;
    double _mean;
    double _stddev;
    double _alpha;
    unsigned _seed;
    unsigned _samplesize;
    unsigned _sampleit;
    WhiteNoise* _wngenerator;
    NoiseFilter* _thefilter;
    void _generateSample();
};

#endif // __COLOREDNOISE_H__
