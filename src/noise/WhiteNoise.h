#include <iostream>
#include <random>
#include <chrono>

#ifndef __WHITENOISE_H__
#define __WHITENOISE_H__

class WhiteNoise
{
  public:
    WhiteNoise(double mean, double stddev, unsigned seed=0);
    double operator()();
  private:
    std::default_random_engine _generator;
    std::normal_distribution<double> _distribution;
    double _mean;
    double _stddev;
    unsigned _seed;
};

#endif // __WHITENOISE_H__
