#include "ColoredNoise.h"

ColoredNoise::ColoredNoise(double mean, double stddev, double alpha, unsigned seed, unsigned samplesize)
  : _mean(mean), _stddev(stddev), _alpha(alpha), _seed(seed), _samplesize(samplesize)
{
  _sample = new double[_samplesize];
  _wngenerator = new WhiteNoise(_mean, _stddev, _seed);
  _thefilter = new NoiseFilter(_alpha, _samplesize);
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
  return _sample[_sampleit];
}

void ColoredNoise::_generateSample()
{
  double* whitenoise = new double[_samplesize];
  // Fill sample with whitenoise.
  for(unsigned k = 0; k < _samplesize; ++k)
    whitenoise[k] = (*_wngenerator)();
  // Apply the colored noise filter.
  _thefilter->filter(whitenoise, _sample);
  // Free up memory occupied by whitenoise.
  delete[] whitenoise;
}
