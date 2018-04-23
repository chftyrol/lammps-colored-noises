#include "WhiteNoise.h"

WhiteNoise::WhiteNoise(double mean, double stddev, unsigned seed)
  : _mean(mean), _stddev(stddev)
{
  if(!seed)
  {
    // If no seed is specified use a time-based one.
    _seed = std::chrono::system_clock::now().time_since_epoch().count();
  }
  else
  {
    // Otherwise use the provided one.
    _seed = seed;
  }

  // Check if the stddev provided is valid
  if(stddev <= 0)
  {
    std::cerr << "WARNING: Trying to initialize a WhiteNoise with negative stddev!";
  }

  // Initialize the generator
  _generator = std::default_random_engine(_seed);

  // Generate the distribution
  _distribution = std::normal_distribution<double>(_mean, _stddev);
}

double WhiteNoise::operator()()
{
  return _distribution(_generator);
}
