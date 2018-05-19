#include "ColoredNoise.h"

ColoredNoise::ColoredNoise(double mean, double stddev, double alpha, unsigned seed, unsigned samplesize, double leakcoef)
  : _mean(mean), _stddev(stddev), _alpha(alpha), _seed(seed), _samplesize(samplesize), _leakcoef(leakcoef)
{
  _sample = new double[2 * _samplesize];
  _wngenerator = new WhiteNoise(_mean, _stddev, _seed);
  if(_alpha != 0.0)
    _thefilter = new NoiseFilter(_alpha, _samplesize, _leakcoef);
  _sampleit = 0;
  _generateSample();
}

ColoredNoise::~ColoredNoise()
{
  delete[] _sample;
  delete _wngenerator;
  if(_alpha != 0.0)
    delete _thefilter;
}

double ColoredNoise::operator()()
{
  if(_sampleit >= _samplesize)
  {
    _sampleit = 0;
    _generateSample();
  }
  return _sample[_sampleit++];
}

void ColoredNoise::_generateSample()
{
  double* whitenoise = new double[2 * _samplesize];
  // Fill sample with whitenoise.
  for(unsigned k = 0; k < _samplesize; ++k)
    whitenoise[k] = (*_wngenerator)();
  for(unsigned j = _samplesize; j < 2 * _samplesize; ++j)
    whitenoise[j] = 0.;
  if(_alpha == 0.0)
  {
    // No need to color the white noise.
    _sample = whitenoise;
  }
  else
  {
    // Apply the colored noise filter.
    _thefilter->filter(whitenoise, _sample);
    // Free up memory occupied by whitenoise.
    delete[] whitenoise;
  }
}
