#include "ColoredNoise.h"

ColoredNoise::ColoredNoise(double mean, double stddev, double alpha, unsigned seed, unsigned samplesize, int fft_flags)
  : _mean(mean), _stddev(stddev), _alpha(alpha), _seed(seed), _samplesize(samplesize), _fft_flags(fft_flags)
{
  _sample = new fftw_complex[_samplesize];
  _wngenerator = new WhiteNoise(_mean, _stddev, _seed);
  _thefilter = new NoiseFilter(_alpha, _samplesize, _fft_flags);
  _sampleit = 0;
  _generateSample();
}

ColoredNoise::~ColoredNoise()
{
  delete[] _sample;
  delete _wngenerator;
  delete _thefilter;
}

double ColoredNoise::operator()()
{
  if(_sampleit >= _samplesize)
  {
    _sampleit = 0;
    _generateSample();
  }
  _sampleit++;
  return _sample[_sampleit][1];
}

void ColoredNoise::_generateSample()
{
  // Fill sample with whitenoise.
  for(unsigned k = 0; k < _samplesize; ++k)
  {
    _sample[k][0] = (*_wngenerator)();
    _sample[k][1] = 0.;
  }
  // Apply the colored noise filter.
  _thefilter->filter(_sample, _sample);
}
