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
    std::cerr << "Usage:\ntester.x -N <samplesize> -s <seed> -a <alpha>" << std::endl;
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
