#include <iostream>
#include <cmath>
#include <fftw3.h>
#include "ColoredNoise.h"

int main(int argc, char** argv)
{
  const unsigned N = 500;
  const double mean = 0.;
  const double stddev = 1.0;
  const double alpha = 0.0;
  const unsigned seed = 58;

  ColoredNoise gen(mean, stddev, alpha, seed);

  for(unsigned i = 0; i < N; ++i)
    std::cout << i << "\t" << gen() << std::endl;

  return 0;
}
