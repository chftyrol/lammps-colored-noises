#include <iostream>
#include <string>
#include <iomanip>
#include "ColoredNoise.h"

int main(int argc, char** argv)
{
  unsigned N = 2048;
  double mean = 0.;
  double stddev = 1.0;
  double alpha = 2.0;
  unsigned seed = 79;

  // Parse args
  if(argc < 9)
  {
    std::cerr << "Usage:  tester.x -N <samplesize> -s <seed> -a <alpha> -d <stddev>" << std::endl \
              << "ARGS:" << std::endl \
              << "    samplesize: an unsigned integer value, representing how many random numbers are going to make up the noise sample." << std::endl \
              << "    seed: an unsigned integer value, representing the seed for the random number generator." << std::endl \
              << "    alpha: a non-negative floating point number in the interval [0.0,2.0]. The exponent in (1/f)^alpha, specifying the color of the noise." << std::endl \
              << "    stddev: A positive floating point number, specifying the standard deviation of the white noise used to make colored noise." << std::endl ;
    return 1;
  }
  else
  {
    for(int a = 1; a < argc; ++a)
    {
      if(std::string(argv[a]) == "-N")
      {
        a++;
        N = (unsigned)atoi(argv[a]);
      }
      else if(std::string(argv[a]) == "-s")
      {
        a++;
        seed = (unsigned)atoi(argv[a]);
      }
      else if(std::string(argv[a]) == "-d")
      {
        a++;
        stddev = atof(argv[a]);
      }
      else if(std::string(argv[a]) == "-a")
      {
        a++;
        alpha = atof(argv[a]);
      }
    }
  }

  std::cerr << "N = "               << N                                   << std::endl;
  std::cerr << "seed = "            << seed                                << std::endl;
  std::cerr << std::setprecision(2) << std::fixed << "stddev = " << stddev << std::endl;
  std::cerr << std::setprecision(2) << std::fixed << "alpha = "  << alpha  << std::endl;

  ColoredNoise gen(mean, stddev, alpha, seed, N);

  for(unsigned i = 0; i < N; ++i)
    std::cout << i << "\t" << gen() << std::endl;

  return 0;
}